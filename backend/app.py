from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import desc
from datetime import datetime
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
    avatar_url = db.Column(db.String(255), nullable=True, unique=False, default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcThQ_mJzFSBReUZorw2OFBccmXNjdsfzleL1Q5JuoNKMA&s")

    def json(self):
        return{'id': self.id, 'discord_name': self.discord_name, 'bankroll': self.bankroll, 'avatar_url': self.avatar_url}

class Tournament(db.Model):
    __tablename__ = 'tournaments'
    id = db.Column(db.Integer, primary_key=True)
    stake = db.Column(db.Integer, nullable=False, default=0)
    payout = db.Column(db.Integer, nullable=True, default=0)
    first = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    second = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    third = db.Column(db.BigInteger, db.ForeignKey('users.discord_id'), nullable=True)
    ongoing = db.Column(db.Boolean, nullable=False, default="True")
    start_time = db.Column(db.DateTime, default=datetime.now)

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

    users.append(User(discord_id=84205293101154304, discord_name='stef_.'))
    users.append(User(discord_id=89918396170268672, discord_name='n1d'))
    users.append(User(discord_id=189043397489721345, discord_name='aven5187'))
    users.append(User(discord_id=150297317658984448, discord_name='denya9'))
    users.append(User(discord_id=799796051157975090, discord_name='dnd.gaw'))
    users.append(User(discord_id=572499409661853698, discord_name='babushka_frosia'))
    db.session.add_all(users)
    db.session.commit()

    tournaments.append(Tournament(stake=20, payout=300, first=799796051157975090, second=150297317658984448, third=572499409661853698, ongoing=False))
    tournaments.append(Tournament(stake=10, payout=100, first=89918396170268672, second=150297317658984448, third=84205293101154304, ongoing=False))

    db.session.add_all(tournaments)
    db.session.commit()
    
    participants.append(Participant(discord_id=84205293101154304, discord_name='stef_.', tournament_id=1, rebuy_amt=0))
    participants.append(Participant(discord_id=89918396170268672, discord_name='n1d', tournament_id=1, rebuy_amt=1))
    participants.append(Participant(discord_id=189043397489721345, discord_name='aven5187', tournament_id=1, rebuy_amt=0))
    participants.append(Participant(discord_id=150297317658984448, discord_name='denya9', tournament_id=1, rebuy_amt=2))
    participants.append(Participant(discord_id=799796051157975090, discord_name='dnd.gaw', tournament_id=1, rebuy_amt=5))
    participants.append(Participant(discord_id=572499409661853698, discord_name='babushka_frosia', tournament_id=1, rebuy_amt=1))

    participants.append(Participant(discord_id=84205293101154304, discord_name='stef_.', tournament_id=2, rebuy_amt=0))
    participants.append(Participant(discord_id=89918396170268672, discord_name='n1d', tournament_id=2, rebuy_amt=1))
    participants.append(Participant(discord_id=189043397489721345, discord_name='aven5187', tournament_id=2, rebuy_amt=0))
    participants.append(Participant(discord_id=150297317658984448, discord_name='denya9', tournament_id=2, rebuy_amt=2))
    participants.append(Participant(discord_id=799796051157975090, discord_name='dnd.gaw', tournament_id=2, rebuy_amt=1))
    participants.append(Participant(discord_id=572499409661853698, discord_name='babushka_frosia', tournament_id=2, rebuy_amt=0))

    db.session.add_all(participants)
    db.session.commit()

# Route for getting user information (Members Page)
@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.discord_id, 'username': user.discord_name, 'bankroll': user.bankroll, 'avatar_url': user.avatar_url} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
    
# Route for getting all tournaments and a list of their participants (tournaments page)
@app.route('/api/flask/tournaments', methods=['GET'])
def get_tournaments_and_participants():
    try:
        tournaments = Tournament.query.order_by(desc(Tournament.start_time)).all()
        tournaments_data = []
        for tournament in tournaments:
            participants_data = []
            participants = Participant.query.filter_by(tournament_id=tournament.id).all()
            for participant in participants:
                user = User.query.filter_by(discord_id=participant.discord_id).first()
                participants_data.append({
                    'id': participant.id,
                    'username': user.discord_name,
                    'bankroll': user.bankroll,
                    'avatar_url': user.avatar_url,
                    'rebuy_amt': participant.rebuy_amt
                })
            
            tournaments_data.append({
                'id': tournament.id,
                'stake': tournament.stake,
                'payout': tournament.payout,
                'start_time' : tournament.start_time,
                'participants': participants_data,
            })
                
        return jsonify(tournaments_data), 200
    except Exception as e:
        return make_response(jsonify({'message': 'error getting tournaments', 'error': str(e)}), 500)

# Home route API call for recent tournament podium
@app.route('/api/flask/most_recent_tournament_with_users', methods=['GET'])
def get_most_recent_tournament_with_users():
    try:
        # Query the most recent tournament entry based on start_time
        most_recent_tournament = Tournament.query.order_by(Tournament.start_time.desc()).first()
        
        # Check if there's any tournament entry
        if most_recent_tournament:
            # Get user information for the tournament entries
            first_user = User.query.filter_by(discord_id=most_recent_tournament.first).first()
            second_user = User.query.filter_by(discord_id=most_recent_tournament.second).first()
            third_user = User.query.filter_by(discord_id=most_recent_tournament.third).first()
            
            tournament_data = {
                'id': most_recent_tournament.id,
                'stake': most_recent_tournament.stake,
                'payout': most_recent_tournament.payout,
                'first': {
                    'discord_id': first_user.discord_id,
                    'discord_name': first_user.discord_name,
                    'bankroll': first_user.bankroll,
                    'avatar_url': first_user.avatar_url
                } if first_user else None,
                'second': {
                    'discord_id': second_user.discord_id,
                    'discord_name': second_user.discord_name,
                    'bankroll': second_user.bankroll,
                    'avatar_url': second_user.avatar_url
                } if second_user else None,
                'third': {
                    'discord_id': third_user.discord_id,
                    'discord_name': third_user.discord_name,
                    'bankroll': third_user.bankroll,
                    'avatar_url': third_user.avatar_url
                } if third_user else None,
                'ongoing': most_recent_tournament.ongoing,
                'start_time': most_recent_tournament.start_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            return jsonify(tournament_data), 200
        else:
            return jsonify({'message': 'No tournament entries found'}), 404
    except Exception as e:
        return make_response(jsonify({'message': 'Error getting most recent tournament with users', 'error': str(e)}), 500)

# Test route
@app.route('/api/flask/test', methods=['GET'])
def test():
    return jsonify({'message': 'the server is running'})
      

# Test route
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
