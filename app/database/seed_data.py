from app import db
from app.database.models import User, Post, Comment, Invoice, Product, Coupon, Order, Vendor

def create_test_data():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Seed data from agents.md
    users = [
        {"id": 1, "email": "alice@example.com", "password": "password123", "role": "user", "balance": 1000.0},
        {"id": 2, "email": "bob@example.com", "password": "hunter2", "role": "user", "balance": 10.0},
        {"id": 3, "email": "admin@example.com", "password": "admin123", "role": "admin"}
    ]
    for user_data in users:
        if not User.query.get(user_data['id']):
            user = User(**user_data)
            db.session.add(user)

    posts = [
        {"id": 100, "title": "Welcome", "comments": []}
    ]
    for post_data in posts:
        if not Post.query.get(post_data['id']):
            post = Post(id=post_data['id'], title=post_data['title'])
            db.session.add(post)

    invoices = [
        {"id": 9001, "owner_user_id": 1, "amount": 499.99},
        {"id": 9002, "owner_user_id": 2, "amount": 29.99}
    ]
    for invoice_data in invoices:
        if not Invoice.query.get(invoice_data['id']):
            invoice = Invoice(**invoice_data)
            db.session.add(invoice)

    products = [
        {"id": 10, "name": "Pro Plan", "price": 199.00}
    ]
    for product_data in products:
        if not Product.query.get(product_data['id']):
            product = Product(**product_data)
            db.session.add(product)

    coupons = [
        {"code": "WELCOME10", "discount_percent": 10},
        {"code": "BLACKFRI50", "discount_percent": 50}
    ]
    for coupon_data in coupons:
        if not Coupon.query.filter_by(code=coupon_data['code']).first():
            coupon = Coupon(**coupon_data)
            db.session.add(coupon)

    orders = [
        {"id": 5001, "user_id": 1, "total": 199.00, "status": "paid", "refunded_amount": 0.0}
    ]
    for order_data in orders:
        if not Order.query.get(order_data['id']):
            order = Order(**order_data)
            db.session.add(order)
            
    vendors = [
        {"id": 77, "name": "Acme Supplies", "balance": 0}
    ]
    for vendor_data in vendors:
        if not Vendor.query.get(vendor_data['id']):
            vendor = Vendor(**vendor_data)
            db.session.add(vendor)

    db.session.commit()
