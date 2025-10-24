from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'supersecretkey'

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'sq_user.login'

    from app.database.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.showcase import sq, xs, id, cs, sr, fu, sh, signup
    from app.routes.product_management import user_lookup, promo_codes, user_credits, verification, order_mgnt, cart_pricing, stock_mgnt, refunds, user_roles, vendor_pmts
    from app.routes.showcase import sq_user, xs_user, id_user, cs_user, fu_user, sr_user, sh_user

    app.register_blueprint(sq.bp)
    app.register_blueprint(xs.bp)
    app.register_blueprint(id.bp)
    app.register_blueprint(cs.bp)
    app.register_blueprint(sr.bp)
    app.register_blueprint(fu.bp)
    app.register_blueprint(sh.bp)
    app.register_blueprint(signup.bp)
    app.register_blueprint(user_lookup.bp)
    app.register_blueprint(promo_codes.bp)
    app.register_blueprint(user_credits.bp)
    app.register_blueprint(verification.bp)
    app.register_blueprint(order_mgnt.bp)
    app.register_blueprint(cart_pricing.bp)
    app.register_blueprint(stock_mgnt.bp)
    app.register_blueprint(refunds.bp)
    app.register_blueprint(user_roles.bp)
    app.register_blueprint(vendor_pmts.bp)

    # Register secure blueprints
    app.register_blueprint(sq_user.bp)
    app.register_blueprint(xs_user.bp)
    app.register_blueprint(id_user.bp)
    app.register_blueprint(cs_user.bp)
    app.register_blueprint(fu_user.bp)
    app.register_blueprint(sr_user.bp)
    app.register_blueprint(sh_user.bp)

    return app
