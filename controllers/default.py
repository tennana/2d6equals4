# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
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

	if auth.user.email:
		db.auth_user.email.writable = False
		fields.remove('email')
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
		record.update(auth.user)
		record['tableName'] = ''
		if own_gameTable_record:
			record.update(own_gameTable_record.as_dict())

	form = SQLFORM.factory(db.auth_user,db.participant,db.gameTable,
		table_name='participant_regist',
		record=record,
		showid=False,
		fields = fields,
		formstyle = 'divs',
		deletable=True,delete_label="参加をキャンセルする"
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

			if useMasterFields and form.vars.category.isdigit():
				if (not own_participant_record or own_participant_record.category != 0) and int(form.vars.category) > 0:
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