from market import db,login_manager
from market import bcrypt#from flask_bcrypt import generate_password_hash ### i mistakely wrote flask instead of market in the above import and full problem remeber
from flask_login import UserMixin #to avoid the errors in login manager stuff


#the below three lines we got from a site when an exception got raised
#from a login try we did and this is for some loader thing
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(length=30),nullable=False,unique=True)
    email_address=db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash=db.Column(db.String(length=60),nullable=False)
    budget=db.Column(db.Integer(),nullable=False,default=1000)
    items=db.relationship('Item',backref='owned_user',lazy=True)#backref allows to see who the owner of the  splecific item is
    #lazy= True is given so the sql alchemy will grab all objects of items

    @property
    def prettier_budget(self):#to give comas in budgets, number ex 100,000
        if len(str(self.budget))>=4:
            return f"{str(self.budget)[:-3]},{str(self.budget)[-3:]}$"
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password


    @password.setter
    def password(self,plain_text_password):
       self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self,attempted_password):
        return bcrypt.check_password_hash(self.password_hash,attempted_password)
            
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self,item_obj):
        return item_obj in self.items
        
    




class Item(db.Model):
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    quantity =db.Column(db.Integer(),nullable=False)
    description=db.Column(db.String(length=1024),nullable=False)
    owner = db.Column(db.Integer(),db.ForeignKey('user.id'))

    

    def __repr__(self): #this helps to see in better the list of items when v try to c them in terminal through databses(refer1.42)
        return f'Item {self.name}'
    
    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self,user):
        self.owner = None
        user.budget += self.price
        db.session.commit()

