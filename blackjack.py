# Mini-project #6 - Blackjack a.k.a "Sorry if my BlackJack logo caused your eyes to melt"

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        out = ""
        for card in range(len(self.card_list)):
            out += str(self.card_list[card])+" "
        return "Hand contains " + out
    
    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        for n in self.card_list:
            if n.rank != 'A':
                value += VALUES[n.rank]
            else:
                if value + 10 <= 21:
                    value += VALUES[n.rank] + 10
                else:
                    value += VALUES[n.rank]
        return value
           
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.card_list:
            card.draw(canvas,pos)
            pos[0] += 105
        
# define deck class 
class Deck:
    def __init__(self):
        self.card_list = []
        for rank in RANKS:
            for suit in SUITS:
                self.card_list.append(Card(suit,rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)

    def deal_card(self):
        # deal a card object from the deck
        return random.choice(self.card_list)
    def __str__(self):
        out = ""
        for card in range(len(self.card_list)):
            out += str(self.card_list[card]) + " "
        return "Deck contains "+out

#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer, current_deck, locked,score
    # your code goes here
    outcome = "Hit or stand?"
    current_deck = Deck()
    current_deck.shuffle()
    player = Hand()
    dealer = Hand()
    player.add_card(current_deck.deal_card())
    player.add_card(current_deck.deal_card())
    dealer.add_card(current_deck.deal_card())
    dealer.add_card(current_deck.deal_card())
    #print "player's cards:",player," . Value: ",player.get_value(),"\n","dealer's cards:",dealer," . Value: ",dealer.get_value()
    if in_play:
        score -= 1
    in_play = True
    locked = False
    
    
def hit():
    # replace with your code below
    global player, dealer, current_deck,outcome, locked
    # if the hand is in play, hit the player
    if not locked:
        if player.get_value() <= 21:
            player.add_card(current_deck.deal_card())
        else:
            outcome = "You're busted! New deal?"
        
        # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global player, dealer, current_deck, outcome, score, in_play, locked
    # replace with your code below
    in_play = False
    if not locked:
        if player.get_value() > 21:
            outcome = "You're busted! New deal?"
            score -= 1
        else:
            while dealer.get_value() <= 17:
                dealer.add_card(current_deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "Dealer's busted! New deal?"
                score += 1
            else:
                if player.get_value() > dealer.get_value():
                    outcome = "Player win! New deal?"
                    score += 1
                else:
                    outcome = "Dealer win! New deal?"
                    score -= 1
        locked = True
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player, dealer
    player.draw(canvas,[50,400])
    dealer.draw(canvas,[50,150])
    color = random.choice(["Red","Green","Blue","Yellow","Orange","Lime","Cyan","Gray","White"])
    canvas.draw_text("BlackJack",(50,50),36,color,"serif")
    canvas.draw_text(outcome,(200,330),24,"White")
    canvas.draw_text("Score : "+str(score),(400,50),36,"White")
    if in_play:
        canvas.draw_image(card_back,CARD_BACK_CENTER,CARD_BACK_SIZE,[50+CARD_BACK_CENTER[0],150+CARD_BACK_CENTER[1]],CARD_BACK_SIZE)
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
