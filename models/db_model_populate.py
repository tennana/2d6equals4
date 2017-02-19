from gluon.contrib.populate import populate
if db(db.auth_user).isempty():
     populate(db.auth_user,10)
     populate(db.t_participant,10)
     populate(db.t_user,10)
     populate(db.t_wishforgametable,10)
