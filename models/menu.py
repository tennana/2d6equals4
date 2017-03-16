response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('TOP'),URL('default','index')==URL(),URL('default','index'),[]),
(T('Participant Regist'),URL('default','participant_manage')==URL(),URL('default','participant_manage'),[]),
]
