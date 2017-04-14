# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires

# 卓決定
@auth.requires_membership('admin')
def index():
    db.participant.convention.readable = False
    db.participant.status.readable = False
    db.participant.created_by.readable = True
    db.participant.created_on.readable = True
    db.participant.modified_on.readable = True
    db.participant.decisionToPlayer.readable = True
    db.participant.decisionToPlayer.writable = True
    db.participant.lottry_exclude.readable = True
    db.participant.lottry_exclude.writable = True

    db.auth_user.last_name.readable = False
    db.wishforgametable.participant_id.writable = False

    if not request.args(0):
        db.participant.decisionToPlayer.represent = lambda value,row:options_widget(db.participant.decisionToPlayer,value,
                     **{'_name':'decisionToPlayer_row_%s' % row.participant.id})

    if len(request.post_vars) > 0:
        gametable_ids = db(db.gameTable).select(db.gameTable.id,cacheable=True)
        for record in gametable_ids:
              group_id = auth.id_group('convention_%s_%s' % (1,record.id))
              if not group_id:
                  auth.add_group('convention_%s_%s' % (1,record.id),'')
        for key, value in request.post_vars.iteritems():   
            (field_name,sep,row_id) = key.partition('_row_') #name looks like home_state_row_99
            if row_id and db.participant[row_id] and str(db.participant[row_id][field_name]) != str(value):
                user_id = db.participant[row_id].created_by
                for record in gametable_ids:
                    auth.del_membership(auth.id_group('convention_%s_%s' % (1,record.id)),user_id)
                if value == '':
                    value = None
                else:
                    auth.add_membership(auth.id_group('convention_%s_%s' % (1,value)),user_id)
                db(db.participant.id == row_id).update(**{field_name:value})

    FirstWith = db.wishforgametable.with_alias('first_with')
    SecondWith = db.wishforgametable.with_alias('second_with')
    grid = SQLFORM.grid(
        db.participant,
        left=(
            FirstWith.on((FirstWith.participant_id==db.participant.id) & (FirstWith.priority==500)),
            SecondWith.on((SecondWith.participant_id==db.participant.id) & (SecondWith.priority==400))
        ),
        fields=[db.participant.id,db.participant.created_by,db.participant.category,db.participant.lottry_exclude,db.participant.decisionToPlayer,FirstWith.gametable_id,SecondWith.gametable_id],
        headers={
             'participant.id':'ID',
             'participant.created_by':'参加者名',
             'participant.category':'参加区分',
             'participant.optional_assist':'えび尻尾',
             'participant.optional_closing_party':'懇親会参加',
             'participant.decisionToPlayer':'決定卓',
             'first_with.gametable_id':'第一希望',
             'second_with.gametable_id':'第二希望'
        },formname='lottry',user_signature=False,create=False,
        selectable= lambda ids : redirect(URL('lottry','index',vars=request._get_vars)),
        deletable=False,
        details=False,
        editable=True,
    )
    return dict(form=grid)

def options_widget(field,value,**kwargs):
    return SQLFORM.widgets.options.widget(field,value,**kwargs)

def getFirst():
    res = dict()
    rows = db(db.wishforgametable.priority == 500).select(db.wishforgametable.participant_id,db.wishforgametable.gametable_id)
    for row in rows :
        key = 'decisionToPlayer_row_%s' % row.participant_id
        res[key] = row.gametable_id
    return res
