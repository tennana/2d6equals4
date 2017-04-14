# -*- coding: utf-8 -*-
### required - do no delete
import StringIO
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

from gluon.tools import Crud

@auth.requires_membership('admin')
def user_list():
	crud = Crud(db)
	crud.settings.controller = 'ebiadmin'
	crud.settings.detect_record_change = True
	crud.settings.label_separator = ':'

	db.gameTable.convention_id.readable = False
	db.gameTable.created_by.readable = True
	db.gameTable.created_on.readable = True
	db.gameTable.modified_on.readable = True

	db.participant.convention.readable = False
	db.participant.created_by.readable = True
	db.participant.created_on.readable = True
	db.participant.modified_on.readable = True
	db.auth_user.last_name.readable = False

	count = None;
        args = request.args
        if len(args) > 1:
		count = db(db[args[1]]).count()

	return dict(form=crud(),count=count)

@auth.requires_membership('admin')
def export():
    s = StringIO.StringIO()
    db.export_to_csv_file(s)
    response.headers['Content-Type'] = 'text/csv'
    return s.getvalue()

@auth.requires_membership('admin')
def importCSV():
    form = FORM(INPUT(_type='file', _name='data'), INPUT(_type='submit'))
    if form.process().accepted:
        db.import_from_csv_file(form.vars.data.file,unique=False)
    return form

@auth.requires_membership('admin')
def manage():
    table = request.args(0)
    if not table in db.tables():
         return dict(form=TABLE(*[TR(A(name,_href='/ebiadmin/manage/'+name))
                       for name in db.tables]))

    db.gameTable.convention_id.readable = False
    db.gameTable.created_by.readable = True
    db.gameTable.created_on.readable = True
    db.gameTable.modified_on.readable = True
    
    db.participant.convention.readable = False
    db.participant.created_by.readable = True
    db.participant.created_on.readable = True
    db.participant.modified_on.readable = True
    db.auth_user.last_name.readable = False
    grid = SQLFORM.grid(db[table],args=request.args[:1])
    return locals()

@auth.requires_membership('admin')
def today():
    db.gameTable.convention_id.readable = False
    db.gameTable.created_by.readable = True
    db.gameTable.created_on.readable = True
    db.gameTable.modified_on.readable = True
    
    db.participant.convention.readable = False
    db.participant.status.readable = False
    db.participant.created_by.readable = True
    db.participant.created_on.readable = True
    db.participant.modified_on.readable = True
    db.participant.decisionToPlayer.readable = True
    db.participant.decisionToPlayer.writable = True

    db.auth_user.last_name.readable = False
    db.wishforgametable.participant_id.writable = False

    FirstWith = db.wishforgametable.with_alias('first_with')
    SecondWith = db.wishforgametable.with_alias('second_with')
    gameTableGrid = SQLFORM.smartgrid(db.gameTable,create=False,sortable=False)
    grid = SQLFORM.grid(
        db.participant,
        left=(
            FirstWith.on((FirstWith.participant_id==db.participant.id) & (FirstWith.priority==500)),
            SecondWith.on((SecondWith.participant_id==db.participant.id) & (SecondWith.priority==400))
        ),
        fields=[db.participant.id,db.participant.created_by,db.participant.category,db.participant.optional_assist,db.participant.optional_closing_party,db.participant.decisionToPlayer,FirstWith.gametable_id,SecondWith.gametable_id],
        headers={
             'participant.id':'ID',
             'participant.created_by':'参加者名',
             'participant.category':'参加区分',
             'participant.optional_assist':'えび尻尾',
             'participant.optional_closing_party':'懇親会参加',
             'participant.decisionToPlayer':'決定卓',
             'first_with.gametable_id':'第一希望',
             'second_with.gametable_id':'第二希望'
        }
    )

    return locals()