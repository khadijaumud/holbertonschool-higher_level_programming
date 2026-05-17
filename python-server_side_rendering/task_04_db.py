from flask import Flask, render_template, request
import json
import csv
import sqlite3

app = Flask(__name__)

def read_json(filepath, product_id=None):
    with open(filepath, 'r') as f:
        data = json.load(f)
    if product_id:
        data = [p for p in data if p['id'] == product_id]
    return data

def read_csv(filepath, product_id=None):
    products = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['id'] = int(row['id'])
            row['price'] = float(row['price'])
            products.append(row)
    if product_id:
        products = [p for p in products if p['id'] == product_id]
    return products

def read_sql(product_id=None):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    if product_id:
        cursor.execute('SELECT id, name, category, price FROM Products WHERE id = ?', (product_id,))
    else:
        cursor.execute('SELECT id, name, category, price FROM Products')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "category": r[2], "price": r[3]} for r in rows]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/products')
def products():
    source = request.args.get('source')
    product_id = request.args.get('id', type=int)

    if source == 'json':
        data = read_json('products.json', product_id)
    elif source == 'csv':
        data = read_csv('products.csv', product_id)
    elif source == 'sql':
        data = read_sql(product_id)
    else:
        return render_template('product_display.html', error="Wrong source")

    if product_id and not data:
        return render_template('product_display.html', error="Product not found")

    return render_template('product_display.html', products=data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)