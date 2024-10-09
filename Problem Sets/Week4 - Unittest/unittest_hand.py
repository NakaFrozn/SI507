from unittest import TestCase
from cards import *
from hand import *

class TestHand(TestCase):
    def setUp(self):
        self.deck = Deck()
        self.hand = Hand([])

    def testInit(self):
        self.assertIsInstance(self.hand, Hand) # check the initialization of Hand
        self.assertEqual(self.hand.cards, []) # check if the cards is an empty list
        self.assertIsInstance(self.deck, Deck) # check if the deck is an instance of Deck

    def testAddAndRemoveCard(self):
        card1 = Card(0, 2)
        card2 = Card(1, 2)
        card3 = Card(2, 2)
        card4 = Card(0, 2)
        self.hand.add_card(card1)
        self.hand.add_card(card2)
        self.assertEqual(self.hand.cards, [card1, card2]) # check if cards are correctly added
        self.assertEqual(self.hand.remove_card(card2), card2) # check if card is correctly removed
        self.assertEqual(self.hand.cards, [card1]) # double check if card is correctly removed
        self.assertEqual(self.hand.remove_card(card3), None) # check if non-existent card is not removed
        self.hand.add_card(card4) 
        self.assertEqual(self.hand.cards, [card1]) # check if duplicate card is not added
        
    def testDraw(self):
        self.hand.draw(self.deck) 
        self.assertEqual(len(self.hand.cards), 1) # check if hand has one card
        self.hand.draw(self.deck) 
        self.assertEqual(len(self.hand.cards), 2) # check if hand has two cards
        card1 = self.hand.remove_card(self.hand.cards[0]) 
        self.assertEqual(card1.rank, 13) # check the popped card is correct
        self.assertEqual(card1.suit, 3)
        card2 = self.hand.remove_card(self.hand.cards[0])
        self.assertEqual(card2.rank, 12) # check another popped card is correct
        self.assertEqual(card2.suit, 3)
