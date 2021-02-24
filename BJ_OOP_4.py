from time import sleep
import pyinputplus as pyip
from random import shuffle
from collections import namedtuple

Card = namedtuple('Card',['rank','suit'])

class Deck:

	ranks = [str(n) for n in range(2,11)] + list('JQKA')
	suits = 'SPADES DIAMONDS HEARTS CLUBS'.split()

	def __init__(self):
		self._cards = list()

	def __repr__(self):
		return str((c for c in self._cards))

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
		return shuffle(self._cards)

	def draw_card(self):
		return self._cards.pop()


class Hand:
	def __init__(self):
		self._cards = list()
		self._value = 0
		self.is_busted = False
		self.doubled_down = False
		self.ace_count = 0
		self.ace_not_in = True

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
				self._value += 1

		if self._value > 12 and self.ace_count and self.ace_not_in:
			self._value -= 10
			self.ace_not_in = False

		count = 0
		for n in self._cards:
			if n[0] == 'A':
				count += 1
		for ace in range(count):
			if self._value < 12:
				self._value += 10

	def show_one(self,n):
		return f"{self._cards[n].rank} of {self._cards[n].suit}" 


class Chips:
	def __init__(self, amt):
		self._value = amt

	def __repr__(self):
		return f"{self._value}"

	def __str__(self):
		return f"You have chips worth {self._value}$."

	def add_chips(self, amt):
		self._value += amt

	def minus_chips(self, amt):
		self._value -= amt


def pick_winner(p_hand,d_hand):
	if p_hand._value == 21 and len(p_hand) == 2:
		p_chips.add_chips(bet*2)
		print("\nBLACKJACK!\n")
		print("You win twice your bet!\n")
		return str(p_chips)
	elif d_hand._value == 21 and len(d_hand) == 2:
		p_chips.minus_chips(bet)
		print("\nDealer got BLACKJACK!\n")
		return str(p_chips)
	elif p_hand.is_busted:
		if p_hand.doubled_down:
			p_chips.minus_chips(bet*2)
		else:
			p_chips.minus_chips(bet)
		print("\nYou're BUST! Better luck next time\n")
		return str(p_chips)
	elif p_hand._value < d_hand._value:
		print(d_hand)
		if p_hand.doubled_down:
			p_chips.minus_chips(bet*2)
		else:
			p_chips.minus_chips(bet)
		print("\nSorry! You lose. Better luck next time\n")
		return str(p_chips)
	elif d_hand._value == p_hand._value:
		print(d_hand)
		print("TIE!")
		return str(p_chips)
	else:
		while d_hand._value <= 17:
			d_hand.add_card(deck)
			if d_hand._value > 21:
				d_hand.is_busted = True

			if d_hand.is_busted:
				print(d_hand)
				if p_hand.doubled_down:
					p_chips.add_chips(bet*2)
				else:
					p_chips.add_chips(bet)
				print("\nI'm BUST!\n")
				return str(p_chips)
			elif d_hand._value > p_hand._value:
				print(d_hand)
				if p_hand.doubled_down:
					p_chips.minus_chips(bet*2)
				else:
					p_chips.minus_chips(bet)
				print("\nSorry! You lose. Better luck next time\n")
				return str(p_chips)
			elif d_hand._value < p_hand._value:
				if p_hand.doubled_down:
					p_chips.add_chips(bet*2)
				else:
					p_chips.add_chips(bet)
				print("\nWINNER WINNER, CHICKEN DINNER!\n")
				return str(p_chips)
			elif d_hand._value == p_hand._value:
				print("TIE!")
				return str(p_chips)
			else:
				continue

def deal_hands(p_hand,d_hand):
	for i in range(4):
		if i % 2 == 0:
			p_hand.add_card(deck)
		else:
			d_hand.add_card(deck)

	return (f"\n| {d_hand.show_one(0)} v/s {p_hand.show_one(0)} + {p_hand.show_one(1)} |\n")
 
def play_game(p_hand,d_hand):
	p_resp = str()
	while p_resp not in ('H', 'S', 'D'):
		p_resp = input("\nHit, Stand or Double?: ")
		if p_resp.upper() == 'H':
			p_hand.add_card(deck)
			print(p_hand)
			if p_hand._value > 21:
				p_hand.is_busted = True
				return pick_winner(p_hand,d_hand)
			p_resp = p_resp
		elif p_resp.upper() == 'D':
			p_hand.doubled_down = True
			p_chips.minus_chips(bet)
			p_hand.add_card(deck)
			print(p_hand)
			if p_hand._value > 21:
				p_hand.is_busted = True
				return pick_winner(p_hand,d_hand)
		elif p_resp.upper() == 'S':
			return pick_winner(p_hand,d_hand)

def replay():
	resp = pyip.inputYesNo("Want to gamble again (y/n)?:")
	if resp == 'yes':
		return True
	else:
		return False

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
			if pyip.inputYesNo("All in (y/n)?: ") == 'yes':
				bet = int(repr(p_chips))
			else:
				bet = pyip.inputNum("Enter your bet: ", min=1, max=int(repr(p_chips)))

			p_hand = Hand()
			d_hand = Hand()

			print(deal_hands(p_hand,d_hand))

			print(play_game(p_hand,d_hand))

			if not p_chips._value:
				print("\nCongrats! You have successfully gambled all your chips.")
				game_on = False
				flag = False
				replay = replay()
				break

	if replay == True:
		flag = True
	else:
		print("OK! Goodbye")
		
		
