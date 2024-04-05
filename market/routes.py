from market import app
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,PurchaseItemForm,SellItemForm
from market import db
from flask_login import login_user,logout_user,login_required,current_user

@app.route("/")
@app.route("/home")
def home_page():
    return render_template("home.html")

@app.route('/market',methods=['GET','POST'])
@login_required 
#this login required decorater wont let u get to market page without logging in
def market_page():
   
   ''' items = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "quantity": 5
    },
    {
        "id": 2,
        "name": "Headphones",
        "price": 49.99,
        "quantity": 10
    },
    {
        "id": 3,
        "name": "Notebook",
        "price": 5.99,
        "quantity": 20
    }
    ]'''#this is commented for demonstration of item using queries
   purchase_form=PurchaseItemForm()
   selling_form = SellItemForm()
   ''' if purchase_form.validate_on_submit():
   #  print(purchase_form['purchased_item'])#this is to c info in server side refer 5.31 n before
   print(request.form.get('purchased_item'))#same as the above commented line'''
   #the above thing was commented beacuse while executing that one r asked by the browser to fill the form if we try to refresh for more info refer 5.31 itself
   #to remove that if we r using the below stuff
   if request.method == "POST":
       #Purchase item logic
       purchased_item=request.form.get('purchased_item')
       p_item_object = Item.query.filter_by(name=purchased_item).first()
       if p_item_object:
           if current_user.can_purchase(p_item_object):
              p_item_object.buy(current_user)#this was implemented differently first ref5.50
              
              flash(f"congratulations ! you purchsed {p_item_object.name} for {p_item_object.price} ")
           else:
               flash(f"you dont have enough money to buy{p_item_object.name}")
       #Selling item logic
       sold_item = request.form.get("sold_item")
       s_item_object = Item.query.filter_by(name=sold_item).first()
       if s_item_object:
           if current_user.can_sell(s_item_object):
               s_item_object.sell(current_user)
               flash(f"congratulations ! you sold {s_item_object.name} for {s_item_object.price} ")
           else:
               flash(f"something went wrong while selling",category='danger')
       return redirect(url_for("market_page"))      
   if request.method == "GET":     #this also same reason as the above post if thing 
   #items=Item.query.all()#this is commented ref 5.24 because this displays all the items
      items=Item.query.filter_by(owner=None)
      owned_items = Item.query.filter_by(owner = current_user.id)


   return render_template("market.html", items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)


@app.route('/register',methods=['GET','POST'])#this is given so that our route ccan handle post also
def register_page():

    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,
                            email_address=form.email_address.data,
                            password=form.password1.data,#this password is set by the password setter we used in models
                            ) 
        db.session.add(user_to_create)   
        db.session.commit()
        return redirect(url_for('market_page'))
    #the below code was used in validation but didnt work refer 2.51
    '''if form.errors != {}: #if no errors from the validatitons
        for err_msg in form.errors.values():
            print(f'There was an error : {err_msg}')
            #due to some reason the error r directly being seen in the form place itself lucky
           # flash(f'There was an error : {err_msg}')#so users also can c the error for this we need to import flash and related stuff'''
    return render_template('register.html',form=form)
    
@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username = form.username.data).first()  #i think tis first is used to really grab the objects other wise the entire stuff is taken something like that
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'success!logged in: {attempted_user.username}',category='success')
            return redirect(url_for('market_page')) 
        else:
            flash("username and password donot match",category='danger')#danger provides that red colour message

                                                             
    return render_template('login.html',form=form)



@app.route('/logout')
def logout_page():
    logout_user()
    #this  is enough this inbuilt function will automatically logout the user
    #now we can put some flashmesssage to show the user that v have logout but this flash shit is not working in my 
    flash("logged out succesfully",category='info')
    return redirect(url_for("home_page"))