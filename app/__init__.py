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
    login_manager.login_view = 'tech_001_sq_s.login'

    from app.database.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.technical import tech_001_sq, tech_002_xs, tech_003_id, tech_004_cs, tech_005_sr, tech_006_fu, tech_007_sh
    from app.routes.business_logic import user_lookup, promo_codes, user_credits, verification, order_mgnt, cart_pricing, stock_mgnt, refunds, user_roles, vendor_pmts
    from app.routes.technical import tech_001_sq_s, tech_002_xs_s, tech_003_id_s, tech_004_cs_s, tech_006_fu_s, tech_005_sr_s, tech_007_sh_s

    app.register_blueprint(tech_001_sq.bp)
    app.register_blueprint(tech_002_xs.bp)
    app.register_blueprint(tech_003_id.bp)
    app.register_blueprint(tech_004_cs.bp)
    app.register_blueprint(tech_005_sr.bp)
    app.register_blueprint(tech_006_fu.bp)
    app.register_blueprint(tech_007_sh.bp)
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
    app.register_blueprint(tech_001_sq_s.bp)
    app.register_blueprint(tech_002_xs_s.bp)
    app.register_blueprint(tech_003_id_s.bp)
    app.register_blueprint(tech_004_cs_s.bp)
    app.register_blueprint(tech_006_fu_s.bp)
    app.register_blueprint(tech_005_sr_s.bp)
    app.register_blueprint(tech_007_sh_s.bp)

    return app
