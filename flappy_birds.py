import pygame
import random
pygame.init()
pygame.font.init()

fps = 60
WIDTH = 800
HEIGHT = WIDTH

BACKGROUNDCOLOR = (20, 20, 20)

WHITE = (255, 255, 255)
RED = (240, 50, 50)
GREEN = (50, 240, 50)

BIRDWIDTH = 30
BIRDHEIGHT = 30

BORDERSPEED = 4
BORDERWIDTH = 70
DISTANCEBETWEENBORDERS = 150

GRAVITY = 0.5
MAXACCELERATION = 8
MAXVELOCITY = 9
MINVELOCITY = -18

FONTSTYLE = 'ROBOTO'
FONTSIZE = 40
FONTSIZETITLE = 60
FONTCOLOR = (130, 130, 130) #(255, 255, 255)
FONT = pygame.font.SysFont(FONTSTYLE, FONTSIZE)
FONTTITLE = pygame.font.SysFont(FONTSTYLE, FONTSIZETITLE)

BIRDSTARTX = WIDTH/4
BIRDSTARTY = HEIGHT/2 

BORDERSTARTX = WIDTH
BORDERSTARTY = 0

pygame.display.set_caption(f'Flappy Birds Game')
win = pygame.display.set_mode((WIDTH, HEIGHT))
gamestate = 0
score = 0
MAXSCORE = 100

class Bird():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = BIRDWIDTH
        self.height = BIRDHEIGHT
        self.acceleration = 0
        self.velocity = 0

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move(self):
        self.acceleration = min(self.acceleration+GRAVITY, MAXACCELERATION)
        self.velocity = max(MINVELOCITY, min(self.velocity+self.acceleration, MAXVELOCITY)) 
        self.y += self.velocity
        self.velocity = 0

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Border():

    _registry = []

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = BORDERWIDTH
        self.height = 300

        self._registry.append(self)

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height), width=2)

    def move(self):
        self.x -= BORDERSPEED
        
        if self.x + self.width < 0:
            self.x = WIDTH
            if self == border1:
                self.height = random.randrange(150, 450)
                border2.y = self.y+self.height+DISTANCEBETWEENBORDERS
                border2.height = HEIGHT-self.height-DISTANCEBETWEENBORDERS
            if self == border3:
                self.height = random.randrange(150, 450)
                border4.y = self.y+self.height+DISTANCEBETWEENBORDERS
                border4.height = HEIGHT-self.height-DISTANCEBETWEENBORDERS

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

bird = Bird(BIRDSTARTX, BIRDSTARTY, RED)
border1 = Border(BORDERSTARTX, BORDERSTARTY, WHITE)
border2 = Border(BORDERSTARTX, HEIGHT-border1.height, WHITE)
border3 = Border(BORDERSTARTX+BORDERSTARTX/2+BORDERWIDTH/2, BORDERSTARTY, WHITE)
border4 = Border(BORDERSTARTX+BORDERSTARTX/2+BORDERWIDTH/2, HEIGHT-border1.height, WHITE)

def resetGame():
    global gamestate
    gamestate = 0

def drawWindow(win):
    win.fill(BACKGROUNDCOLOR)

    bird.move()
    bird.draw(win)

    for border in Border._registry:
        border.move()
        border.draw(win)

        if bird.getRect().colliderect(border.getRect()):
            print("lost")

def main():
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            et = event.type
            if et == pygame.QUIT:
                run = False
                break

            elif et == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.acceleration = -13

                if gamestate == 1 and event.key == pygame.K_RETURN:
                    resetGame()

        drawWindow(win)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()