"""
-RESTApi
-RESTful (REpresentational State Transfer architectural style)
-jsonify
-flask-restful
-serialization/deserialization (flask-marshmallow)
"""

from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = "?``§=)()%``ÄLÖkhKLWDO=?)(_:;LKADHJATZQERZRuzeru3rkjsdfLJFÖSJ"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

product_category = db.Table(
    'product_category', db.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
)


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    stock = db.relationship('Stock', back_populates='product')
    categories = db.relationship('Category', secondary=product_category, back_populates='products')


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    products = db.relationship('Product', secondary=product_category, back_populates='categories')


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='stock')


with app.app_context():
    import forms
    db.create_all()


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/api/index')
def index_api():
    return jsonify(['text', 'Hello World!', 'key', True])


@app.route('/api/show_categories')
def show_categories_api():
    categories = Category.query.all()
    categories = [
        {'id': item.id, 'name': item.name} for item in categories
    ]
    return jsonify(categories)


@app.route('/api/create_category', methods=['POST'])
def create_category_api():
    data = request.get_json()
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/api/update_category/<category_id>', methods=['PUT', 'PATCH'])
def update_category_api(category_id):
    data = request.get_json()
    category = Category.query.get(category_id)
    category.name = data.get('name')
    db.session.add(category)
    db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/api/delete_category/<category_id>', methods=['DELETE'])
def delete_category_api(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = forms.AddClientForm()
    if request.method == 'POST':
        name = form.name.data
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('show_clients'))

    return render_template('add_client.html', form=form)


@app.route('/clients')
def show_clients():
    clients = db.session.execute(db.select(Client)).scalars()
    return render_template('clients.html', data=clients)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = forms.CreateProductForm()
    if request.method == 'POST':
        product = Product(name=form.name.data, code=form.code.data)
        for category in form.categories.data:
            cat = Category.query.get(category.id)
            product.categories.append(cat)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_product.html', form=form)


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    form = forms.CreateStockForm()
    if request.method == 'POST':
        stock = Stock(quantity=form.quantity.data, product_id=form.product_id.data.id)
        db.session.add(stock)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_stock.html', form=form)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    form = forms.CreateCategoryForm()
    if request.method == 'POST':
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_category.html', form=form)


@app.route('/show_stock')
def show_stock():
    stock = Stock.query.all()
    return render_template('show_stock.html', data=stock)


@app.route('/show_product_item/<product_id>')
def show_product_item(product_id):
    product = Product.query.get(product_id)
    return render_template('show_product_item.html', product=product)


@app.route('/show_products')
def show_products():
    products = Product.query.all()
    return render_template('show_products.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
