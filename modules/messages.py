# -*- coding: utf-8 -*-
from gluon import *
from gluon.tools import Crud
from gluon.html import *

def messages(db,auth,request):

    crud= Crud(db)
    crud.settings.formstyle = 'table3cols'
    crud.settings.keepvalues = True
    crud.messages.submit_button = '送信'
    crud.messages.delete_label = '削除する'
    crud.messages.record_created = 'メッセージを作成しました'
    crud.messages.record_updated = 'メッセージを更新しました'
    crud.messages.record_deleted = '削除しました'
    crud.messages.create_log = 'Message Record %(id)s created'
    crud.messages.update_log = 'Message Record %(id)s updated'
    crud.settings.create_next = URL('messages')
    crud.settings.download_url = URL('download')

    button = A(BUTTON('リストへ戻る'),_href=URL('messages'));
    db.messages.to_group.represent = show_to_group
    db.messages.to_group.requires = IS_IN_SET(get_to_group_list(),zero=None)
    db.messages.created_by.label = '作成者'
    db.messages.created_by.readable = True

    if(request.args(0) == 'read'):
        crud.settings.auth = auth
	if auth.has_permission('update', db.messages, request.args(1)):
		button += A(BUTTON('編集する'),_href=URL('messages/update',request.args(1)));
        return dict(form=crud.read(db.messages,request.args(1)),button=button)
    if(request.args(0) == 'new'):
        return dict(form=crud.create(db.messages,onaccept=give_create_message_permission),button=button)
    if(request.args(0) == 'update'):
        crud.settings.auth = auth
	db.messages.to_group.writable = False
        return dict(form=crud.update(db.messages,request.args(1), deletable=True),button=button)

    query = auth.accessible_query('read', db.messages, auth.user.id)
    db.messages.title.represent = lambda title, row:A(title,_href=URL(args=('read',row.id)))
    db.messages.id.represent = lambda id, row:''
    form = crud.select(db.messages,query=query, fields=['title','created_by','modified_on','id'], orderby=~db.messages.modified_on,
           headers={'messages.title':'件名','messages.created_by': db.messages.created_by.label,'messages.modified_on':'更新時刻','messages.id':''})
    return dict(form=form,button=A(BUTTON('新規作成'),_href=URL('messages/new')))

def give_create_message_permission(form):
    db = current.db
    auth = current.auth

    message_id = form.vars.id
    group_id = auth.id_group('user_%s' % auth.user.id)
    auth.add_permission(group_id, 'read', db.messages,message_id)
    auth.add_permission(group_id, 'update', db.messages,message_id)
    auth.add_permission(group_id, 'delete', db.messages,message_id)
    # 宛先
    auth.add_permission(form.vars.to_group, 'read', db.messages,message_id)

def show_to_group(id,row):
	return get_to_group_list()[id]

def get_to_group_list():
	db = current.db
	auth = current.auth
	dicToGroup = {auth.id_group('admin'):'EbiconHQ'}
	own_participant_record = db.participant(db.participant.created_by==auth.user_id)
	if own_participant_record and own_participant_record.decisionToPlayer:
		id = auth.id_group('convention_%s_%s' % (own_participant_record.convention_id,own_participant_record.decisionToPlayer))
		if id:
			dicToGroup[id] = '参加卓の全員'
	return dicToGroup
