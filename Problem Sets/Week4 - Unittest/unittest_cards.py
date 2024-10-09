import unittest
import cards
from typing import Type

class TestCard(unittest.TestCase):

    def test_construct_Card(self) -> None:
        c1 = cards.Card(0, 2)
        c2 = cards.Card(1, 1)

        self.assertEqual(c1.suit, 0)
        self.assertEqual(c1.suit_name, "Diamonds")
        self.assertEqual(c1.rank, 2)
        self.assertEqual(c1.rank_name, "2")

        self.assertIsInstance(c1.suit, int)
        self.assertIsInstance(c1.suit_name, str)
        self.assertIsInstance(c1.rank, int)
        self.assertIsInstance(c1.rank_name, str)

        self.assertEqual(c2.suit, 1)
        self.assertEqual(c2.suit_name, "Clubs")
        self.assertEqual(c2.rank, 1)
        self.assertEqual(c2.rank_name, "Ace")
        
    def test_q1(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 1:
        Test that if you create a card with rank 12, its rank_name will be "Queen"
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        card_q1 = cards.Card(rank=12)
        self.assertEqual(card_q1.rank_name, "Queen")
        X, Y = card_q1.rank_name, "Queen"
        return X, Y
    
    def test_q2(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 1:
        Test that if you create a card instance with suit 1, its suit_name will be "Clubs"
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        card_q2 = cards.Card(suit=1)
        self.assertEqual(card_q2.suit_name, "Clubs")
        X, Y = card_q2.suit_name, "Clubs"
        return X, Y    

    def test_q3(self) -> tuple[str, str]:
        '''
        1. fill in your test method for question 3:
        Test that if you invoke the __str__ method of a card instance that is created with suit=3, rank=13, it returns the string "King of Spades"

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        card_q3 = cards.Card(suit=3, rank=13)
        self.assertEqual(str(card_q3), "King of Spades")
        X, Y = str(card_q3), "King of Spades"
        return X, Y
    
    def test_q4(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 4:
        Test that if you create a eck instance, it will have 52 cards in its cards instance variable
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        test_q4 = cards.Deck()
        self.assertEqual(len(test_q4.cards), 52)
        X, Y = len(test_q4.cards), 52
        return X, Y  

    def test_q5(self) -> tuple[cards.Card, Type[cards.Card]]:
        '''
        1. fill in your test method for question 5:
        Test that if you invoke the deal_card method on a deck, it will return a card instance.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        card_q5 = cards.Deck().deal_card()
        self.assertIsInstance(card_q5, cards.Card)
        X, Y = card_q5, cards.Card
        return X, Y
    
    def test_q6(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 6:
        
        Test that if you invoke the deal_card method on a deck, the deck has one fewer cards in it afterwards.
        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        deck_q6 = cards.Deck()
        deck_q6.deal_card()
        self.assertEqual(len(deck_q6.cards), 51)
        X, Y = len(deck_q6.cards), 51
        return X, Y    
    

    def test_q7(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 7:
        Test that if you invoke the replace_card method, the deck has one more card in it afterwards. (Please note that you want to use deal_card function first to remove a card from the deck and then add the same card back in)

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        deck_q7 = cards.Deck()
        card_q7 = deck_q7.deal_card()
        deck_q7.replace_card(card_q7)
        self.assertEqual(len(deck_q7.cards), 52)
        X, Y = len(deck_q7.cards), 52
        return X, Y
    
    def test_q8(self) -> tuple[int, int]:
        '''
        1. fill in your test method for question 8:
        Test that if you invoke the replace_card method with a card that is already in the deck, the deck size is not affected.(The function must silently ignore it if you try to add a card that’s already in the deck)

        
        2. remove the pass command
        
        3. uncomment the return command and 
        3b. change X, Y to the values from your assert statement
        ### please note: normally unit test methods do not have return statements. But returning will allow for unit testing of your unit test, and allow you to check your answer with the autograder.  This is optional today.

        '''
        deck_q8 = cards.Deck()
        card_q8 = deck_q8.deal_card()
        deck_q8.replace_card(card_q8)
        deck_q8.replace_card(card_q8)
        self.assertEqual(len(deck_q8.cards), 52)
        X, Y = len(deck_q8.cards), 52
        return X, Y  



if __name__=="__main__":
    unittest.main()