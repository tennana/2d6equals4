response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('TOP'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Participant Regist'),URL('default','participant_manage')==URL(),URL('default','participant_manage'),[]),
(T('卓情報'),URL('default','gameTable')==URL(),URL('default','gameTable'),[]),
]

'''
own_participant_record = db.participant(db.participant.created_by==auth.user_id)
if(own_participant_record):
	response.menu.append(
		((T('メッセージ'),URL('default','messages')==URL(),URL('default','messages'),[
			(T('一覧'),URL('default','messages')==URL('default','messages'),URL('default','messages')),
			(T('新規作成'),URL('default','messages')==URL('default','messages/new'),URL('default','messages/new'))
		]))
	);
'''