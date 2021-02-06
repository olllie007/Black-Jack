#for flask and restful api
from flask import Flask, session
from flask_restful import Api, Resource
#for database
import sqlite3
import random
global suits, ten, connection, cursor
#connection setup
connection = sqlite3.connect('score.db', check_same_thread=False)
cursor = connection.cursor()
app = Flask(__name__)
api = Api(app)


suits = ['hearts', 'diamonds', 'clubs', 'spades']
ten = ['jack', 'queen', 'king']
class score(Resource):
    def post(self, name1, score1):
        #when you win a game this will update your score
        global suits, ten, connection, cursor
        connection = sqlite3.connect('score.db')
        cursor = connection.cursor()
        sql = 'INSERT INTO ' + name1 + ' VALUES(?)'
        cursor.execute(sql, [score1])
        connection.commit()
        return {'score': 0}
class new(Resource):
    def post(self, name1):
        #to get the persons score if they dont have an account it will create a table and return 0
        global suits, ten, connection, cursor
        try:
            connection = sqlite3.connect('score.db')
            cursor = connection.cursor()
            sql = "SELECT * FROM " + name1
            cursor.execute(sql)
            items = cursor.fetchall()
            length = len(items)
            length = length - 1
            item = items[length][0]
            print(item)
            return {'score': item}
        except:
            create =  'CREATE TABLE ' + name1 + ' (score text)'
            cursor.execute(create)
            return {'score': 0}
            
class cards(Resource):
    def get(self, number):
        #when you need to get two new cards it will get two new cards adding up to a specific number so it can be rigged
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
        #get a new card to a specific value
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
#restful apis
api.add_resource(cards, '/cards/<int:number>')
api.add_resource(card, '/card/<int:number>')
api.add_resource(score, '/score/<string:name1>/<int:score1>')
api.add_resource(new, '/new/<string:name1>')
if __name__  == "__main__":
    app.run(use_reloader=False, debug=True)
    
