import requests
import random
from tkinter import *
global outcome, label, Label, number, cards, value, value1, score, score2
root = Tk()
root.attributes('-fullscreen', True)
score = 0
root.title("Black Jack")
e = Entry(root, width=50, bg='red', borderwidth=10)
e.pack()

def myClick():
    name = e.get()
    response = requests.post(BASE + 'new/' + name)
    response  = response.json()
    print(response)
def new():
    global outcome, label, Label, number, cards, value, score2
    label.forget()
    label.update()
    number = random.randint(2, 21)
    number = str(number)
    response = requests.get(BASE + 'cards/' + number)
    response  = response.json()
    cards = 'Your cards are the ' + response['cards'][0] + ' of ' + response['suits'][0] + ' and the ' + response['cards'][1] + ' of ' + response['suits'][1]
    value = response['value'][0] + response['value'][1]
    label = Label(root, text=cards)
    label.pack()
def dealer():
    global outcome, label, Label, number, cards, value1, value, score, score2
    name = e.get()
    label.forget()
    label.update()
    number = random.randint(2, 21)
    number = str(number)
    response = requests.get(BASE + 'cards/' + number)
    response  = response.json()
    cards = 'The dealers cards are the ' + response['cards'][0] + ' of ' + response['suits'][0] + ' and the ' + response['cards'][1] + ' of ' + response['suits'][1]
    value1 = response['value'][0] + response['value'][1]
    while True:
        response = requests.get(BASE + 'card/' + number)
        response  = response.json()
        value1 = value1 + response['value']
        if value1 == 21:
            label = Label(root, text='You Loose The Dealer Had Black Jack')
            label.pack()
            break
        elif value1 > 21:
            label = Label(root, text='You Win The Dealer Went Bust')
            label.pack()
            score = score + 1
            
            response = requests.post(BASE + 'score/' + name + '/' + str(score))
            score1 = 'score = ' + str(score)
            print(score1)
            score2.forget()
            score2 = Label(root, text=score1)
            score2.pack()
            score2.update()
            break
        elif value1 >= value:
            cards = 'You loose ' + cards
            label = Label(root, text=cards)
            label.pack()
            break
        else:
            cards = cards + ' ' + response['card'] + ' of ' + response['suit']
            value = value + response['value']
def extraCard():
    global outcome, label, Label, number, cards, value, score
    name = e.get()
    label.forget()
    label.update()
    print(cards)
    number = '5'
    response = requests.get(BASE + 'card/' + number)
    response  = response.json()
    cards = cards + ' ' + response['card'] + ' of ' + response['suit']
    value = value + response['value']
    if value == 21:
        label = Label(root, text='Black Jack')
        label.pack()
        score = score + 1
        response = requests.post(BASE + 'score/' + name + '/' + str(score))
        score1 = 'score = ' + str(score)
        score2.forget()
        score2 = Label(root, text=score1)
        score2.pack()
        score2.update()
    elif value > 21:
        label = Label(root, text='You Went Bust')
        label.pack()
    else:
        label = Label(root, text=cards)
        label.pack()
myButton = Button(root, text='Submit', command=myClick)
myButton.pack()
extraCard = Button(root, text='Extra Card', command=extraCard, background='red')
extraCard.pack()
dealer = Button(root, text='See Dealers Cards', command=dealer, background='red')
dealer.pack()
new = Button(root, text='New Game', command=new, background='red')
new.pack()
BASE = 'http://127.0.0.1:5000/'
number = random.randint(2, 21)
number = str(number)
response = requests.get(BASE + 'cards/' + number)
response  = response.json()
cards = 'Your cards are the ' + response['cards'][0] + ' of ' + response['suits'][0] + ' and the ' + response['cards'][1] + ' of ' + response['suits'][1]
value = response['value'][0] + response['value'][1]
score1 = 'score = ' + str(score)
print(score1)
score2 = Label(root, text=score1)
score2.pack()
label = Label(root, text=cards)
label.pack()
root.configure(background='green')
root.mainloop()    
