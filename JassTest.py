# test

# game ini
import random
import JassModel

jass = JassModel.Jass()
jass.shuffle()

hand_1 = JassModel.Hand(jass.deck[0:9])
hand_2 = JassModel.Hand(jass.deck[9:18])
hand_3 = JassModel.Hand(jass.deck[18:27])
hand_4 = JassModel.Hand(jass.deck[27:36])

jass.select_game_first()
print("this game the first player is the player ", jass.game_first_player)
jass.select_round_first()
print("this round the first player is the player ", jass.round_first_player)

for i in range(0, 9):

    jass.board = []
    # each player play
    hand_1 = jass.ai_play(hand_1)
    hand_2 = jass.ai_play(hand_2)
    hand_3 = jass.ai_play(hand_3)
    hand_4 = jass.ai_play(hand_4)

    print("those card have been played this round")
    for card in jass.board:
        print(str(card))
    # for card in hand_1:
    #    print(str(card))
    print("the player 1 has ", len(list(hand_1)), " card remaining")

    jass.check_round_winner()
    print("the winner is player ", jass.check_round_winner() + 1)
    jass.add_round_score()
    print("the score for team [1, 2] are ", jass.score)
    jass.select_round_first()
    print("this round the first player is the player ", jass.round_first_player)



