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

	return dict(form=crud())
