from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.BigInteger, nullable=False, unique=True)
    discord_name = db.Column(db.String(80), nullable=False, unique=True)
    bankroll = db.Column(db.Integer, nullable=True, default=0)

    def json(self):
        return{'id': self.id, 'username': self.username, 'bankroll': self.bankroll}

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    stake = db.Column(db.Integer, nullable=False, default=0)
    payout = db.Column(db.Integer, nullable=True, default=0)
    first = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    second = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    third = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    ongoing = db.Column(db.Boolean, nullable=False, default="True")

    def json(self):
        return{'id': self.id, 'stake': self.stake, 'payout': self.payout, 'first': self.first, 'second': self.second, 'third': self.third}

class Participant(db.Model):
    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    discord_id = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'))
    discord_name = db.Column(db.String(80), db.ForeignKey('users.discord_name'))
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournaments.id'))
    rebuy_amt = db.Column(db.Integer, nullable=True, default=0)

    def json(self):
        return{'id': self.id, 'user_id': self.id, 'tournament_id': self.tournament_id}

with app.app_context():
    db.create_all()

    users = []

    tournaments = []

    participants = []

    users.append(User(discord_id=84205293101154304, discord_name='stef'))
    users.append(User(discord_id=89918396170268672, discord_name='dan'))
    users.append(User(discord_id=189043397489721345, discord_name='alex'))
    users.append(User(discord_id=150297317658984448, discord_name='denya'))
    users.append(User(discord_id=799796051157975090, discord_name='dasik'))
    users.append(User(discord_id=572499409661853698, discord_name='artem'))
    db.session.add_all(users)
    db.session.commit()

    tournaments.append(Tournament(stake=20, payout=300, first=89918396170268672, second=150297317658984448, third=572499409661853698, ongoing=False))
    db.session.add_all(tournaments)
    db.session.commit()
    
    participants.append(Participant(discord_id=84205293101154304, discord_name='stef', tournament_id=1, rebuy_amt=0))
    participants.append(Participant(discord_id=89918396170268672, discord_name='dan', tournament_id=1, rebuy_amt=1))
    participants.append(Participant(discord_id=189043397489721345, discord_name='alex', tournament_id=1, rebuy_amt=0))
    participants.append(Participant(discord_id=150297317658984448, discord_name='denya', tournament_id=1, rebuy_amt=2))
    participants.append(Participant(discord_id=799796051157975090, discord_name='dasik', tournament_id=1, rebuy_amt=5))
    participants.append(Participant(discord_id=572499409661853698, discord_name='artem', tournament_id=1, rebuy_amt=1))
    db.session.add_all(participants)
    db.session.commit()

# with app.app_context():
#     db.create_all()


@app.route('/api/flask/test', methods=['GET'])
def test():
    return jsonify({'message': 'the server is running'})
    
@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.discord_id, 'username': user.discord_name, 'bankroll': user.bankroll} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
    
app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
        return make_response(jsonify({'message':'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message':'error getting user', 'error': str(e)}), 500)

# @app.route('/api/flask/users', methods=['POST'])
# def create_user():
#     try:
#         data = request.get_json()
#         new_user = User(username=data['username'])
#         db.session.add(new_user)
#         db.session.commit()

#         return jsonify({
#             'id': new_user.id,
#             'username': new_user.username,
#             'bankroll': new_user.bankroll
#         }), 201
    
#     except Exception as e:
#         return make_response(jsonify({'message':'error creating user', 'error': str(e)}), 500)


# app.route('/api/flask/users/<id>', methods=['PUT'])
# def update_user_bankroll(id, operation, value):
#     try:
#         user = User.query.filter_by(id=id).first()
#         if user:
#             data = request.get_json()
#             if operation == "add":
#                 user.bankroll = user.bankroll + value
#             elif operation == "subtract":
#                 user.bankroll = user.bankroll - value
#             return make_response(jsonify({'message':'user updated'}), 200)
#         return make_response(jsonify({'message':'user not found', 'error': str(e)}), 404)
#     except Exception as e:
#         return make_response(jsonify({'message':'error getting user', 'error': str(e)}), 500)
