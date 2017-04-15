import pygame
import random
# from pygame.locals import *
# import os, sys

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

pygame.init()

class gameMain:

    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load(image)


    def mainLoop(self):
        done = True
        # attaching = False
        all_sprites=pygame.sprite.Group()
        all_players=pygame.sprite.Group()
        # ball_group=pygame.sprite.Group()
        # player2 = Player('player.png', (30,30))
        player1 = Player(True, (200,100))
        player2 = Player(False, (200,350))
        ball = SoccerBall(self.width, self.height)
        all_sprites.add(player1)
        all_sprites.add(player2)
        all_sprites.add(ball)
        all_players.add(player1)
        all_players.add(player2)
        # ball_group.add(ball)

        while done:
            self.screen.blit(self.background_image,(0,0))
            # player
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done=False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done=False

            for player in all_players:
                player.move(ball)

            collision=pygame.sprite.spritecollide(ball, all_players, False)
            if collision != []:
                for colls in collision:
                    ball.attached = True
                    for players in all_players:
                        players.getPlayer(ball)
            else:
                for players in all_players:
                    players.noball = True
            all_sprites.draw(self.screen)
            pygame.display.flip()

class Player(pygame.sprite.Sprite):
    def __init__(self, control, position, opponent=None):
        super().__init__()
        self.image = pygame.image.load('player.png')
        # self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.accel_x = 0
        self.accel_y = 0
        self.control = control
        self.rect.x, self.rect.y = position
        self.noball = True
        self.changeready = False

    def move(self, ball):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        # event = pygame.key.get_focused()
        # print("A",event)
        if self.control == True:
            if key[pygame.K_s]:
                if self.accel_y < 5:
                    self.accel_y+=1
            if key[pygame.K_w]:
                if self.accel_y > -5:
                    self.accel_y-=1
            if key[pygame.K_d]:
                if self.accel_x < 5:
                    self.accel_x += 1;
            if key[pygame.K_a]:
                if self.accel_x > -5:
                    self.accel_x -= 1;
            if sum(key)==0:
                print("NOKEY")
                if self.accel_x > 0:
                    self.accel_x -= 0.5
                elif self.accel_x < 0:
                    self.accel_x += 0.5
                if self.accel_y>0:
                    self.accel_y -= 0.5
                elif self.accel_y<0:
                    self.accel_y += 0.5
            self.rect.x += self.accel_x
            self.rect.y += self.accel_y

            if self.control == True:
                ball.update(self.rect.x, self.rect.y)

        if key[pygame.K_q] and self.noball == True:
            if self.changeready == True:
                if self.control == True:
                    self.control = False
                else:
                    self.control = True
                self.changeready = False
        if not key[pygame.K_q] and self.changeready == False:
            self.changeready = True


    def getPlayer(self, ball):
        if pygame.sprite.collide_rect(ball, self):
            self.control = True
        else:
            self.control = False



class SoccerBall(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        # import math
        self.image = pygame.image.load('soccerball.jpg').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size=self.image.get_rect().size
        self.rect.x = width/2-(self.size[0]/2)
        self.rect.y = height/2-(self.size[1]/2)
        self.image.get_rect().size
        self.accel_x, self.accel_y = 0,0
        self.attached = False
        self.mouseX, self.mouseY = 0,0
        self.angleX, self.angleY = 0,0

    def update(self, x, y):
        import math
        #Calculate Position
        if self.attached == True:
            self.mouseX, self.mouseY = pygame.mouse.get_pos()
            self.angleX = math.acos((self.mouseX-x)/math.hypot(self.mouseX-x,self.mouseY-y))
            self.angleY = math.asin((self.mouseY-y)/math.hypot(self.mouseX-x,self.mouseY-y))

            self.rect.x = x+math.cos(self.angleX)*50
            self.rect.y = y+math.sin(self.angleY)*50

        #Calculate Acceleration
        if self.accel_x != 0:
            if self.accel_x > 10:
                self.accel_x -= int(abs((math.cos(self.angleX)*5)))
            elif self.accel_x < -10:
                self.accel_x += int(abs((math.cos(self.angleX)*5)))
            else:
                self.accel_x = 0
        if self.accel_y != 0:
            if self.accel_y > 10:
                self.accel_y -= int(abs((math.sin(self.angleY)*5)))
            elif self.accel_y < -10:
                self.accel_y += int(abs((math.sin(self.angleY)*5)))
            else:
                self.accel_y = 0

        #Apply ball Position according to mouse
        self.rect.x += self.accel_x
        self.rect.y += self.accel_y
        # print(int(math.cos(self.angleX)*30))
        #BALL BOUNDARIES
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= (800 - self.rect.width):
            self.rect.x = (800 - self.rect.width)
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= (521 - self.rect.height):
            self.rect.y = (521 - self.rect.height)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.attached == True: # down key
            attached = False
            self.kick()
            print("KICKED")

    def kick(self):
        import math
        self.accel_x += (math.cos(self.angleX)*30)
        self.accel_y += (math.sin(self.angleY)*30)
        self.attached = False

if __name__ == "__main__":
    MainWindow = gameMain(800, 521, 'field.png')
    MainWindow.mainLoop()
