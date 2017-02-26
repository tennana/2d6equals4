from gluon.storage import Storage
# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
myconf = AppConfig(reload=True)

settings = Storage()

settings.migrate = myconf.get('db.migrate')
settings.title = myconf.get('app.name')
settings.subtitle = myconf.get('app.subtitle')
settings.author = myconf.get('app.author')
settings.author_email = myconf.get('app.email')
settings.keywords = myconf.get('app.keywords')
settings.description = myconf.get('app.description')
settings.layout_theme = 'Default'
settings.database_uri = myconf.get('db.uri')
settings.security_key = myconf.get('db.security_key')
settings.email_server = myconf.get('smtp.server')
settings.email_sender = myconf.get('smtp.sender')
settings.email_login = ''
settings.login_method = 'janrain'
settings.janrain_app_name = myconf.get('janrain.app_name')
settings.janrain_secret_key = myconf.get('janrain.secret_key')
settings.plugins = []
