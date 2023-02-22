from flask import Flask, redirect, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
from waitress import serve
from modules import db
import uuid, hashlib
import string, secrets
import os, json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4().hex)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1000 * 1000

csrf = CSRFProtect()
csrf.init_app(app)

master_password = os.environ["PASSWORD"]
login_token = None

upload_path = 'static/uploads/' + str(datetime.now().year) + '/' + str(datetime.now().month) + '/'

def gethash(string):
    result = hashlib.md5(string.encode())
    return str(result.hexdigest())

def generate_token():
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(72))
    return gethash(token + str(uuid.uuid4().hex))

def save_file(file):
    filename = secure_filename(file.filename)
    hash = hashlib.sha256()
    hash.update(filename.encode())
    new_filename = str(gethash(uuid.uuid4().hex)) + str(hash.hexdigest()) + '.' + filename.split('.')[-1]
    save_path = './' + upload_path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file.save(save_path + new_filename)
    return str('/' + upload_path + new_filename)

def require_login(func):
    def inner(*args, **kwargs):
        if "token" in session:
            if login_token != session["token"]:
                return render_template("admin/login.html", title = "Login"), 403
        else:
            return render_template("admin/login.html", title = "Login"), 403
        return func(*args, **kwargs)
    inner.__name__ = func.__name__
    return inner

## Routes

@app.route('/')
def home():
    with open('./data/slogans.json', 'r') as f:
        data = json.load(f)
    random_index = random.randint(0, len(data) - 1)
    random_slogan = data[random_index]
    menu = db.products.get_all()
    random.shuffle(menu)
    number_of_home_menu_item = 5
    if len(menu) > number_of_home_menu_item:
        n_of_menu_items = number_of_home_menu_item
    else:
        n_of_menu_items = len(menu)
    return render_template("frontend/home.html", title = "Home", menu = menu, n_of_menu_items = n_of_menu_items, slogan_title = random_slogan["title"], slogan = random_slogan["slogan"])

@app.route('/menu')
def menu():
    menu = db.products.get_all()
    random.shuffle(menu)
    return render_template("frontend/menu.html", title = "Menu", menu = menu)

@app.route('/order')
def order():
    if request.args.get('id'):
        menu_item = db.products.get_by_id(request.args.get('id'))
        if not menu_item:
            return render_template("flow/message.html", message = "Error while getting menu item information, maybe the item doesn't exists?", url = "/")
        return render_template("frontend/order.html", item = menu_item, title=f"Order { str(menu_item[1]) }")
    else:
        return render_template("flow/message.html", message = "No menu item selected, please return home and select a menu item.", url = "/")

@app.route('/order/thankyou')
def order_thankyou():
    if 'order_thankyou' in session:
        session.pop('order_thankyou')
        return render_template("frontend/order/thankyou.html", title = "Thank you for your order.")
    else:
        return render_template("frontend/404.html"), 404

## POST Routes

@app.route('/__instafood/order', methods=['POST'])
def collect_order():
    try:
        customer_name = request.values["name"]
        customer_address = request.values["address"]
        customer_phonenumber = request.values["phonenumber"]
        item_id = int(request.values["id"])
        quantity = request.values["quantity"]
    except:
        return render_template("flow/message.html", message = "Error while placing your order.", url = "/")
    item = db.products.get_by_id(item_id)
    if not item:
        return render_template("flow/message.html", message = "Error while placing your order.", url = "/")
    query = db.orders.create(customer_name, customer_address, customer_phonenumber, item[1], quantity, item[5])
    if not query:
        return render_template("flow/message.html", message = "Error while placing your order.", url = "/")
    session["order_thankyou"] = True
    return redirect('/order/thankyou')

## Admin

@app.route('/admin')
@require_login
def admin_dash():
    with open('./data/quotes.json', 'r', encoding='ISO-8859-1') as f:
        data = json.load(f)
    random_index = random.randint(0, len(data) - 1)
    random_quote = data[random_index]
    menu_items = len(db.products.get_all())
    orders = len(db.orders.get_all())
    return render_template("admin/dash.html", title = "Admin", quote = random_quote["quoteText"], quote_author = random_quote["quoteAuthor"], orders = orders, menu_items = menu_items)

@app.route('/admin/orders')
@require_login
def admin_orders():
    orders = db.orders.get_all()
    if orders == False:
        return render_template("flow/message.html", message = "Error while loading orders", url = "/admin")
    return render_template("admin/orders.html", orders = orders, title = "Orders")

@app.route('/admin/menu')
@require_login
def admin_menu():
    menu = db.products.get_all()
    if menu == False:
        return render_template("flow/message.html", message = "Error while loading menu items.", url = "/admin")
    return render_template("admin/menu.html", menu = menu, title = "Menu")

@app.route('/admin/menu/add', methods=['POST'])
@require_login
def admin_menu_add():
    try:
        itemname = str(request.values["name"])
        category = str(request.values["category"]).lower()
        desc = str(request.values["description"])
        image = request.files["image"]
        price = int(request.values["price"])
    except:
        return render_template("flow/message.html", message = "missing info.")
    try:
        uploaded_file = save_file(image)
    except:
        return render_template("flow/message.html", message = "Error while uploading image.", url = '/admin/menu')
    query = db.products.create(itemname, category, desc, uploaded_file, price)
    if query:
        return render_template("flow/message.html", message = "Item added to menu successfully.", url = "/admin/menu")
    else:
        return render_template("flow/message.html", message = "Error while adding item.", url = "/admin/menu")

@app.route('/admin/menu/remove', methods=['POST'])
@require_login
def admin_menu_remove():
    try:
        itemid = int(request.values["id"])
    except:
        return render_template("flow/message.html", message = "missing info.")
    item = db.products.get_by_id(itemid)
    os.remove('.' + item[4])
    query = db.products.delete(itemid)
    if query:
        return render_template("flow/message.html", message = "Product deleted successfully.", url = "/admin/menu")
    else:
        return render_template("flow/message.html", message = "Error while deleting product.", url = "/admin/menu")


@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.values["password"] == master_password:
        global login_token
        login_token = generate_token()
        session["token"] = login_token
        return redirect("/admin")
    else:
        return render_template("flow/message.html", message = "Incorrect login information, please try again.", url = "/admin", title="Login")

@app.route('/admin/logout')
def admin_logout():
    if "token" not in session or session["token"] == None:
        return redirect('/')
    global login_token
    login_token = None
    session.pop("token")
    return render_template("flow/message.html", message = "Logged out successfully.", url = "/")

## Error Handlers

@app.errorhandler(404)
def not_found(e):
  return render_template("frontend/404.html", title="Not Found")

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=6969)