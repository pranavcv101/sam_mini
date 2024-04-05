from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,EqualTo,Email,DataRequired,ValidationError
#validations are not used now so this above import is not that necesary
from market.models import User


class RegisterForm(FlaskForm):
    #below function for checking the unique constraints  n all but this isnot working(validation part)
    '''   def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists')'''



    username = StringField(label='User name:')#this squre bracket is added to convert the values inside them to list ,validators=[Length(min=2,max=30),DataRequired()]
    email_address= StringField(label='Email')#datarequire is for not to leave that blank alone ,validators=[Email(),DataRequired()]
    password1=PasswordField(label='Password')#,validators=[Length(min=6),DataRequired()]
    password2=PasswordField(label='Confirm Password')#,validators=[EqualTo('password1'),DataRequired()]
    submit=SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    #here also use validations but now no need since learning
    username=StringField(label='User name:')
    password=PasswordField(label='Password')
    submit=SubmitField(label='sign in')

class PurchaseItemForm(FlaskForm):
    submit  = SubmitField(label="Purchase item!")

class SellItemForm(FlaskForm):
    submit  = SubmitField(label="Sell item!")