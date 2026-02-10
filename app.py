from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

products = [
    {"id": 1, "name": "Upcycled Denim Bag", "price": 499, "image": "bag.jpg"},
    {"id": 2, "name": "Patchwork Cushion Cover", "price": 299, "image": "cushion.jpg"},
    {"id": 3, "name": "T-Shirt Tote Bag", "price": 199, "image": "tote.jpg"}
]

cart = []

@app.route("/")
def home():
    return render_template("index.html", products=products)

@app.route("/add/<int:id>")
def add_to_cart(id):
    for p in products:
        if p["id"] == id:
            cart.append(p)
    return redirect(url_for("cart_page"))

@app.route("/cart")
def cart_page():
    return render_template("cart.html", cart=cart)

@app.route("/checkout", methods=["POST"])
def checkout():
    cart.clear()
    return "<h2>Order placed successfully 🌱</h2>"

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
