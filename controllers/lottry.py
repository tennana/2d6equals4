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

def lot():
	res = dict()

	FirstWith = db.wishforgametable.with_alias('first_with')
	SecondWith = db.wishforgametable.with_alias('second_with')
	db_participant = db((db.participant.category!=1) & ((db.participant.lottry_exclude == 0) | (db.participant.lottry_exclude == None)))
	participant_records = db_participant.select(
	db.participant.id,db.participant.created_by,db.participant.category,db.participant.decisionToPlayer,FirstWith.gametable_id,SecondWith.gametable_id,
	left=[
	    FirstWith.on((FirstWith.participant_id==db.participant.id) & (FirstWith.priority==500)),
	    SecondWith.on((SecondWith.participant_id==db.participant.id) & (SecondWith.priority==400))
	],
        orderby='<random>')
	print db._lastsql
	gameTable_ids = []
	gameTable_max = []
	db_gameTable = db((db.gameTable.created_by == db.participant.created_by) & (db.participant.category==1))
	gameTableCount = db_gameTable.count()
        for gametable_record in db_gameTable.select(cacheable=True, orderby='<random>'):
		gameTable_ids.append(gametable_record.gameTable.id)
		gameTable_max.append(gametable_record.gameTable.maximumnumber)

	gameTable_prefl = range(db_participant.count())
	all_prefs = []
	for row in participant_records:
		own_prefs = range(gameTableCount)
		if row.first_with:
			first_table_id = row.first_with.gametable_id
			if first_table_id:
				first_table_index = gameTable_ids.index(first_table_id)
				own_prefs[first_table_index], own_prefs[gameTableCount-1] = own_prefs[gameTableCount-1], own_prefs[first_table_index]
		if row.second_with:
			second_table_id = row.second_with.gametable_id
			if second_table_id:
				second_table_index = gameTable_ids.index(second_table_id)
				own_prefs[second_table_index], own_prefs[gameTableCount-2] = own_prefs[gameTableCount-2], own_prefs[second_table_index]
		all_prefs.append(own_prefs)
        matching = stable_matching2(all_prefs,gameTable_prefl,gameTable_max)
	index = 0;
	for row in participant_records:
	        key = 'decisionToPlayer_row_%s' % row.participant.id
		res[key] = gameTable_ids[matching[index]]
		index+=1

	return res


"""
Copyright: 2015-2017 Saito Tsutomu
License: Python Software Foundation License
"""
def stable_matching(prefm, preff):
    """
    安定マッチング問題
    入力
        prefm, preff: 選好
    出力
        マッチング
    """
    res, n = {}, len(prefm)
    pos, freem = [0] * n, list(range(n-1, -1, -1))
    while freem:
        m, freem = freem[-1], freem[:-1]
        if pos[m] == n: continue
        f, pos[m] = prefm[m][pos[m]], pos[m]+1
        if f in res:
            if preff[f].index(res[f]) < preff[f].index(m):
                freem.append(m)
                continue
            else: freem.append(res[f])
        res[f] = m
    return res


def stable_matching2(prefs, prefl, capa):
    """
    非対称マッチング
    prefs: 卓に対する選好
    prefl: 参加者に対する選好(全ての卓は同じ選好とする)
    capa: 卓の受入可能数
    """
    acca = list(accumulate([0] + capa[:-1])) # 累積受入可能数
    idx = [i for i, j in enumerate(capa) for _ in range(j)] # ダミー配属先→配属先の変換リスト
    prefs = [[j+acca[i] for i in pr for j in range(capa[i])] for pr in prefs] # ダミーの選考
    res = stable_matching([prefl] * len(prefl), prefs)
    return{k:idx[v] for k, v in res.items()} # ダミーをオリジナルに戻して返す

def accumulate(iterable):
    'Return running totals'
    # accumulate([1,2,3,4,5]) --> 1 3 6 10 15
    # accumulate([1,2,3,4,5], operator.mul) --> 1 2 6 24 120
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = total + element
        yield total