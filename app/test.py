from app import db, models

db.create_all()
u = models.User("ibrahim", "ibrahim.ghailani@gmail.comm")
db.session.add(u)
db.session.commit()

print u
u = models.User.query.all()[0]
print u

t = models.Task(title="Title", content="Content", user=u)
db.session.add(t)
db.session.commit()

print t

t = models.Task.query.all()[0]

print t
