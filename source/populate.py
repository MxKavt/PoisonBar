from source.extensions import db
from source import create_app

app = create_app()
app.app_context().push()

db.drop_all()
db.create_all()
db.session.commit()



