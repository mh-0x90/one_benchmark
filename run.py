from app import create_app, db
from app.database.seed_data import create_test_data

app = create_app()

with app.app_context():
    db.create_all()
    create_test_data()

if __name__ == '__main__':
    app.run(debug=True)
