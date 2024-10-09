import random
import unittest

VERSION = 0.01
 
class Card:
    '''a standard playing card
    cards will have a suit and a rank
    Class Attributes
    ----------------
    suit_names: list
        the four suit names in order 
        0:Diamonds, 1:Clubs, 2: Hearts, 3: Spades
    
    faces: dict
        maps face cards' rank name
        1:Ace, 11:Jack, 12:Queen,  13:King
    Instance Attributes
    -------------------
    suit: int
        the numerical index into the suit_names list
    suit_name: string
        the name of the card's suit
    rank: int
        the numerical rank of the card
    rank_name: string
        the name of the card's rank (e.g., "King" or "3")
    '''
    suit_names = ["Diamonds","Clubs","Hearts","Spades"]
    faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}
 

    def __init__(self, suit=0,rank=2):
        self.suit = suit
        self.suit_name = Card.suit_names[self.suit]

        self.rank = rank
        if self.rank in Card.faces:
            self.rank_name = Card.faces[self.rank]
        else:
            self.rank_name = str(self.rank)
 
    def __str__(self):
        return f"{self.rank_name} of {self.suit_name}"
 

class Hand:
    '''a hand for playing card '''


    def __init__(self, init_cards) -> None:

        
        '''

        init the hand instance

        Parameters
        -------------------
        init_cards: a list of card instance
        the instance should be created using the card class in card.py

        
        Attributes
        -------------------
        cards: list
        use the init_cards to create self.cards
        a list of cards instance, indicating the cards in the hand
        

        '''
        self.cards = init_cards


    def add_card(self, card) -> None:

        '''
        
        add a card to hand
        silently fails if the card is already in the hand
        assuming there is only one deck with 52 cards (except jokers)
        two different cards instance with the same rank and suit are 
        regarded as one card
        
        for example:
            card1 = Card(suit=0,rank=2)
            card2 = Card(suit=0,rank=2)
            card1 and card2 are regarded as the same card

        Parameters
        -------------------
        card: card instance
        a card to add

        Returns
        -------
        None

        ''' 
        for own_card in self.cards:
            if own_card.rank == card.rank and own_card.suit == card.suit:
                return None
        self.cards.append(card)


    def remove_card(self, card)-> Card | None:
        '''

        remove a card from the hand

        Parameters
        -------------------
        card: card instance
        a card to remove

        Returns
        -------
        the removed card instance, or None if the card was not in the Hand

        '''
        for own_card in self.cards:
            if own_card.rank == card.rank and own_card.suit == card.suit:
                self.cards.remove(own_card)
                return own_card
        return None

    def draw(self, deck) -> None:
        '''

        draw a card from a deck and add it to the hand
        side effect: the deck will be depleted by one card

        Parameters
        -------------------
        deck: deck instance
        a deck from which to draw
        
        Returns
        -------
        None

        '''
        self.add_card(deck.deal_card())
    
    def remove_pairs(self) -> None:
        '''

        remove all the pairs in the hand
        this method is for extra credit 2
        
        Parameters
        -------------------
        None
        
        Returns
        -------
        None

        '''
        card_count = {}
        for card in self.cards:
            if card_count.get(card.rank) == None:
                card_count[card.rank] = 1
            else:
                card_count[card.rank] = card_count.get(card.rank) + 1
        
        for rank, count in card_count.items():
            if count == 2:
                card_remove = [card for card in self.cards if card.rank == rank]
            if count == 3:
                card_remove = [card for card in self.cards if card.rank == rank][:2]
            if count == 4:
                card_remove = [card for card in self.cards if card.rank == rank]
            for card in card_remove:
                self.remove_card(card)
        return None

class Deck:
    '''a deck of Cards
    Instance Attributes
    -------------------
    cards: list
        the list of Cards currently in the Deck. Initialized to contain
        all 52 cards in a standard deck
    '''

    def __init__(self): 

        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card) # appends in a sorted order
 
    def deal_card(self, i=-1):
        '''remove a card from the Deck
        Parameters  
        -------------------
        i: int (optional)
            the index of the ard to remove. Default (-1) will remove the "top" card
        Returns
        -------
        Card
            the Card that was removed
        '''
        return self.cards.pop(i) 
 
    def shuffle(self):
        '''shuffles (randomizes the order) of the Cards
        self.cards is modified in place
        Parameters  
        ----------
        None
        Returns
        -------
        None
        '''
        random.shuffle(self.cards)
 
    def replace_card(self, card):
        card_strs = [] # forming an empty list
        for c in self.cards: # each card in self.cards (the initial list)
            card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
        if card.__str__() not in card_strs: # if the string representing this card is not in the list already
            self.cards.append(card) # append it to the list
    
    def sort_cards(self):
        '''returns the Deck to its original order
        
        Cards will be in the same order as when Deck was constructed.
        self.cards is modified in place.
        Parameters  
        ----------
        None
        Returns
        -------
        None
        '''
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                card = Card(suit,rank)
                self.cards.append(card)
 
    def deal_hand(self, hand_size):
        '''removes and returns hand_size cards from the Deck
        
        self.cards is modified in place. Deck size will be reduced
        by hand_size
        Parameters  
        -------------------
        hand_size: int
            the number of cards to deal
        Returns
        -------
        list
            the top hand_size cards from the Deck
        '''
        hand_cards = []
        for i in range(hand_size):
            hand_cards.append(self.deal_card())
        return hand_cards
    
    def deal(self, numHand: int, numCard: int = -1) -> list:
        '''Deal cards to a given number of hands and cards per hand.
        
        Parameters
        -----------
        numHand: int
            The number of hands to deal.
        numCard: int
            The number of cards per hand. The default is -1, which means all cards are dealt.
        
        Returns
        --------
        list
            A list of hands with the given number of cards.
        '''
        self.shuffle()
        hands = []
        if numCard == -1:
            numCard = len(self.cards) // numHand
        for _ in range(numHand):
            if len(self.cards) >= numCard:
                hands.append(self.deal_hand(numCard))
            else:
                hands.append(self.deal_hand(len(self.cards)))
        return hands
        


def print_hand(hand):
    '''prints a hand in a compact form
    
    Parameters  
    -------------------
    hand: list
        list of Cards to print
    Returns
    -------
    none
    '''
    hand_str = '/ '
    for c in hand:
        s = c.suit_name[0]
        r = c.rank_name[0]
        hand_str += r + "of" + s + ' / '
    print(hand_str)

