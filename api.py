from flask import Flask, session
from flask_restful import Api, Resource
import sqlite3
import random
global suits, ten, connection, cursor
connection = sqlite3.connect('score.db', check_same_thread=False)
cursor = connection.cursor()
try:
    cursor.execute("CREATE TABLE  scoring (name text, scores integer)")
    connection.commit()
    
except:
    print('Table already created')
app = Flask(__name__)
api = Api(app)


suits = ['hearts', 'diamonds', 'clubs', 'spades']
ten = ['jack', 'queen', 'king']
class score(Resource):
    def post(self, name1, score1):
        try:
            cursor.execute("INSERT INTO scoring VALUES ('(name1)', '(score1)')")
            connection.commit()
            connection.close()
            print(' Great Sucsess')
        except:
            print('failure')

class new(Resource):
    def post(self, name1):
        global  connection, cursor

        
        cursor.execute("INSERT INTO scoring VALUES ('(name1)', '0')")
        connection.commit()
    
        print('Great Sucsess')
        
class cards(Resource):
    def get(self, number):
        if number < 10:
            Type = 'low'
        else:
            Type = 'high'
        card1 = None
        card1_num = None
        card2 = None
        suit = random.randint(0,3)
        suit1 = suits[suit]
        suit = random.randint(0,3)
        suit2 = suits[suit]
        if Type == 'low':
            card = random.randint(1,5)
            if card == 1:
                card1_num = 1
                card1 = 'ace'
            else:
                card1_num = card
                card1 = str(card)
        else:
            card = random.randint(6,10)
            if card == 10:
                card1_num = 10
                tens = random.randint(0,2)
                card1 = ten[tens] 
            else:
                card1_num = card
                card1 = str(card)
        card2 = number - card1_num
        if card2 > 10:
            card2 = 10
        elif card2 < 1:
            card2 = 1
        card2_num = card2
        if card2 == 1:
            card2 = 'ace'
        elif card2 == 10:
            tens = random.randint(0,2)
            card2 = ten[tens]
        else:
            card2 = str(card2)
        cards = [card1, card2]
        suit = [suit1, suit2]
        value = [card1_num, card2_num]
        return {'cards': cards, 'suits': suit, 'value': value}
    
class card(Resource):
    def get(self, number):
        if number > 10:
            number = 10
        elif number < 1:
            number = 1
        if number == 1:
            card = 'ace'
        elif number == 10:
            tens = random.randint(0,2)
            card = ten[tens]
        else:
            card = str(number)
        suit = random.randint(0,3)
        suit = suits[suit]
        return {'card': card, 'suit': suit, 'value': number}
api.add_resource(cards, '/cards/<int:number>')
api.add_resource(card, '/card/<int:number>')
api.add_resource(score, '/score/<string:name1>/<int:score1>')
api.add_resource(new, '/new/<string:name1>')
if __name__  == "__main__":
    app.run(use_reloader=False, debug=False)
