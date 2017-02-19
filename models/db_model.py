### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

########################################
db.define_table('users',
    Field('name', type='string',
          label=T('Name')),
    Field('email_authid', type='reference auth_user',
          label=T('Email Authid')),
    Field('twitter', type='reference auth_user',
          label=T('Twitter')),
    Field('google', type='reference auth_user',
          label=T('Google')),
    Field('oAuth', type='reference auth_user',
          label=T('oAuth')),
    auth.signature,
    migrate=settings.migrate)

db.define_table('t_user_archive',db.users,Field('current_record','reference users',readable=False,writable=False))

########################################
db.define_table('convention',
    Field('name', type='string', length=320,
          label=T('Name')),
    Field('gamemasterduedate', type='datetime', required=True,
          label=T('Gamemasterduedate')),
    Field('reservemasterduedate', type='datetime', required=True,
          label=T('ReserveMasterDueDate')),
    Field('playerduedate', type='datetime', required=True,
          label=T('PlayerDueDate')),
    Field('openingDate', type='datetime', required=True,
          label=T('Date')),
    Field('adminuserid', type='reference users', required=True,
          label=T('AdminUserID')),
    auth.signature,
    migrate=settings.migrate)

db.define_table('t_convention_archive',db.convention,Field('current_record','reference convention',readable=False,writable=False))

########################################
db.define_table('gameTable',
    Field('name', type='string', required=True, length=512 ,
          label=T('Name')),
    Field('systemname', type='string', required=True, length=128 ,
          label=T('SystemName')),
    Field('minimumnumber', type='integer', required=True,
          label=T('MinimumNumber')),
    Field('maximumnumber', type='integer', required=True,
          label=T('MaximumNumber')),
    Field('gameLevel', type='integer', required=True,
          label=T('Level')),
    Field('belongings', type='text',
          label=T('Belongings')),
    Field('abstract', type='text', required=True,
          label=T('Abstract')),
    Field('remark', type='text',
          label=T('Remark')),
    Field('convention_id', type='reference convention',
          label=T('Convention Id')),
    Field('gamemaster_id', type='reference users',
          label=T('GameMaster Id')),
    auth.signature,
    migrate=settings.migrate)

db.define_table('t_gametable_archive',db.gameTable,Field('current_record','reference gameTable',readable=False,writable=False))

########################################
db.define_table('participant',
    Field('convention', type='reference convention'),
    Field('status', type='integer', notnull=True, default = 0,
          label=T('Status')),
    Field('category', type='integer', notnull=True, default = 0,
          label=T('Category')),
    Field('optional_assist', type='integer',default = 0,
          label=T('Optional Assist')),
    Field('optional_closing_party', type='integer', default = 0,
          label=T('Optional Closing Party')),
    Field('decisionToPlayer', type='reference gameTable'),
    Field('remark', type='text',
          label=T('Remark')),
    auth.signature,
    migrate=settings.migrate)

db.define_table('t_participant_archive',db.participant,Field('current_record','reference participant',readable=False,writable=False))

########################################
db.define_table('wishforgametable',
    Field('participant_id', type='reference participant', required=True,
          label=T('Participant Id')),
    Field('gametable_id', type='reference gameTable', required=True,
          label=T('Gametable Id')),
    Field('priority', type='integer', default = 999,
          label=T('Priority')),
    auth.signature,
    migrate=settings.migrate)

db.define_table('t_wishforgametable_archive',db.wishforgametable,Field('current_record','reference wishforgametable',readable=False,writable=False))
