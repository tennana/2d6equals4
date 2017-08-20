# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()

import gluon.contrib.simplejson as json
import datetime
### end requires

def index():
    count = db.participant.id.count()
    list = db(db.participant).select(
	db.participant.category,count
	,groupby=db.participant.category
	,cacheable=True
    )
    return dict(participant_list=SQLTABLE(
	list,
	headers={'participant.category':'参加区分','COUNT(participant.id)':"人数"},
	_id='participant_list'
    ))

def gameTable():
    # テーブル状態取得
    tableNo = None
    if len(request.args)>0 :
        tableNo = request.args[0]
        game_table_info_rows = db((db.gameTable.created_by == db.participant.created_by) & (db.participant.category==1) & (db.gameTable.id==tableNo)).select(cacheable=True)
    else :
        game_table_info_rows = db((db.gameTable.created_by == db.participant.created_by) & (db.participant.category==1)).select(cacheable=True)

    own_participant_record = db.participant(db.participant.created_by==auth.user_id)
    if not own_participant_record :
        return dict(game_table_rows = game_table_info_rows, json_table_data_tag = None)

    # 参加者なら参加情報からタグに必要な情報を作る
    db_wishforgametable = db(db.wishforgametable.participant_id==own_participant_record.id);
    count = db_wishforgametable.count();
    wishforgametable_record = db_wishforgametable.select(orderby=~db.wishforgametable.priority)

    tableInfoForJson = [dict(tableID = r.gameTable.id, tableName = r.gameTable.tableName) for r in game_table_info_rows];
    GMDataDic = dict()
    decisionPlayer = None
    if own_participant_record.category == 1:
        # GM情報の生成
        own_gameTableInfo_record = db(db.gameTable.created_by == own_participant_record.created_by).select(cacheable=True)
        gmTableId = own_gameTableInfo_record.first().id
	db_wish_own_table = db.wishforgametable.gametable_id==gmTableId
        GMDataDic["one"] = db((db_wish_own_table) & (db.wishforgametable.priority == 500)).count()
        GMDataDic["two"] = db((db_wish_own_table) & (db.wishforgametable.priority == 400)).count()
	GMDataDic["gmTableId"] = gmTableId

        decision_participants = db((db.participant.decisionToPlayer == gmTableId) & (db.participant.created_by == auth.user_id))
        if decision_participants.count() > 0:
            GMDataDic["player"] = [dict(name = r.auth_user.first_name) for r in decision_participants.select(cacheable=True)]
            decisionPlayer = GMDataDic["player"]
    else:
        decision_participants = db((db.participant.decisionToPlayer == own_participant_record.decisionToPlayer) & (db.participant.created_by == db.auth_user.id))
        if decision_participants.count() > 0:
            decisionPlayer = [dict(name = r.auth_user.first_name) for r in decision_participants.select(cacheable=True)]

    json_table_data = json.dumps(dict(
         info = tableInfoForJson,
         oneTableID = wishforgametable_record[0].gametable_id if count > 0 else None,
         twoTableID = wishforgametable_record[1].gametable_id if count > 1 else None,
         decision = own_participant_record.decisionToPlayer,
         GMData = GMDataDic,
         decisionPlayer = decisionPlayer
    ))
    return dict(game_table_rows = game_table_info_rows, json_table_data_tag = SCRIPT('var tagData = '+json_table_data, _type='text/javascript'))

@auth.requires_login()
def wish():
    own_participant_record = db.participant(db.participant.created_by==auth.user_id)
    if not own_participant_record :
        return 'error:参加者登録が見つかりません'
    if own_participant_record.decisionToPlayer:
        return 'error:既に参加卓が決まっています'

    db.wishforgametable.update_or_insert(
        ((db.wishforgametable.participant_id == own_participant_record.id) & (db.wishforgametable.priority==500)),
        participant_id= own_participant_record.id,
        gametable_id = request.vars.oneTableID,
        priority = 500
    )

    db.wishforgametable.update_or_insert(
        ((db.wishforgametable.participant_id == own_participant_record.id) & (db.wishforgametable.priority==400)),
        participant_id= own_participant_record.id,
        gametable_id = request.vars.twoTableID,
        priority = 400
    )
    response.flash = '卓希望を更新しました'

def error():
    return dict()

@auth.requires_login()
def participant_manage():
	fields = [
		'first_name','email',
		'category','optional_assist','optional_closing_party'
	]
	useMasterFields = True

	own_participant_record = db.participant(db.participant.created_by==auth.user_id)
	own_gameTable_record = None

	readonly = db.convention[1].openingDate < datetime.datetime.today() # 開始時刻を過ぎたら編集不可

	if auth.user.email:
		db.auth_user.email.writable = False
		fields.remove('email')
	if own_participant_record:
		db.participant.category.writable = False
		if own_participant_record.category == 0:
			useMasterFields = False
	elif readonly:
		return dict(form=B("参加者登録は締め切りました"),conventionName=db.convention[1].name)
	if useMasterFields:
		gametableFields = [
			'systemname','minimumnumber','maximumnumber','gameLevel','belongings','abstract'
		]
		fields.extend(gametableFields)
		own_gameTable_record = db.gameTable(db.gameTable.created_by==auth.user_id)

	fields.append('remark')

	record = None
	if own_participant_record:
		record = own_participant_record.as_dict()
		record.update(auth.user)
		record['tableName'] = ''
		if own_gameTable_record:
			record.update(own_gameTable_record.as_dict())
	form = SQLFORM.factory(db.auth_user,db.participant,db.gameTable,
		table_name='participant_regist',
		record=record,
		showid=False,
		readonly=readonly,
		fields = fields,
		formstyle = 'divs',
		deletable= not readonly,delete_label="参加をキャンセルする"
	)
	form.vars.first_name = auth.user.first_name
	form.vars.email = auth.user.email

	if form.process().accepted:
		if form.deleted:
			own_participant_record.delete_record()
			if own_gameTable_record:
				own_gameTable_record.delete_record()
			response.flash = '参加をキャンセルしました'
		else:
			user = db.auth_user[auth.user.id];
			auth.user.email = form.vars.email
			auth.user.first_name = form.vars.first_name
			user.update_record(**{'email': form.vars.email,'first_name' : form.vars.first_name})

			if useMasterFields:
				if ((not own_participant_record and int(form.vars.category) > 0)
				 or (own_participant_record and own_participant_record.category != 0)):
					form.vars.tableName = '%(first_name)s卓 ' % auth.user + form.vars.systemname
					db.gameTable.update_or_insert(
						(db.gameTable.created_by==auth.user_id),
						**db.gameTable._filter_fields(form.vars)
					)
					form.vars.status = -1

			db.participant.update_or_insert(
				(db.participant.created_by==auth.user_id),
				**db.participant._filter_fields(form.vars)
			)
			db.commit()
			redirect(URL('complete'))
	elif form.errors:
		response.flash = '入力内容にエラーがあります'

	return dict(form=form,conventionName=db.convention[1].name)

def complete():
	return dict()

@auth.requires_login()
def messages():
    import messages as messagesModule
    return messagesModule.messages()
