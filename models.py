from app import db

class User(db.Model):
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    blogs = db.relationship('Blog', backref='owner')
 
    def __init__(self, username, password):
         self.username = username
         self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True)    
    body = db.Column(db.Text)
    pub_date = db.Column(db.Date)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner, pub_date=None):
        self.title = title
        self.body = body
        self.owner = owner
        #if pub_date is None:
        #    pub_date = date.today()
        self.pub_date = pub_date