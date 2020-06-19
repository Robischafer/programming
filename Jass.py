import os
import sys
import pygame
import JassModel

HEIGHT = 720
WIDTH = 1280

# global constant
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
grey = pygame.Color(128, 128, 128)
red = pygame.Color(255, 0, 0)
blue = pygame.Color(0, 0, 255)
green = pygame.Color(0, 255, 0)


class GameController:

    def __init__(self):
        deck = JassModel.Deck()
        self.images = {}
        self.scale = 0.5
        self.cardSize = (WIDTH / 7, WIDTH / 5)
        self.buffer = 50
        self.background = pygame.image.load("img/background.jpg").convert_alpha()
        self.cardBack = pygame.image.load('img/back.png').convert_alpha()
        self.cardBack = pygame.transform.scale(self.cardBack, (int(self.scale * self.cardSize[0]),
                                                               int(self.scale * self.cardSize[1])))

        # draw loading screen
        font = pygame.font.Font("font/CoffeeTin.ttf", 50)
        loadText = font.render("Loading...", 1, black)
        loadSize = font.size("Loading...")
        loadLoc = (WIDTH / 2 - loadSize[0] / 2, HEIGHT / 2 - loadSize[1] / 2)

        self.scores = [0, 0, 0, 0]
        SCREEN.blit(self.background, -320, -100)
        SCREEN.blit(loadText, loadLoc)
        pygame.display.flip()

        # draw game card
        for card in deck:
            self.images[str(card)] = pygame.image.load(card.image_path).convert_alpha()
            self.images[str(card)] = pygame.transform.scale(self.images[str(card)],
                                                            (int(self.scale * self.cardSize[0]),
                                                             int(self.scale * self.cardSize[1])))

        self.start_up_init()

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

    def start_up_init(self):
        # method for the starting screen
        self.jass = JassModel.Jass(self.scores)

        self.font = pygame.font.Font('font/CoffeeTin.ttf', 150)
        self.font2 = pygame.font.Font('font/IndianPoker.ttf', 75)
        self.font2.set_bold(True)

        self.startText = self.font2.render("Welcome to Jass!", 1, black)
        self.startSize = self.font2.size("Welcome to Jass!")
        self.startLoc = (WIDTH / 2 - self.startSize[0] / 2, self.buffer)

        self.startButton = self.font.render(" Start ", 1, black)
        self.buttonSize = self.font.size(" Start ")
        self.buttonLoc = (WIDTH / 2 - self.buttonSize[0] / 2, HEIGHT / 2 - self.buttonSize[1] / 2)

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)

        self.state = 0

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
                    if mouseRect.collidedict(self.buttonRect):
                        self.state += 1
                        self.play_init()
                        return

        # background
        SCREEN.blit(self.background, (-320, -100))

        # welcome text
        SCREEN.blit(self.startText, self.startLoc)

        # start button
        pygame.draw.rect(SCREEN, red, self.buttonRect)
        pygame.draw.rect(SCREEN, black, self.buttonRectOutline, 2)
        SCREEN.blit(self.startButton, self.buttonLoc)

        pygame.display.flip()

    def play_init(self):

        # create the new variables
        self.cardLoc = {}
        self.round = 0

        # setup the locations for each card in the hand
        x = 4.5 * int(self.scale * self.cardSize[0])
        self.youLoc = (x - 150, self.buffer)

        for index in range(len(self.jass.playerHand)):
            self.cardLoc[index] = (x, self.buffer)
            x += int(self.scale * self.cardSize[0])

        # setup the text that will be printed to the screen
        self.font = pygame.font.Font('font/IndianPoker.ttf', 25)
        self.font.set_bold(True)
        self.font2 = pygame.font.Font('font/CoffeeTin.ttf', 60)
        self.youText = self.font.render("Your Hand", 1, black)
        self.youSize = self.font.size("Your Hand")

        self.youLoc = (self.cardLoc[0][0], self.cardLoc[0][1] - 30)
        # (self.youLoc[0], self.buffer + self.scale * self.cardSize[1]/2 - self.youSize[1]/2)

        self.playButton = self.font2.render(" Play ", 1, black)
        self.buttonSize = self.font2.size(" Play ")

        self.buttonLoc = (x + 30, self.buffer + self.scale * self.cardSize[1] / 2 - self.buttonSize[1] / 2)

        self.buttonRect = pygame.Rect(self.buttonLoc, self.buttonSize)
        self.buttonRectOutline = pygame.Rect(self.buttonLoc, self.buttonSize)

    def play(self):
        return 0

    def results_init(self):
        return 0

    def results(self):
        return 0

    def display_hand(self, hand, x, y):
        for card in hand:
            SCREEN.blit(self.images[str(card)], (x, y))
            x += int(self.scale * self.cardSize[0])

    def display_scoreboard(self):
        return 0


if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center screen
    pygame.init()
    pygame.display.set_caption("Jass")
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)

    Runit = GameController()
    FPS = pygame.time.Clock()
    while 1:
        Runit.main()
        FPS.tick(30)

pygame.quit()
