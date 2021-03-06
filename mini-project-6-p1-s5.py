# Mini-project #6 - Blackjack

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
player_hand=[]
dealer_hand=[]

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
        self.hand = []	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.hand)):
            ans += str(self.hand[i])+" "
        return "Hand contains " + ans	# return a string representation of a hand

    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0
        ans = ""
        for i in range(len(self.hand)):
            ans += str(self.hand[i])+" "
        for card in self.hand:
            value = VALUES[card.get_rank()]
            sum = sum +value
        if "A" in ans:
            if sum +10>21:
                return sum
            else:
                return sum+10
        else:
            return sum
            # compute the value of the hand, see Blackjack video
    def draw(self, canvas, pos):
        i = 0
        for c in self.hand:
            c.draw(canvas,[pos[0]+72*i,pos[1]])
            i+=1
            
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suits in SUITS:
            for ranks in RANKS:
                card = Card(suits,ranks)
                self.deck.append(card)# create a Deck object
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        return self.deck.pop()	# deal a card object from the deck
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck)):
            ans += str(self.deck[i])+" "
        return "Deck contains " + ans
        # return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play,player_hand, dealer_hand,deck
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    outcome = "New Game!"
    # your code goes here
    
    in_play = True

def hit():
        # replace with your code below
    global outcome, in_play,player_hand
    
    if in_play:
        player_hand.add_card(deck.deal_card())
    if player_hand.get_value()<=21 and in_play==True:
        outcome = "Hit or stand"
    elif player_hand.get_value()>21 and in_play==True:
        in_play = False  
        score = player_hand.get_value()
        outcome = "You're busted! Dealer wins!"
        
        
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global outcome, in_play,dealer_hand,player_hand
    in_play = True
    if player_hand.get_value()>21:
        outcome = "Player is busted"
        in_play= False
    while dealer_hand.get_value()<17 and in_play:
        dealer_hand.add_card(deck.deal_card())
        
    if dealer_hand.get_value()>21 and in_play:
        in_play = False
        outcome = "Dealer is busted! Player wins."
        
    else:
        if player_hand.get_value()>dealer_hand.get_value() and in_play:
            outcome = "Player wins!"
            in_play = False
        else:
            outcome = "Dealer wins!"  
            in_play = False
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    
    canvas.draw_polygon([[200, 0], [400, 0], [400, 55], [200, 55]], 3, 'Yellow', 'Black')
    canvas.draw_text("Blackjack", (200, 40), 50, 'White')
    canvas.draw_text(outcome, (250, 500), 20, 'White')
    canvas.draw_text("Player "+"| "+"Score is " + str(player_hand.get_value()), (0, 80), 20, 'White')
    canvas.draw_text("Dealer "+"| "+"Score is " + str(dealer_hand.get_value()), (0, 280), 20, 'White')
    
    player_hand.draw(canvas,[0,100])
    dealer_hand.draw(canvas,[0,300])
    if in_play:
        card_back_loc = (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [0 + CARD_BACK_CENTER[0], 300 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
     


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


# remember to review the gradic rubric
