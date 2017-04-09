# -*- coding: utf-8 -*-
db.define_table('messages',
    Field('convention_id', type='reference convention', default=1, required=True,
          label=T('Convention'),writable=False,readable=False),
    Field('to_group', type='reference auth_group', label='宛先'),
    Field('title', type='string', required=True, label='件名'),
    Field('body', type='text', required=True, label='本文'),
    Field('attechment', type='upload', label='添付ファイル',autodelete=True),
    auth.signature,
    migrate=settings.migrate)
db.messages.id.readable = False
db.messages.id.writable = False

db.messages.attechment.authorize = lambda record:    auth.is_logged_in() and    auth.has_permission('read', db.messages, record.id, auth.user.id)

db.messages._enable_record_versioning()
