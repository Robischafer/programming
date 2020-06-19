import operator
import random
import pygame


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.image_path = ('img/' + str(rank) + str(suit) + '.png')
        self.selected = False

        if self.rank == 14:
            self.value = 11
        elif self.rank == 13:
            self.value = 4
        elif self.rank == 12:
            self.value = 3
        elif self.rank == 11:
            self.value = 2
        elif self.rank == 10:
            self.value = 10
        else:
            self.value = 0

        # convert the rank to an integer so it's easier to compute the winner of a hand
        if rank == 'A':
            self.rank = 14
        elif rank == 'K':
            self.rank = 13
        elif rank == 'Q':
            self.rank = 12
        elif rank == 'J':
            self.rank = 11
        elif rank == 'T':
            self.rank = 10
        else:
            self.rank = int(rank)

    def __str__(self):
        out = ""

        # convert rank back to a word
        if self.rank == 14:
            out += "Ace"
        elif self.rank == 13:
            out += "King"
        elif self.rank == 12:
            out += "Queen"
        elif self.rank == 11:
            out += "Jack"
        else:
            out += str(self.rank)

        out += ' of '

        # convert the suit to a word
        if self.suit == 'H':
            out += 'Hearts'
        elif self.suit == 'S':
            out += 'Spades'
        elif self.suit == 'C':
            out += 'Clubs'
        elif self.suit == 'D':
            out += 'Diamonds'
        else:
            raise Exception("error in card ini")

        return out

    def __int__(self):

        out = ""
        out += str(self.rank)

        # convert the suit to a number
        if self.suit == 'H':
            out += '0'
        elif self.suit == 'S':
            out += '1'
        elif self.suit == 'C':
            out += '2'
        elif self.suit == 'D':
            out += '3'

        return int(out)


class Hand:
    def __init__(self, hand):
        self.hand = hand

    def __getitem__(self, index):
        return self.hand[index]


class Deck:

    def __init__(self):
        self.deck = []
        for suit in ['H', 'S', 'C', 'D']:
            for rank in range(6, 15):
                self.deck.append(Card(rank, suit))
        list(self)

    def __str__(self):
        out = ""
        for card in self.deck:
            out += str(card) + ", "
        return out

    def __getitem__(self, index):
        return self.deck[index]

    def random_order(self):
        # select random card
        # insert in new deck
        # return randomized deck
        temp = []
        L = list(self)
        for i in range(0, 35):
            draw = random.choice(L)
            temp.append(draw)
            L.remove(draw)

        self = temp

        return self


class Jass:

    def __init__(self):
        self.deck = Deck().random_order()
        self.score = [0, 0]
        self.board = []
        self.round = 0
        self.round = None
        self.game_first_player = None
        self.round_first_player = None

    def shuffle(self):
        # method to shuffle the deck of card
        # between game
        self.deck = Deck().random_order()
        return self.deck

    def select_game_first(self):
        # method to determine the first player
        # at jass ini the first player is the one
        # who has the 7 of diamond, then its the
        # player beside the previous 1st player

        if self.game_first_player is None:
            # find player with 7 of diamond in hand
            # Card(7, 0)
            L = []
            for i in range(0, 35):
                L.append(int(list(self.deck)[i]))
            if L.index(73) <= 8:
                self.game_first_player = 0
            elif L.index(73) <= 17:
                self.game_first_player = 1
            elif L.index(73) <= 26:
                self.game_first_player = 2
            else:
                self.game_first_player = 3
        else:
            self.game_first_player = (self.game_first_player + 1) % 4
        return self.game_first_player

    def select_round_first(self):
        # the current round 1st player
        # is the previous round winner
        # except in the fist round
        if self.round is None:
            self.round_first_player = self.game_first_player
            self.round = 0
        else:
            self.round_first_player += self.check_round_winner()
            self.round += 1

        return self.round_first_player % 4

    def play(self, hand, board):

        return board

    def ai_play(self, hand, board):

        # 1st player can play anything
        if not board:
            valid_card = [card for card in hand]
        # other player must player either trump card
        # or the same card color as the 1st player
        elif board and [card for card in hand if card.suit == board[0].suit]:
            valid_card = [card for card in hand if card.suit == board[0].suit]
        # when players cannot play any cards, restriction
        # are lifted and they can play anything
        else:
            valid_card = [card for card in hand]

        played_card = random.choice(valid_card)
        hand = [card for card in hand if card != played_card]
        self.board.append(played_card)
        return hand, self.board

    def check_round_winner(self):
        # return the position on the board who won
        b = self.board
        round_color = b[0].suit
        highest_valid_card = b[0]
        winner = 0
        # find highest ranking card
        for i in range(1, 3):
            if round_color == b[i].suit and highest_valid_card.rank < b[i].rank:
                highest_valid_card = b[i]
                winner = i

        return winner

    def add_round_score(self):
        winner = self.check_round_winner()
        b = self.board
        round_score = 0
        for i in range(0, 4):
            round_score += b[i].value

        if winner % 2 == 0:
            self.score[0] += round_score
        else:
            self.score[1] += round_score

        return self.score


# test

# game ini
jass = Jass()

hand_1 = Hand(jass.deck[0:8])
hand_2 = Hand(jass.deck[9:17])
hand_3 = Hand(jass.deck[18:26])
hand_4 = Hand(jass.deck[27:35])

jass.select_game_first()
jass.select_round_first()

# each player play
jass.hand_1 = jass.ai_play(hand_1, jass.board)
jass.hand_2 = jass.ai_play(hand_2, jass.board)
jass.hand_3 = jass.ai_play(hand_3, jass.board)
jass.hand_4 = jass.ai_play(hand_4, jass.board)

for card in jass.board:
    print(str(card))
for card in hand_1:
    print(str(card))
len(list(hand_1))

jass.check_round_winner()
jass.add_round_score()
jass.select_round_first()
jass.board = []
