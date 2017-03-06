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
	return dict(form=crud())
