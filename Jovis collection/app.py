from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import stripe
from config import STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, DISCOUNT_CODE
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
stripe.api_key = STRIPE_SECRET_KEY
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

# Initialize products in database
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, name TEXT, price REAL, image TEXT)''')
    # Sample products (use INSERT OR IGNORE so re-running is safe)
    c.execute("INSERT OR IGNORE INTO products (id,name,price,image) VALUES (1,'Men Jacket',120,'jacket.jpg')")
    c.execute("INSERT OR IGNORE INTO products (id,name,price,image) VALUES (2,'Women Bag',80,'bag.jpg')")
    conn.commit()
    conn.close()

init_db()

# Helper to fetch product details
def get_products_by_ids(ids):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if not ids:
        return []
    placeholders = ','.join('?' for _ in ids)
    c.execute(f"SELECT * FROM products WHERE id IN ({placeholders})", tuple(ids))
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def home():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM products WHERE id=?", (product_id,))
    product = c.fetchone()
    conn.close()
    if not product:
        return "Product not found", 404
    return render_template('product.html', product=product)

# Cart page
@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    # prepare full product info
    product_ids = list(cart_items.keys())
    products = get_products_by_ids(product_ids)
    items = []
    total = 0
    for p in products:
        pid = p[0]
        qty = cart_items.get(pid, 0)
        items.append({'id': pid, 'name': p[1], 'price': p[2], 'qty': qty, 'image': p[3]})
        total += p[2] * qty
    discount = session.get('discount', 0)
    total_after_discount = total * (1 - discount)
    return render_template('cart.html', items=items, total=total, discount=discount, total_after_discount=total_after_discount)

# Add to cart
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

# Remove from cart
@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

# Update quantity (POST)
@app.route('/update_cart', methods=['POST'])
def update_cart():
    cart = session.get('cart', {})
    for key, value in request.form.items():
        if key.startswith('qty_'):
            pid = int(key.split('_',1)[1])
            try:
                qty = int(value)
                if qty <= 0:
                    cart.pop(pid, None)
                else:
                    cart[pid] = qty
            except:
                pass
    session['cart'] = cart
    return redirect(url_for('cart'))

# Apply discount
@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    code = request.form.get('discount_code','').strip()
    if code == DISCOUNT_CODE:
        session['discount'] = 0.10  # 10% discount
        session['discount_code'] = code
    else:
        session['discount'] = 0
        session['discount_code'] = ''
    return redirect(url_for('cart'))

# Checkout
@app.route('/checkout', methods=['GET','POST'])
def checkout():
    cart = session.get('cart', {})
    products = get_products_by_ids(list(cart.keys()))
    items = []
    total = 0
    for p in products:
        pid = p[0]
        qty = cart.get(pid, 0)
        items.append({'id': pid, 'name': p[1], 'price': p[2], 'qty': qty})
        total += p[2] * qty
    discount = session.get('discount', 0)
    total_after_discount = round(total * (1 - discount), 2)
    if request.method == 'POST':
        # Create Stripe Checkout Session
        line_items = []
        for item in items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item['name']},
                    'unit_amount': int(item['price'] * 100),
                },
                'quantity': item['qty'],
            })
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cart', _external=True)
        )
        return redirect(checkout_session.url, code=303)
    return render_template('checkout.html', items=items, total=total, discount=discount, total_after_discount=total_after_discount, key=STRIPE_PUBLISHABLE_KEY)

@app.route('/success')
def success():
    session.pop('cart', None)
    session.pop('discount', None)
    session.pop('discount_code', None)
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
