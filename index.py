from flask import Flask, render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/gms'
db=SQLAlchemy(app)

#Class of Products
class Product(db.Model):
    pid=db.Column(db.Integer, primary_key=True)
    pname=db.Column(db.String(40), nullable=False)
    price=db.Column(db.Integer, nullable=False)
    quantity_type=db.Column(db.String(10), nullable=False)
    total_quantity=db.Column(db.Integer(), nullable=False)

#First Entry
app.secret_key="login"
@app.route("/")
def home():
    return render_template('homepage.html')

#Logout
@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template('homepage.html')

#Login
@app.route("/login",methods=['POST'])
def login():
    if(request.method=='POST'):
        username=request.form.get('username')
        password=request.form.get('password')
        if (username=='pragati' and password=='abc'):
            session['username']=username
            return redirect("/prod")
        else:
            msg="Invalid username/password"
            return render_template('homepage.html',msg=msg)  

#Add More Products 
@app.route("/product", methods=['GET','POST'])
def product():
    if('username' in session):
        msg="Product Added Successfully"
        if(request.method=='POST'):
            pname=request.form.get('pname')
            price=request.form.get('price')
            quantity_type=request.form.get('quantity_type')
            total_quantity=request.form.get('total_quantity')
            entry=Product(pname=pname,price=price,quantity_type=quantity_type,total_quantity=total_quantity)
            db.session.add(entry)
            db.session.commit()
            return render_template('addmore.html',msg=msg)
        else:
                return render_template('addmore.html')
    else:
        return render_template('homepage.html')

#Display all Products
@app.route("/prod", methods=['POST','GET'])
def prod():
    allproducts=Product.query.all()
    return render_template('My_products.html',allproducts=allproducts)

#Edit the details of product
@app.route('/edit/<int:pid>',methods=['POST','GET'])
def edit(pid):
    if('username' in session):
        user= Product.query.filter_by(pid=pid).first()
        return render_template('update.html',user=user)
    else:
        return render_template('homepage.html')

#update products(editing)
@app.route('/update/<int:pid>',methods=['POST','GET'])
def update(pid):
    if('username' in session):
        msg="Product Updated Successfully"
        if (request.method=='POST'):
            user=Product.query.filter_by(pid=pid).first()
            user.pname=request.form.get('pname')
            user.price=request.form.get('price')
            user.quantity_type=request.form.get('quantity_type')
            user.total_quantity=request.form.get('total_quantity')
            db.session.add(user)
            db.session.commit()
            return render_template('update.html',user=user,msg=msg)
        else:
            return render_template('update.html',user=user)
    else:
        return render_template('homepage.html')
    
#Deleting Products
@app.route('/delete/<int:pid>') 
def delete(pid):
    if ('username' in session):
        user=Product.query.filter_by(pid=pid).first()
        db.session.delete(user)
        db.session.commit()
        flash("Deleted Successfully")
        return redirect('/prod')
    else:
        return render_template('homepage.html')

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        seach_query= request.form['pname']
        products = Product.query.filter(Product.pname.ilike(f'%{seach_query}')).all()
        return render_template('search_results.html', products=products)
    return render_template('My_products.html')

app.run(debug = True)

