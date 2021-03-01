from time import sleep
import pyinputplus as pyip
from random import shuffle
from collections import namedtuple

Card = namedtuple('Card', ['rank', 'suit'])


class Deck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = '\u2660 \u2666 \u2665 \u2663'.split()

    def __init__(self):
        self._cards = list()

    def __repr__(self):
        return str([c for c in self._cards])

    def __str__(self):
        return f"The deck is composed of {len(self._cards)} cards."

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, pos):
        return self._cards[pos]

    def build(self, num):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
        self._cards *= num

    def shuffle_deck(self):
        shuffle(self._cards)

    def draw_card(self):
        return self._cards.pop()


class Hand:
    def __init__(self):
        self._cards = list()
        self._value = 0
        self.is_busted = False
        self.doubled_down = False
        self.ace_count = 0

    def __str__(self):
        return str([f"{c[0]} of {c[1]}" for c in self._cards])

    def __repr__(self):
        return str([c for c in self._cards])

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, pos):
        return self._cards[pos]

    def add_card(self, deck):
        s_card = deck.draw_card()
        self._cards.append(s_card)

        try:
            self._value += int(s_card[0])
        except ValueError:
            if s_card[0] in 'J Q K'.split():
                self._value += 10
            elif s_card[0] == 'A':
                self.ace_count += 1
                self._value += 11

        for _ in range(self.ace_count):
            while self._value > 21 and self.ace_count > 0:
                self._value -= 10
                self.ace_count -= 1

    def show_one(self, n):
        return f"{self._cards[n].rank} of {self._cards[n].suit}"


class Chips:
    def __init__(self, amt):
        self._value = amt

    def __repr__(self):
        return f"{self._value}"

    def __str__(self):
        return f"You have chips worth {self._value}$."

    def add_chips(self, amt, hand):
        if hand.doubled_down:
            self._value += amt*2
        else:
            self._value += amt

    def minus_chips(self, amt, hand):
        if hand.doubled_down:
            self._value -= amt*2
        else:
            self._value -= amt


def deal_hands(p_hand, d_hand):
    for i in range(4):
        if i % 2 == 0:
            p_hand.add_card(deck)
        else:
            d_hand.add_card(deck)

    return (f"\n| {d_hand.show_one(0)} v/s {p_hand.show_one(0)} + {p_hand.show_one(1)} |\n")

def dealer_plays(p_hand,d_hand):
    print(f"Dealer: {d_hand} Score: {d_hand._value}")
    sleep(1)
    while d_hand._value < 17:
        d_hand.add_card(deck)
        print(f"Dealer: {d_hand} Score: {d_hand._value}")
        sleep(1)
        if d_hand._value > 21:
            d_hand.is_busted = True

def play_game(p_hand, d_hand):
    p_resp = str()
    while p_resp not in ('H', 'S', 'D'):
        p_resp = input("\nHit, Stand or Double?: ")
        if p_resp.upper() == 'H':
            p_hand.add_card(deck)
            print(f"\nPlayer: {p_hand} Score: {p_hand._value}")
            if p_hand._value > 21:
                p_hand.is_busted = True
                dealer_plays(p_hand,d_hand)
                return pick_winner(p_hand, d_hand)
            p_resp = p_resp
        elif p_resp.upper() == 'D':
            p_hand.doubled_down = True
            p_chips.minus_chips(bet)
            p_hand.add_card(deck)
            print(f"\nPlayer: {p_hand} Score: {p_hand._value}")
            if p_hand._value > 21:
                p_hand.is_busted = True
            dealer_plays(p_hand,d_hand)
            return pick_winner(p_hand, d_hand)
        elif p_resp.upper() == 'S':
            dealer_plays(p_hand,d_hand)
            return pick_winner(p_hand, d_hand)

def pick_winner(p_hand, d_hand):
    if p_hand._value == 21 and len(p_hand) == 2:
        p_chips.add_chips(bet*2, p_hand)
        print("\nBLACKJACK!\n")
        print("You win twice your bet!\n")
        return str(p_chips)
    elif d_hand._value == 21 and len(d_hand) == 2:
        p_chips.minus_chips(bet, p_hand)
        print(f"\nDealer: {d_hand}")
        print("\nDealer gets BLACKJACK!\n")
        return str(p_chips)
    elif p_hand.is_busted:
        p_chips.minus_chips(bet, p_hand)
        print("\nYou're BUST! Better luck next time\n")
        return str(p_chips)
    elif d_hand.is_busted:
        p_chips.add_chips(bet, p_hand)
        print("\nI'm BUST! The round goes to you!\n")
        return str(p_chips)
    elif p_hand._value > d_hand._value:
        p_chips.add_chips(bet, p_hand)
        print("\nWINNER WINNER, CHICKEN DINNER!\n")
        return str(p_chips)
    elif d_hand._value > p_hand._value:
        p_chips.minus_chips(bet, p_hand)
        print("\nSorry! You lose. Better luck next time\n")
        return str(p_chips)
    elif d_hand._value == p_hand._value:
        print("TIE!")
        return str(p_chips)

def replay():
    resp = pyip.inputYesNo("\nWant to gamble again (y/n)?:")
    return resp == 'yes'

if __name__ == "__main__":
    # Game logic
    flag = True
    while flag:
        print("\n-------------Welcome to BlackJack-------------\n")
        gamble_amt = pyip.inputNum("How much would you like to gamble?: ", min=100, max=10000)
        p_chips = Chips(gamble_amt)

        game_on = True

        deck = Deck()
        deck.build(pyip.inputNum("Enter the number of decks(1-6): ", min=1, max=6))

        while game_on:

            print("Shuffling your deck . . .")
            deck.shuffle_deck()
            sleep(1)

            while p_chips._value:
                if pyip.inputYesNo("\nAll in (y/n)?: ") == 'yes':
                    bet = int(repr(p_chips))
                else:
                    bet = pyip.inputNum("Enter your bet: ", min=1, max=int(repr(p_chips)))

                p_hand = Hand()
                d_hand = Hand()

                print(deal_hands(p_hand, d_hand))

                print(play_game(p_hand, d_hand))

                if not p_chips._value:
                    print("\nCongrats! You have successfully gambled all your chips.")
                    game_on = False
                    flag = False
                    break

        if replay():
            flag = True
        else:
            print("\nOK! Goodbye")
