from app import db, models

db.create_all()
u = models.User("ibrahim2", "ibrahim.ghailani2@gmail.comm")
db.session.add(u)
db.session.commit()

print u.to_dict()
u = models.User.query.all()[0]
print u.to_dict()

t = models.Task(title="Title", content="Content", user=u)
db.session.add(t)
db.session.commit()

print t.to_dict()

t = models.Task.query.filter_by(user_id=u.id)[0]

print t.to_dict()
