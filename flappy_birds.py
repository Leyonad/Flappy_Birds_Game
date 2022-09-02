import pygame
import random
pygame.init()
pygame.font.init()

fps = 60
WIDTH = 700
HEIGHT = 800

BACKGROUNDCOLOR = (20, 20, 20)

WHITE = (255, 255, 255)
RED = (240, 50, 50)
GREEN = (50, 240, 50)

BIRDWIDTH = 30
BIRDHEIGHT = 30

N_BORDERS = 3
BORDERSPEED = 4
BORDERWIDTH = 70
DISTANCEBETWEENBORDERS = 150

GRAVITY = 0.8
MAXACCELERATION = 8
MAXVELOCITY = 9
MINVELOCITY = -10

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

        if self.y < 0 or self.y+self.height > HEIGHT:
            global gamestate
            gamestate = 1

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Border():

    _registry = []

    def __init__(self, index, color):
        self.index = index
        self.color = color
        self.width = BORDERWIDTH
        self.height = random.randrange(250, HEIGHT-350)
        self.x = WIDTH + (index//2) * ((WIDTH-BORDERWIDTH*N_BORDERS)/N_BORDERS + BORDERWIDTH)
        self.y = 0
        self.crossed = False
        
        if self.index % 2 != 0:
            self.x = self._registry[self.index-1].x
            self.y = self._registry[self.index-1].height + DISTANCEBETWEENBORDERS
            self.height = HEIGHT - self.y

        self._registry.append(self)

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width, self.height), width=2)

    def move(self):
        self.x -= BORDERSPEED
        
        if self.x < 0:
            self.x = WIDTH
            self.crossed = False
            if self.index % 2 == 0:
                self.height = random.randrange(250, HEIGHT-350)
            else:
                self.y = self._registry[self.index-1].height + DISTANCEBETWEENBORDERS
                self.height = HEIGHT - self.y

    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

bird = Bird(BIRDSTARTX, BIRDSTARTY, RED)
[Border(i, WHITE) for i in range(N_BORDERS*2)]

def resetGame():
    global gamestate, score
    gamestate = 0
    score = 0
    bird.y = BIRDSTARTY
    for border in Border._registry:
        border.x = WIDTH + (border.index//2) * ((WIDTH-BORDERWIDTH*N_BORDERS)/N_BORDERS + BORDERWIDTH)
        border.height = random.randrange(250, HEIGHT-350)
        if border.index % 2 != 0:
                    border.x = Border._registry[border.index-1].x
                    border.y = Border._registry[border.index-1].height + DISTANCEBETWEENBORDERS
                    border.height = HEIGHT - border.y

def drawWindow(win):
    global gamestate, score
    win.fill(BACKGROUNDCOLOR)
    
    if gamestate == 0:
        bird.draw(win)
        bird.move()
        for border in Border._registry:
            border.move()
            border.draw(win)

            if bird.x > border.x and border.crossed is False:
                border.crossed = True
                score += 0.5

            if bird.getRect().colliderect(border.getRect()):
                gamestate = 1
                break
    else:
        label2 = FONT.render(f'POINTS: {round(score) }', True, FONTCOLOR)
        label_rect2 = label2.get_rect(center=(WIDTH/2, HEIGHT/2+label2.get_height()))
        label3 = FONT.render(f'PRESS SPACEBAR TO RESTART', True, FONTCOLOR)
        label_rect3 = label3.get_rect(center=(WIDTH/2, HEIGHT/2+label2.get_height()*2))
        win.blit(label2, label_rect2)
        win.blit(label3, label_rect3)

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

                if gamestate == 1 and event.key == pygame.K_SPACE:
                    resetGame()

        drawWindow(win)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()