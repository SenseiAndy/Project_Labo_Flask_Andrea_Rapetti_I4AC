
from flask import Blueprint
from flask import render_template
from models.model import User
from models.connection import db
from flask import jsonify
from flask import request
from flask import url_for
from flask import redirect
from models.model import Umore
from models.model import Frase
import random
from flask import flash

app = Blueprint('default', __name__)

@app.route('/')
def home():
    #return url_for('hello_guest')
    return render_template('hello.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/emotions', methods=['GET', 'POST'])
def emotions_display():
    if request.method == 'POST':
        emotion_id = request.form.get('existing_emotion')
        user_id = request.form.get('user_id')

        user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        emotion = db.session.execute(db.select(Umore).filter_by(id=emotion_id)).scalar_one_or_none()

        if user and emotion:
            user.umore = emotion
            db.session.commit()
            return redirect(url_for('default.show_solution', emotion_name=emotion.stato))

    emotions = Umore.query.all()
    return render_template('home.html', emotions=emotions)



import random

@app.route('/solution/<string:emotion_name>')
def show_solution(emotion_name):
    emotion = db.session.execute(db.select(Umore).filter_by(stato=emotion_name)).scalar_one_or_none()

    if not emotion:
        return jsonify({'error': 'Emotion not found'}), 404

    phrases = emotion.frasi  # Access related phrases via backref
    random_phrase = random.choice(phrases).frase if phrases else "No phrase available for this emotion."

    return render_template('solution.html', emotion_name=emotion_name, phrase=random_phrase)


@app.route('/add_emotion', methods=['GET', 'POST'])
def add_emotion():
    if request.method == 'POST':
        stato = request.form.get('stato')
        frase = request.form.get('frase')

        if not stato or not frase:
            flash('Both fields are required.')
            return redirect(url_for('default.add_emotion'))

        existing = db.session.execute(db.select(Umore).filter_by(stato=stato)).scalar_one_or_none()
        if existing:
            flash('Emotion already exists.')
            return redirect(url_for('default.add_emotion'))

        new_emotion = Umore(stato=stato)
        db.session.add(new_emotion)
        db.session.commit()

        new_frase = Frase(frase=frase, umore=new_emotion)
        db.session.add(new_frase)
        db.session.commit()

        return redirect(url_for('default.emotions_display'))

    return render_template('add_emotion.html')


@app.route('/add_phrase', methods=['GET', 'POST'])
def add_phrase():
    if request.method == 'POST':
        emotion_id = request.form.get('emotion_id')
        frase_text = request.form.get('frase')

        emotion = db.session.execute(db.select(Umore).filter_by(id=emotion_id)).scalar_one_or_none()

        if emotion and frase_text:
            new_frase = Frase(frase=frase_text, umore=emotion)
            db.session.add(new_frase)
            db.session.commit()
            return redirect(url_for('default.emotions_display'))

    emotions = Umore.query.all()
    return render_template('add_phrase.html', emotions=emotions)





@app.route('/formdb')
def form_display():
    return render_template('form.html')


### generated with Copilot AI ###
@app.route('/submit', methods=['POST'])
def submit_form():
    # Accept AJAX (application/json) and regular form (application/x-www-form-urlencoded)
    if request.is_json:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

    # Check required fields
    if not username or not email or not password:
        response = {'error': 'All fields are required'}
        return jsonify(response), 400

    # Check if user/email already exists
    if db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none():
        return jsonify({'error': 'Username already exists'}), 400
    if db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none():
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    response = {
        'message': 'User successfully registered',
        'user': new_user.to_dict()
    }
    return jsonify(response), 201


@app.route('/hello')
def hello_guest():
    return render_template('hello.html')


@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)
    
@app.route('/users')
def get_all_users():
    users = User.query.all()

    response = {'users':[]} # JSON con lista vuota

    for user in users:
        response['users'].append(user.to_dict()) # Aggiunge alla lista "users" gli "user"

    return jsonify(response), 200


@app.route('/umori')
def get_all_umori():
    umori = Umore.query.all()

    response = {'umori':[]} # JSON con lista vuota

    for umore in umori:
        response['umori'].append(umore.to_dict()) # Aggiunge alla lista "umori" gli "umore"

    return jsonify(response), 200


@app.route('/frasi')
def get_all_frasi():
    frasi = Frase.query.all()

    response = {'frasi':[]} # JSON con lista vuota

    for frase in frasi:
        response['frasi'].append(frase.to_dict()) # Aggiunge alla lista "frasi" gli "frase"

    return jsonify(response), 200