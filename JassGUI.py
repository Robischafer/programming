import os
import sys
import pygame
import JassModel

# Montserrat font are from https://www.fontsquirrel.com/fonts/list/popular
# card back from https://opengameart.org/content/colorful-poker-card-back

HEIGHT = 720
WIDTH = 1280

# global constant
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
gray = pygame.Color(128, 128, 128)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)

# score to end the game
ENDSCORE = 1000
# variable used in wait time
PAUSE_TIME = 1500


class GameController:

    def __init__(self):
        self.jass = JassModel.Jass()
        self.state = 0
        self.images = {}
        self.scale = 0.5
        self.cardSize = (WIDTH / 7, WIDTH / 5)
        self.buffer = 50
        self.background = pygame.image.load("img/background.jpg").convert_alpha()
        self.cardBack = pygame.image.load('img/back.png').convert_alpha()
        self.cardBack = pygame.transform.scale(self.cardBack, (int(self.scale * self.cardSize[0]),
                                                               int(self.scale * self.cardSize[1])))

        # draw loading screen
        font = pygame.font.Font("font/Montserrat-Black.otf", 50)
        loadText = font.render("Loading...", 1, black)
        loadSize = font.size("Loading...")
        loadLoc = (WIDTH / 2 - loadSize[0] / 2, HEIGHT / 2 - loadSize[1] / 2)

        SCREEN.blit(self.background, (-320, -100))
        SCREEN.blit(loadText, loadLoc)
        pygame.display.flip()

        # draw game card
        for card in self.jass.deck:
            self.images[str(card)] = pygame.image.load(card.image_path).convert_alpha()
            self.images[str(card)] = pygame.transform.scale(self.images[str(card)],
                                                            (int(self.scale * self.cardSize[0]),
                                                             int(self.scale * self.cardSize[1])))

        # ini for the starting screen

        self.font = pygame.font.Font('font/Montserrat-Bold.otf', 150)
        self.font2 = pygame.font.Font('font/Montserrat-Regular.otf', 75)
        self.font2.set_bold(True)

        self.startText = self.font2.render("Welcome to Jass!", 1, black)
        self.startSize = self.font2.size("Welcome to Jass!")
        self.startLoc = (WIDTH / 2 - self.startSize[0] / 2, self.buffer)

        self.startButton = self.font.render(" Start ", 1, black)
        self.buttonSize = self.font.size(" Start ")
        self.buttonLoc = (WIDTH / 2 - self.buttonSize[0] / 2, HEIGHT / 2 - self.buttonSize[1] / 2)

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)

    def main(self):
        # method to check game state
        if self.state == 0:
            self.start_up()
        elif self.state == 1:
            self.play()
        elif self.state == 2:
            self.results()
        else:
            self.new_game()

    def start_up(self):
        # method used to start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # clicking the button activate the playing state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseRect = pygame.Rect(event.pos, (1, 1))
                    if mouseRect.colliderect(self.buttonRect):
                        self.state += 1
                        self.play_init()
                        return

        # background
        SCREEN.blit(self.background, (-320, -100))

        # welcome text
        SCREEN.blit(self.startText, self.startLoc)

        # start button
        pygame.draw.rect(SCREEN, gray, self.buttonRect)
        pygame.draw.rect(SCREEN, black, self.buttonRectOutline, 2)
        SCREEN.blit(self.startButton, self.buttonLoc)

        pygame.display.flip()

    def play_init(self):

        # create the new variables
        self.cardLoc = {}
        self.jass.shuffle()
        self.jass.board = []
        self.jass.round = None
        self.jass.select_game_first()
        self.jass.select_round_first()
        self.play_before_player()

        # setup the locations for each card in the hand
        x = 1 * int(self.scale * self.cardSize[0])
        self.youLoc = (x - 150, self.buffer)

        for index in range(len(list(self.jass.hand_1))):
            self.cardLoc[index] = (x, self.buffer)
            x += int(self.scale * self.cardSize[0])

        # setup the text that will be printed to the screen
        self.font = pygame.font.Font('font/Montserrat-Regular.otf', 25)
        self.font.set_bold(True)
        self.font2 = pygame.font.Font('font/Montserrat-Bold.otf', 60)
        self.youText = self.font.render("Your Hand", 1, black)
        self.youSize = self.font.size("Your Hand")

        self.youLoc = (self.cardLoc[0][0], self.cardLoc[0][1])
        # player 2
        self.player2Loc = (50, HEIGHT / 2)
        self.player2TextLoc = (50, HEIGHT / 2 - 50)
        self.player2Text = self.font.render("player 2", 1, black)
        self.player2Size = self.font.size("player 2")
        # player 3
        self.player3Loc = (WIDTH / 2, HEIGHT - 200)
        self.player3TextLoc = (WIDTH / 2, HEIGHT - 250)
        self.player3Text = self.font.render("player 3", 1, black)
        self.player3Size = self.font.size("player 3")
        # player 4
        self.player4Loc = (WIDTH - 150, HEIGHT / 2)
        self.player4TextLoc = (WIDTH - 150, HEIGHT / 2 - 50)
        self.player4Text = self.font.render("player 4", 1, black)
        self.player4Size = self.font.size("player 4")

        self.playButton = self.font2.render(" Play ", 1, black)
        self.buttonSize = self.font2.size(" Play ")

        self.buttonLoc = (x + 30, self.buffer + self.scale * self.cardSize[1] / 2 - self.buttonSize[1] / 2)

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)

    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # when the user clicks on a card, change its color to signify a selection has occurred
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # create a rectangle for the mouse click and for each card
                    # check for intersection
                    mouseRect = pygame.Rect(event.pos, (1, 1))
                    for index in range(len(list(self.jass.hand_1))):
                        cardRect = pygame.Rect(self.cardLoc[index],
                                               (int(self.scale * self.cardSize[0]),
                                                int(self.scale * self.cardSize[1])))
                        if cardRect.colliderect(mouseRect):
                            temp = list(self.jass.hand_1)[index]
                            temp.selected = not temp.selected
                            break

                    if self.jass.round_first_player == 0:
                        # check if we clicked the playButton
                        if mouseRect.colliderect(self.buttonRect):
                            for i in range(0, len(list(self.jass.hand_1))):
                                if self.jass.hand_1[i].selected:
                                    card_selected = self.jass.hand_1[i]

                            self.jass.hand_1 = self.jass.play(self.jass.hand_1, card_selected)
                            self.jass.hand_2 = self.jass.ai_play(self.jass.hand_2)
                            self.jass.hand_3 = self.jass.ai_play(self.jass.hand_3)
                            self.jass.hand_4 = self.jass.ai_play(self.jass.hand_4)
                            self.display_board()
                            self.display_hand()
                            pygame.display.flip()

                            pygame.time.wait(PAUSE_TIME)
                            self.check_game_state()
                            return

                    elif self.jass.round_first_player == 1:
                        if mouseRect.colliderect(self.buttonRect):
                            for i in range(0, len(list(self.jass.hand_1))):
                                if self.jass.hand_1[i].selected:
                                    card_selected = self.jass.hand_1[i]

                            self.jass.hand_1 = self.jass.play(self.jass.hand_1, card_selected)
                            self.display_board()
                            self.display_hand()
                            pygame.display.flip()
                            pygame.time.wait(PAUSE_TIME)
                            self.check_game_state()
                            return

                    elif self.jass.round_first_player == 2:
                        if mouseRect.colliderect(self.buttonRect):
                            for i in range(0, len(list(self.jass.hand_1))):
                                if self.jass.hand_1[i].selected:
                                    card_selected = self.jass.hand_1[i]

                            self.jass.hand_1 = self.jass.play(self.jass.hand_1, card_selected)
                            self.jass.hand_2 = self.jass.ai_play(self.jass.hand_2)
                            self.display_board()
                            self.display_hand()
                            pygame.display.flip()
                            pygame.time.wait(PAUSE_TIME)
                            self.check_game_state()
                            return

                    elif self.jass.round_first_player == 3:
                        if mouseRect.colliderect(self.buttonRect):
                            for i in range(0, len(list(self.jass.hand_1))):
                                if self.jass.hand_1[i].selected:
                                    card_selected = self.jass.hand_1[i]

                            self.jass.hand_1 = self.jass.play(self.jass.hand_1, card_selected)
                            self.jass.hand_2 = self.jass.ai_play(self.jass.hand_2)
                            self.jass.hand_3 = self.jass.ai_play(self.jass.hand_3)
                            self.display_board()
                            self.display_hand()
                            pygame.display.flip()
                            pygame.time.wait(PAUSE_TIME)
                            self.check_game_state()
                            return

        # display background
        SCREEN.blit(self.background, (-320, -100))

        # display  players
        self.display_hand()
        SCREEN.blit(self.cardBack, self.player2Loc)
        SCREEN.blit(self.player2Text, self.player2TextLoc)
        SCREEN.blit(self.cardBack, self.player3Loc)
        SCREEN.blit(self.player3Text, self.player3TextLoc)
        SCREEN.blit(self.cardBack, self.player4Loc)
        SCREEN.blit(self.player4Text, self.player4TextLoc)

        # display the text
        pygame.draw.rect(SCREEN, red, self.buttonRect)
        pygame.draw.rect(SCREEN, black, self.buttonRectOutline, 2)
        SCREEN.blit(self.playButton, self.buttonLoc)

        # display the scoreboard, hand, board
        self.display_scoreboard()
        self.display_hand()
        self.display_board()
        pygame.display.flip()

    def results_init(self):
        self.font = pygame.font.Font('font/Montserrat-Regular.otf', 25)
        self.replaceButton = self.font2.render(" New Game ", 1, black)
        self.buttonSize = self.font2.size(" New Game ")
        self.buttonLoc = (WIDTH / 2 - self.buttonSize[0] / 2, HEIGHT / 2 - self.buttonSize[1] / 2)

        self.game_results = self.jass.score

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)

        self.jass.score = [0, 0]
        self.jass.game_first_player = None
        self.jass.round_first_player = None
        self.jass.round = None
        self.jass.board = []

    def results(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseRect = pygame.Rect(event.pos, (1, 1))
                    if mouseRect.colliderect(self.buttonRect):
                        # self.start_up_init()
                        self.state = 1
                        self.play_init()
                        return

        # display background
        SCREEN.blit(self.background, (-320, -100))

        # display a play again button
        pygame.draw.rect(SCREEN, red, self.buttonRect)
        pygame.draw.rect(SCREEN, black, self.buttonRectOutline, 2)
        SCREEN.blit(self.replaceButton, self.buttonLoc)

        self.display_game_results()
        pygame.display.flip()

    def new_game(self):
        self.state = 1
        self.play()

    def display_hand(self):
        for index in range(len(self.jass.hand_1)):
            if not list(self.jass.hand_1)[index].selected:
                SCREEN.blit(self.images[str(self.jass.hand_1[index])], self.cardLoc[index])
            else:
                selectFX = self.images[str(self.jass.hand_1[index])].convert()
                selectFX.set_alpha(128)
                SCREEN.blit(selectFX, self.cardLoc[index])

    def display_board(self, x=WIDTH / 3, y=HEIGHT / 3):
        for card in range(0, len(self.jass.board)):
            SCREEN.blit(self.images[str(self.jass.board[card])], (x, y))
            x += int(self.scale * self.cardSize[0])

    def display_scoreboard(self, x=WIDTH - 200, y=10):
        # create labels for each player
        self.Team1_score = self.font.render("Team 1: " + str(self.jass.score[0]), 1, black)
        self.Team2_score = self.font.render("Team 2: " + str(self.jass.score[1]), 1, black)

        SCREEN.blit(self.Team1_score, (x, y))
        SCREEN.blit(self.Team2_score, (x, y + 30))

    def check_game_state(self):
        self.jass.add_round_score()

        if self.jass.score[0] >= ENDSCORE or self.jass.score[1] >= ENDSCORE:
            self.state += 1
            self.results_init()
            return

        elif self.jass.round < 8:
            self.jass.select_round_first()
            self.jass.board = []
            self.play_before_player()
            return

        elif self.jass.round == 8:
            self.play_init()
            for i in range(0, len(list(self.jass.hand_1))):
                self.jass.hand_1[i].selected = False
            return

    def play_before_player(self):
        # check if ai need to play
        if self.jass.round_first_player == 0:
            self.display_board()
            pygame.display.flip()
        elif self.jass.round_first_player == 1:
            self.jass.hand_2 = self.jass.ai_play(self.jass.hand_2)
            self.jass.hand_3 = self.jass.ai_play(self.jass.hand_3)
            self.jass.hand_4 = self.jass.ai_play(self.jass.hand_4)
            self.display_board()
            pygame.display.flip()
        elif self.jass.round_first_player == 2:
            self.jass.hand_3 = self.jass.ai_play(self.jass.hand_3)
            self.jass.hand_4 = self.jass.ai_play(self.jass.hand_4)
            self.display_board()
            pygame.display.flip()
        elif self.jass.round_first_player == 3:
            self.jass.hand_4 = self.jass.ai_play(self.jass.hand_4)
            self.display_board()
            pygame.display.flip()

    def display_game_results(self, x=WIDTH / 2 - 160, y=HEIGHT / 2 - 100):
        # create labels for each player
        self.Team1_score = self.font.render("Team 1: " + str(self.game_results[0]), 1, black)
        self.Team2_score = self.font.render("Team 2: " + str(self.game_results[1]), 1, black)

        SCREEN.blit(self.Team1_score, (x, y))
        SCREEN.blit(self.Team2_score, (x + 200, y))


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center screen
    pygame.init()
    pygame.display.set_caption("Jass")
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    Run = GameController()
    FPS = pygame.time.Clock()
    while 1:
        Run.main()
        FPS.tick(30)

pygame.quit()
