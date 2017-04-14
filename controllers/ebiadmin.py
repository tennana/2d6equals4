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