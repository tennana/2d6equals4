### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

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
    auth.signature,
    migrate=settings.migrate)

db.convention._enable_record_versioning()

########################################
dic_gameLevel = {0:'TRPG初心者OK',1:'システム初心者OK',2:'経験者向け',3:'濃い'}

db.define_table('gameTable',
    Field('tableName', type='string', required=False, length=512 , writable=False,
          label=T('tableName')),
    Field('systemname', type='string', required=True, length=128 ,
          label=T('SystemName')),
    Field('minimumnumber', type='integer', required=True,
          label=T('MinimumNumber')),
    Field('maximumnumber', type='integer', required=True,
          label=T('MaximumNumber')),
    Field('gameLevel', type='integer', required=True, represent=lambda level,row: dic_gameLevel[level],
          requires = IS_IN_SET(dic_gameLevel,zero=None),
          label=T('Level')),
    Field('belongings', type='string',
          label=T('Belongings')),
    Field('abstract', type='text', required=True,
          label=T('Abstract')),
    Field('convention_id', type='reference convention',
          label=T('Convention Id')),
    auth.signature,
    format='%(tableName)s',
    migrate=settings.migrate)

db.gameTable._enable_record_versioning()

########################################

dic_category = {0:'プレイヤー',1:'ゲームマスター',2:'ヘルP'}

db.define_table('participant',
    Field('convention', type='reference convention'),
    Field('status', type='integer', notnull=True, default = 0,writable=False,
          requires = IS_IN_SET({'-1':'保留中','0':'参加受付','1':'キャンセル待ち','2':'キャンセル'},zero=None),
          label=T('Status')),
    Field('category', type='integer', notnull=True, default = 0,
          represent=lambda category,row: dic_category[category] or '【削除済み】',
          requires = IS_IN_SET(dic_category,zero=None),
          label=T('Category')),
    Field('optional_assist', type='boolean',default = 0,
          label=T('Optional Assist')),
    Field('optional_closing_party', type='boolean', default = 0,
          label=T('Optional Closing Party')),
    Field('decisionToPlayer', type='reference gameTable', writable=False, readable=False, ondelete="SET NULL"),
    Field('lottry_exclude', type='boolean',default = 0, writable=False, readable=False),
    Field('remark', type='text',
          label=T('Remark')),
    auth.signature,
    migrate=settings.migrate)

db.participant._enable_record_versioning()

########################################
db.define_table('wishforgametable',
    Field('participant_id', type='reference participant', required=True, ondelete="CASCADE",
          label=T('Participant Id')),
    Field('gametable_id', type='reference gameTable', required=True, ondelete="CASCADE",
          label=T('Gametable Id')),
    Field('priority', type='integer', default = 0,
          label=T('Priority')),
    auth.signature,
    migrate=settings.migrate)

db.wishforgametable._enable_record_versioning()

