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
def gametable_manage():
    form = SQLFORM.smartgrid(db.t_gametable,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def wishforgametable_manage():
    form = SQLFORM.smartgrid(db.t_wishforgametable,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def participant_manage():
    form = SQLFORM.smartgrid(db.t_participant,onupdate=auth.archive)
    return locals()

