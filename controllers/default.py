# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def participant_manage():
	fields = [
		'category','optional_assist','optional_closing_party'
	]
	useMasterFields = True

	own_participant_record = db.participant(db.participant.created_by==auth.user_id)
	own_gameTable_record = None
	if own_participant_record:
		db.participant.category.writable = False
		if own_participant_record.category == 0:
			useMasterFields = False
	if useMasterFields:
		gametableFields = [
			'systemname','minimumnumber','maximumnumber','gameLevel','belongings','abstract'
		]
		fields.extend(gametableFields)
		own_gameTable_record = db.gameTable(db.gameTable.created_by==auth.user_id)

	fields.append('remark');

	record = None
	if own_participant_record:
		record = own_participant_record.as_dict()
		if own_gameTable_record:
			record.update(own_gameTable_record.as_dict())

	form = SQLFORM.factory(db.participant,db.gameTable,
		table_name='participant_regist',
		record=record,
		showid=False,
		fields = fields,
		formstyle = 'divs',
		deletable=True,delete_label="参加をキャンセルする"
	)
	if form.process().accepted:
		if form.deleted:
			own_participant_record.delete_record()
			if own_gameTable_record:
				own_gameTable_record.delete_record()
			response.flash = '参加をキャンセルしました'
		else:
			form.vars.tableName = '%(first_name)s卓 ' % auth.user + form.vars.systemname
			db.participant.update_or_insert(
				(db.participant.created_by==auth.user_id),
				**db.participant._filter_fields(form.vars)
			)
			if (form.vars.category != 0 & useMasterFields):
				db.gameTable.update_or_insert(
					(db.gameTable.created_by==auth.user_id),
					**db.gameTable._filter_fields(form.vars)
				)
			if own_participant_record:
				response.flash = '参加情報を更新しました'
			else :
				response.flash = '参加受付が完了しました'
	elif form.errors:
		response.flash = '入力内容にエラーがあります'

	return dict(form=form,conventionName=db.convention[1].name)

