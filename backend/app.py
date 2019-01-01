from flask import Flask
from extensions import jwt, ma, db
from views.auth import auth_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_dirty_little_secret' #os.environ.get('SECRET_KEY')

db.init_app(app)
jwt.init_app(app)
ma.init_app(app)

app.register_blueprint(auth_blueprint)

@app.route('/', methods=['GET'])
def index():
    return 'hello cfp!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
