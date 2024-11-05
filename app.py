from flask import Flask, render_template, redirect, url_for, request, jsonify
from models import db, Client
from forms import RegistrationForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.db"
app.config["SECRET_KEY"] = "secret"
db.init_app(app)

@app.route('/')
def index():
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_client = Client(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            location=form.location.data,
            gender=form.gender.data
        )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('client_list'))
    return render_template('register.html', form=form)

@app.route('/clients')
def client_list():
    clients = Client.query.all()
    return render_template('client_list.html', clients=clients)

@app.route('/clients/<int:client_id>')
def client_page(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_page.html', client=client)

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    client = Client(
        full_name=data.get('full_name'),
        email=data.get('email'),
        phone=data.get('phone'),
        location=data.get('location'),
        gender=data.get('gender')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify(client.to_dict()), 201

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080)
