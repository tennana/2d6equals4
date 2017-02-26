from gluon.contrib.populate import populate
if db(db.auth_user).isempty():
     populate(db.auth_user,10)
     populate(db.participant,10)
     populate(db.user,10)
     populate(db.wishforgametable,10)
