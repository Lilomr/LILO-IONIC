from flask import Flask, request, jsonify, render_template, send_from_directory, redirect
import secrets
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc 
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
import os
import bcrypt
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__, template_folder='templates')
app.secret_key = secrets.token_hex(16) 

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URL')
app.config["SECRET_KEY"] = secrets.token_hex(16)
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True,
                        nullable=False)
    password = db.Column(db.String(250),
                        nullable=False)
class Publicacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('Users', backref=db.backref('publicacoes', lazy=True))


db.init_app(app)
with app.app_context():
    db.app = app
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/login')
def index_login():
    if current_user.is_authenticated:
        return redirect('/page')
    return render_template('login.html')


@app.route('/deslogar')
def logout():
    logout_user()
    return redirect('/login') 


@app.route('/cadastrar')
def index_cadastrar():
    if current_user.is_authenticated:
        return redirect('/page')
    return render_template('index.html')

@app.route('/page')
@login_required
def index_page():
    return render_template('page.html')

@app.route('/')
def index():
    return redirect('/login')

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    senha = data['senha']
    user = Users.query.filter_by(email=email).first()

    if user and bcrypt.checkpw(bytes(senha, 'utf-8'), bytes(user.password, 'utf-8')):

        login_user(user)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Usuário não encontrado'})

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar_usuario():
    data = request.json
    name = data['name']
    email = data['email']
    senha: str = data['senha']
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(senha,'utf-8'), salt)

    try:
        user = Users(nome=name, email=email, password=hashed.decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': True})
    except exc.IntegrityError as e:
        print(e)
        return jsonify({'success': False, 'error': 'email já existe'})
        return jsonify({'success': False, 'error': 'Email já existe'})

@app.route('/api/publicar',methods=['POST'])
def publicar():
    data = request.json
    conteudo = data['conteudo']
    publicacao = Publicacao(conteudo=conteudo, user_id=current_user.id)

    if not conteudo:
        return jsonify({'success': False, 'error': 'Escreva algo'})
    db.session.add(publicacao)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/publicacoes', methods=['GET'])
def get_publicacoes():
    publicacoes = Publicacao.query.order_by(Publicacao.id.desc()).all()

    return jsonify([{'id': p.id, 'conteudo': p.conteudo, 'user': p.user.nome} for p in publicacoes])

@app.route('/api/deletar', methods=['POST'])
def deletar():
    data = request.json
    id = data['id']
    publicacao = Publicacao.query.filter_by(id=id).first()
    if publicacao.user_id == current_user.id:
        db.session.delete(publicacao)
        db.session.commit()
        return jsonify({'success': True})
    else: 
        return jsonify({'success': False, 'error': 'Você não pode deletar essa publicação'})



if __name__ == '__main__':
    app.run(debug=True)