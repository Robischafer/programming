import operator
import random
import pygame


# possible improvement:
# implement trump card (ai_play:valid_card, new method jass.game_trump
#                       check_round_winner(), add_round_score())
# implement hand sorting for player
# implement validation and error handling
# implement switch case

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

    def __len__(self):
        return len(self.hand)


class Deck:

    def __init__(self):
        self.deck = list()
        for suit in ['H', 'S', 'C', 'D']:
            for rank in range(6, 15):
                self.deck.append(Card(rank, suit))

    def __str__(self):
        out = ""
        for i in range(0, len(self.deck)):
            out += str(self.deck[i]) + ", "
        return out

    def __getitem__(self, index):
        return self.deck[index]

    def __len__(self):
        return len(self.deck)

    def __delitem__(self, i):
        del self.deck[i]

    def random_order(self):
        # select random card
        # insert in new deck
        # return randomized deck
        temp = []
        for i in range(0, 36):
            draw = random.choice(self.deck)
            temp.append(draw)
            self.deck.remove(draw)

        self.deck = temp

        return self


class Jass:

    def __init__(self):
        self.deck = Deck()
        self.score = [0, 0]
        self.board = []
        self.round = None
        self.game_first_player = None
        self.round_first_player = None
        self.trump = None

        self.hand_1 = None
        self.hand_2 = None
        self.hand_3 = None
        self.hand_4 = None

    def shuffle(self):
        # method to shuffle the deck of card
        # between game
        self.deck.random_order()

        self.hand_1 = Hand(self.deck[0:9])
        self.hand_2 = Hand(self.deck[9:18])
        self.hand_3 = Hand(self.deck[18:27])
        self.hand_4 = Hand(self.deck[27:36])

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
            for i in range(0, 36):
                L.append(int(self.deck[i]))

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
            self.round_first_player = self.round_first_player % 4
            self.round += 1

        return self.round_first_player

    def play(self, hand, card_selected):

        hand = [card for card in hand if card != card_selected]
        self.board.append(card_selected)

        return hand

    def ai_play(self, hand):

        # 1st player can play anything
        if not self.board:
            valid_card = [card for card in list(hand)]
        # other player must player either trump card
        # or the same card color as the 1st player
        elif self.board and [card for card in list(hand) if card.suit == self.trump]:
            valid_card = [card for card in list(hand) if (card.suit == self.trump or card.suit == self.board[0].suit)]
        elif self.board and [card for card in list(hand) if card.suit == self.board[0].suit]:
            valid_card = [card for card in list(hand) if card.suit == self.board[0].suit]
        # when players cannot play any cards, restriction
        # are lifted and they can play anything
        else:
            valid_card = [card for card in list(hand)]

        played_card = random.choice(valid_card)
        hand = [card for card in hand if card != played_card]
        self.board.append(played_card)
        return hand

    def check_round_winner(self):
        # return the position on the board who won
        round_color = self.board[0].suit
        if self.round == 0:
            self.set_trump_card(round_color)
        highest_trump_card = Card(0, "H")
        highest_valid_card = Card(0, "H")
        trump_winner = 0
        normal_winner = 0

        # check if trump card on board
        # if yes, then check highest trump card !puur and nell!
        # if not then find highest normal ranking card
        for i in range(1, 4):
            if self.board[i].suit == self.trump and highest_trump_card.rank < self.board[i].rank:
                if self.board[i].rank == 11 and highest_trump_card != Card(11, self.trump):
                    highest_trump_card = self.board[i]
                    trump_winner = i
                elif self.board[i].rank == 9 and highest_trump_card != Card(11, self.trump) \
                        and highest_trump_card != Card(9, self.trump):
                    highest_trump_card = self.board[i]
                    trump_winner = i
                else:
                    highest_trump_card = self.board[i]
                    trump_winner = i

            elif round_color == self.board[i].suit and highest_valid_card.rank < self.board[i].rank:
                highest_valid_card = self.board[i]
                normal_winner = i
            else:
                continue

        if trump_winner != 0:
            return trump_winner
        else:
            return normal_winner

    def set_trump_card(self, trump):
        self.trump = trump
        # set puur and nell
        L = []
        for i in range(0, 36):
            L.append(int(self.deck[i]))
        self.deck[L.index(int(Card(11, trump)))].value = 20
        self.deck[L.index(int(Card(9, trump)))].value = 14

    def add_round_score(self):
        winner = (self.round_first_player + self.check_round_winner() + 1) % 4
        if self.round == 8:
            round_score = 5
        else:
            round_score = 0
        for i in range(0, 4):
            round_score += self.board[i].value

        if winner % 2 == 0:
            self.score[0] += round_score
        else:
            self.score[1] += round_score

        # TO DO: if 157 -> 257

        return self.score
