from app import app, db

app.run(debug=True)

db.create_all()
