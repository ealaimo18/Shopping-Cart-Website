import sqlite3, random
from datetime import datetime
from flask import Flask, session, render_template, redirect, url_for, request

app = Flask('app')
app.secret_key = "golden spoon"

@app.route('/', methods=['GET', 'POST'])
def home():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT category_name FROM category;")
    categories = cursor.fetchall()
    cursor.execute("SELECT * FROM product;")
    products = cursor.fetchall()
    return render_template("home.html", categories = categories, products = products)


@app.route('/category/<category_name>', methods=['GET', 'POST'])
def category(category_name):
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT product_name, product_id FROM product JOIN category ON category_name =  product_category_name WHERE category_name = ?", (category_name,));
    products = cursor.fetchall()
    return render_template("category.html", products = products, category_name= category_name)


@app.route('/category/<category_name>/<product_id>', methods=['GET', 'POST'])
def product(category_name, product_id):
  #add error check for if add to cart is pressed without a quantity
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cursor.execute("SELECT * FROM product JOIN category ON category_name =  product_category_name WHERE category_name = ? AND product_id = ?", (category_name, product_id,));
  product_info = cursor.fetchone()
  if 'cart' not in session:
      session['cart'] = dict()
  if 'user_id' not in session:
    add_error = 'please login to add items to the cart'
    return render_template("product.html", add_error = add_error, category_name = category_name, product_info = product_info)
  if request.method == 'POST':
      p_id = request.form['p_id']
      p_qty = request.form['p_qty']
      cart = session['cart']
      if int(p_qty) <= product_info['inventory']:
        if p_id in cart:
          cart[p_id] += int(p_qty)
        else:
          cart[p_id] = int(p_qty)
      session['cart'] = cart
  return render_template("product.html", category_name = category_name, product_info = product_info)


@app.route('/search', methods=['GET', 'POST'])
def search( ):
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if request.method == 'POST':
        r_search = request.form['field_search']
  cursor.execute("SELECT * FROM product WHERE product_name LIKE ? ", ('%'+r_search+'%',));
  results = cursor.fetchall()
  if len(results) == 0:
    search_error = "there were no results for your search :("
    return render_template("search.html", results = results, r_search = r_search, search_error = search_error)
    
  return render_template("search.html", results = results, r_search = r_search)

  
@app.route('/order_history', methods=['GET', 'POST'])
def order_history( ):
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  orders = list()
  # cursor.execute("SELECT DISTINCT order_id FROM orders WHERE order_user = ?", (session['user_id'], ))
  cursor.execute("SELECT DISTINCT order_id, order_date FROM orders WHERE order_user = ? ORDER BY date(order_date) ASC;", (session['user_id'], ))
  orders = cursor.fetchall()    
  return render_template("order_history.html", orders = orders)


@app.route('/order_history/<order_id>', methods=['GET', 'POST'])
def order_details(order_id):
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  # order_items = list()
  cursor.execute("SELECT * FROM product JOIN orders ON order_product = product_id WHERE order_id = ?",(order_id,) )
  order_items = cursor.fetchall()  
  return render_template ("order_details.html", order_items = order_items, order_id = order_id)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout( ):
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  order_id = random.randint(1, 999999999)
  if 'cart' not in session:
    cart_error = "please login to add items to the cart"
    return render_template("cart.html", cart_error = cart_error)
  cart = session['cart']
  keys = cart.keys()
  for key in keys:
    # cursor.execute("INSERT INTO orders (order_id, order_user, order_product, quantity) VALUES (?, ?, ?, ?)", (order_id, session["user_id"], key, cart.get(key)))
    cursor.execute("INSERT INTO orders (order_id, order_user, order_date, order_product, quantity) VALUES (?, ?, ?, ?, ?)", (order_id, session["user_id"], datetime.now() , key, cart.get(key)))
    connection.commit()
    cursor.execute("SELECT inventory FROM product WHERE product_id = ?", (key,))
    cur_inventory = cursor.fetchone()
    new_inventory = cur_inventory[0] - int(cart.get(key))
    cursor.execute("UPDATE product SET inventory = (?) WHERE product_id = ?", (new_inventory, key,))
  cart.clear()
  session['cart'] = cart
  connection.commit()
  return redirect('/')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
  cart = session['cart']
  if request.method == 'POST':
    key = request.form['cart_pid']
    del cart[key]
  session['cart'] = cart
  return redirect('/cart')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  cart_info = list()
  sum = 0
  if 'cart' not in session:
    cart_error = "please login to add items to the cart"
    return render_template("cart.html", cart_error = cart_error)
  cart = session['cart']
  keys = cart.keys()
  qty = list(cart.values())
  for key in keys:
    cursor.execute("SELECT * FROM product WHERE product_id = ?", (key,))
    cart_product = cursor.fetchone()
    sum += cart_product['product_price'] * cart.get(key)
    sum = round(sum, 2)
    cart_info.append(cart_product)
  return render_template("cart.html", cart_info = cart_info, qty = qty, sum = sum)
  

@app.route('/addnewuser', methods=['GET', 'POST'])
def add_new_user():
  connection = sqlite3.connect("myDatabase.db")
  connection.row_factory = sqlite3.Row
  cursor = connection.cursor()
  if request.method == 'POST':
    r_name = request.form['field_name']
    r_username = request.form['field_username']
    r_password = request.form['field_password']
    cursor.execute("INSERT INTO user (name, username, password) VALUES (?, ?, ?)", (r_name, r_username, r_password))
    connection.commit()
    connection.close()
  return render_template ("newuser.html")
  

@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = sqlite3.connect("myDatabase.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    if request.method == 'POST':
        r_username = request.form['field_username']
        r_password = request.form['field_password']
        cursor.execute(
            "SELECT * FROM user WHERE username = ? AND password = ?",
            (r_username, r_password))
        login = cursor.fetchone()
      
        if login is None:
          message = "username or password is incorrect"
          return render_template("login.html", message=message)
        elif len(login) > 0:
          session['user_id'] = login['user_id']
          session['name'] = login["name"]
          session['cart'] = dict()
          return redirect('/')

    connection.close()
    return render_template("login.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
  # Log the user out and redirect them to the home page
  session.clear()
  return redirect('/')


app.run(host='0.0.0.0', port=8080)
