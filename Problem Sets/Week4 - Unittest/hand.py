# create the Hand with an initial set of cards
from cards import *
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

