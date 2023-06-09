from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Many-to-many relationships tables
childs = db.Table('childs',
    db.Column('tutor_id', db.Integer, db.ForeignKey('tutor.id'), primary_key=True),
    db.Column('child_id', db.Integer, db.ForeignKey('child.id'), primary_key=True)
)

eventhistory = db.Table('eventhistory',
    db.Column('advertiser_id', db.Integer, db.ForeignKey('advertiser.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)
class Participants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))
    was_there = db.Column(db.Boolean)
    score_given = db.Column(db.Integer)

    #Relationships
    event = db.relationship("Event")
    child = db.relationship("Child")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_tutor = db.Column(db.Boolean)
    is_advertiser = db.Column(db.Boolean)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "tutor": self.is_tutor,
            "advertiser": self.is_advertiser
            # do not serialize the password, its a security breach
        }

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    birth = db.Column(db.DateTime, unique=False, nullable=True)
    location = db.Column(db.String(100), unique=False, nullable=True)
    children = db.relationship('Child', secondary = childs)      # Children relation
    avatar = db.Column(db.String(100), unique=False, nullable=True)
    name = db.Column(db.String(50), unique=False, nullable=True)
    lastname = db.Column(db.String(100), unique=False, nullable=True)

    #Relationships
    user = db.relationship("User")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "birth": self.birth,
            "location": self.location,
            "avatar": self.avatar,
            "name": self.name,
            "lastname": self.lastname
        }

class Child(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    birth = db.Column(db.DateTime, unique=False, nullable=False)
    name = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)
    preferences = db.Column(db.String(300), unique=False, nullable=True)
    avatar = db.Column(db.String(100), unique=False, nullable=True)
    school = db.Column(db.String(100), unique=False, nullable=True)
    others = db.Column(db.String(300), unique=False, nullable=True)
    parent = db.Column(db.Integer, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "birth": self.birth,
            "preferences": self.preferences,
            "avatar": self.avatar,
            "school": self.school,
            "others": self.others
        }

class Advertiser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(100), unique=False, nullable=False)
    contact = db.Column(db.Integer, unique=True, nullable=False)
    company = db.Column(db.String(150), unique=True, nullable=False)
    working_since = db.Column(db.DateTime, unique=False, nullable=True)
    description = db.Column(db.String(300), unique=False, nullable=True)
    twitter = db.Column(db.String(150), unique=True, nullable=True)
    avatar = db.Column(db.String(100), unique=False, nullable=True)
    company_image = db.Column(db.String(100), unique=False, nullable=True)
    others = db.Column(db.String(300), unique=False, nullable=True)
    events = db.relationship('Event', secondary = eventhistory)  

     #Relationships
    user = db.relationship("User")
   

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "lastname": self.lastname,
            "contact": self.contact,
            "company": self.company,
            "working_since": self.working_since,
            "description": self.description,
            "twitter": self.twitter,
            "avatar": self.avatar,
            "company_image": self.company_image,
            "others": self.others
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_advertiser = db.Column(db.Integer, db.ForeignKey("advertiser.id"))
    name = db.Column(db.String(200), unique=False, nullable=False)
    localization = db.Column(db.String(200), unique=False, nullable=False)
    min_age = db.Column(db.Integer, unique=False, nullable=False)
    max_age = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String, unique=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=True)
    category = db.Column(db.String(200), unique=False, nullable=False)
    score = db.Column(db.Integer, unique=False, nullable=True)
    score_amount = db.Column(db.Integer, unique=False, nullable=True)
    score_sum = db.Column(db.Integer, unique=False, nullable=True)
    slots = db.Column(db.Integer, unique=False, nullable=True)
    description = db.Column(db.String(300), unique=False, nullable=False)
    done = db.Column(db.Boolean, unique=False, nullable=False)
    contact = db.Column(db.Integer, db.ForeignKey("advertiser.contact"))
    company = db.Column(db.String(150), db.ForeignKey("advertiser.company"))
    cloth = db.Column(db.String(300), unique=False, nullable=True)
    others = db.Column(db.String(300), unique=False, nullable=True)
    participants = db.Column(db.Integer, db.ForeignKey("participants.id"))
    
    # Relationships
    avertiser = db.relationship("Advertiser", foreign_keys = [id_advertiser])
    participants = db.relationship("Participants")

    def serialize(self):
        return {
            "event_id": self.id,
            "advertiser_id": self.id_advertiser,
            "name": self.name,
            "localization": self.localization,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "price": self.price,
            "image":self.image,
            "date": self.date,
            "length": self.length,
            "category": self.category,
            "score": self.score,
            "slots": self.slots,
            "description": self.description,
            "done": self.done,
            "contact": self.contact,
            "company": self.company,
            "cloth": self.cloth,
            "others": self.others,
        }