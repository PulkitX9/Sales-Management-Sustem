from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'sales.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class Store(db.Model):
    StoreID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))

class Product(db.Model):
    ProductID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))
    Price = db.Column(db.Float)
    StoreID = db.Column(db.Integer, db.ForeignKey('store.StoreID'))

class Orders(db.Model):
    OrderNumber = db.Column(db.Integer, primary_key=True,autoincrement=True)
    OrderDate = db.Column(db.String(20))
    CustomerID = db.Column(db.Integer)
    ProductID = db.Column(db.Integer)

class Customer(db.Model):
    CustomerID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(100))

class Employee(db.Model):
    EmployeeID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    Name = db.Column(db.String(100))
    Address = db.Column(db.String(255))
    Email = db.Column(db.String(100))
    Role = db.Column(db.String(50))

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('role'):
                flash("Please log in first to continue.")
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash("Access denied: You do not have permission to access this page.")
                return redirect(url_for('home'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper


# --- Auth ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'Admin' and password == 'admin123':
            session['role'] = 'Admin'
            return redirect(url_for('home'))

        employee = Employee.query.filter_by(Name=username).first()
        if employee:
            session['role'] = employee.Role
            session['employee_id'] = employee.EmployeeID
            return redirect(url_for('home'))

        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
# --- Routes ---
@app.route('/')
def home():
    return render_template('home.html')

# ----- STORE -----
@app.route('/stores')
@role_required('Admin')
def view_stores():
    stores = Store.query.all()
    return render_template('stores.html', stores=stores)

@app.route('/stores/add', methods=['GET', 'POST'])
@role_required('Admin')
def add_store():
    if not session.get('admin'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        new_store = Store(Name=name)
        db.session.add(new_store)
        db.session.commit()
        return redirect(url_for('view_stores'))
    return render_template('add_store.html')

@app.route('/stores/edit/<int:store_id>', methods=['GET', 'POST'])
@role_required('Admin')
def edit_store(store_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    store = Store.query.get_or_404(store_id)
    if request.method == 'POST':
        store.Name = request.form['name']
        db.session.commit()
        return redirect(url_for('view_stores'))
    return render_template('edit_store.html', store=store)

@app.route('/stores/delete/<int:store_id>')
@role_required('Admin')
def delete_store(store_id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    store = Store.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    return redirect(url_for('view_stores'))

# ----- PRODUCT -----
@app.route('/products')
@role_required('Admin', 'ProductManager')
def view_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@role_required('Admin', 'ProductManager')
def add_product():
    stores = Store.query.all()
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        store_id = int(request.form['store_id'])
        print("Adding Product: ", name, price, store_id)
        new_product = Product(Name=name, Price=price, StoreID=store_id)
        db.session.add(new_product)
        db.session.commit()
        print("Product Added Successfully")
        return redirect(url_for('view_products'))
    return render_template('add_product.html', stores=stores)

@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@role_required('Admin', 'ProductManager')
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    stores = Store.query.all()
    if request.method == 'POST':
        product.Name = request.form['name']
        product.Price = float(request.form['price'])
        product.StoreID = int(request.form['store_id'])
        db.session.commit()
        return redirect(url_for('view_products'))
    return render_template('edit_product.html', product=product, stores=stores)

@app.route('/products/delete/<int:product_id>')
@role_required('Admin', 'ProductManager')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('view_products'))

# ----- ORDERS -----
@app.route('/orders')
@role_required('Admin', 'SalesManager')
def view_orders():
    orders = Orders.query.all()
    return render_template('orders.html', orders=orders)

@app.route('/orders/add', methods=['GET', 'POST'])
@role_required('Admin', 'SalesManager')
def add_order():
    products = Product.query.all()
    customers = Customer.query.all()
    if request.method == 'POST':
        order_date = request.form['order_date']
        customer_id = int(request.form['customer_id'])
        product_id = int(request.form['product_id'])
        new_order = Orders(OrderDate=order_date, CustomerID=customer_id, ProductID=product_id)
        db.session.add(new_order)
        db.session.commit()
        return redirect(url_for('view_orders'))
    return render_template('add_order.html', products=products, customers=customers)

@app.route('/orders/edit/<int:order_number>', methods=['GET', 'POST'])
@role_required('Admin', 'SalesManager')
def edit_order(order_number):
    order = Orders.query.get_or_404(order_number)
    products = Product.query.all()
    customers = Customer.query.all()
    if request.method == 'POST':
        order.OrderDate = request.form['order_date']
        order.CustomerID = int(request.form['customer_id'])
        order.ProductID = int(request.form['product_id'])
        db.session.commit()
        return redirect(url_for('view_orders'))
    return render_template('edit_order.html', order=order, products=products, customers=customers)

@app.route('/orders/delete/<int:order_number>')
@role_required('Admin', 'SalesManager')
def delete_order(order_number):
    order = Orders.query.get_or_404(order_number)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for('view_orders'))

# ----- CUSTOMERS -----
@app.route('/customers')
@role_required('Admin', 'SalesManager')
def view_customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/customers/add', methods=['GET', 'POST'])
@role_required('Admin', 'SalesManager')
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        new_customer = Customer(Name=name, Address=address, Email=email)
        db.session.add(new_customer)
        db.session.commit()
        return redirect(url_for('view_customers'))
    return render_template('add_customer.html')

@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
@role_required('Admin', 'SalesManager')
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == 'POST':
        customer.Name = request.form['name']
        customer.Address = request.form['address']
        customer.Email = request.form['email']
        db.session.commit()
        return redirect(url_for('view_customers'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/delete/<int:customer_id>')
@role_required('Admin', 'SalesManager')
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for('view_customers'))

@app.route('/customers/<int:customer_id>/orders')
def customer_orders(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    results = db.session.query(
        Orders.OrderNumber,
        Orders.OrderDate,
        Product.Name.label("ProductName"),
        Product.Price
    ).join(Product, Orders.ProductID == Product.ProductID)\
     .filter(Orders.CustomerID == customer_id).all()

    orders = [
        {
            "OrderNumber": r[0],
            "OrderDate": r[1],
            "ProductName": r[2],
            "Price": r[3]
        } for r in results
    ]

    total_spent = sum(order["Price"] for order in orders)

    return render_template(
        'customer_orders.html',
        customer=customer,
        orders=orders,
        total_spent=total_spent
    )

@app.route('/customers/<int:customer_id>/orders/add', methods=['GET', 'POST'])
@role_required('Admin', 'SalesManager')
def add_order_for_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    products = Product.query.all()
    
    if request.method == 'POST':
        order_date = request.form['order_date']
        product_id = int(request.form['product_id'])
        
        new_order = Orders(OrderDate=order_date, CustomerID=customer_id, ProductID=product_id)
        db.session.add(new_order)
        db.session.commit()
        
        return redirect(url_for('customer_orders', customer_id=customer_id))
    
    return render_template('add_order_for_customer.html', customer=customer, products=products)


# ----- EMPLOYEES -----
@app.route('/employees')
def view_employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/employees/add', methods=['GET', 'POST'])
@role_required('Admin')
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        role = request.form.get('role')
        new_employee = Employee(Name=name, Address=address, Email=email,Role=role)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('view_employees'))
    return render_template('add_employee.html')

@app.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
@role_required('Admin')
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'POST':
        employee.Name = request.form['name']
        employee.Address = request.form['address']
        employee.Email = request.form['email']
        employee.role = request.form.get('role')
        db.session.commit()
        return redirect(url_for('view_employees'))
    return render_template('edit_employee.html', employee=employee)

@app.route('/employees/delete/<int:employee_id>')
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('view_employees'))

if __name__ == '__main__':
    app.run(debug=True)
