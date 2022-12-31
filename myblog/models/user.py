from myblog import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    username = db.Column(db.String(length=50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password
    
    def __repr__(self) -> str:
        return f'User: {self.username}'
# db.session.add(User(username="example"))
# db.session.commit()

# users = db.session.execute(db.select(User)).scalars()