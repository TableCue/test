from flask import Flask, render_template, request
from models import db, Reservation
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/restaurant/<restroname>/reserve', methods=['GET', 'POST'])
def reserve(restroname):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        people = request.form['people']
        special = request.form.get('requests', '')

        reservation = Reservation(
            restaurant=restroname,
            name=name,
            phone=phone,
            people=int(people),
            special_requests=special
        )
        db.session.add(reservation)
        db.session.commit()

        return f"<h3>Thanks {name}! Your table at <b>{restroname}</b> is reserved.</h3>"

    return render_template("reserve_form.html", restroname=restroname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
