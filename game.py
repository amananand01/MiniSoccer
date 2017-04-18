import pygame
import random
import math
from Mastermind import *
import time
# from Main import *
# ip_add = "127.0.0.1"
# ip_add = "172.28.127.17"
port = 6317
# from pygame.locals import *
# import os, sys
# playernumber = 1
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

pygame.init()


class gameMain:
    """
        This is the Main Game class.
        Everything pretty much happenes in this class including
         main Loop, initialization of sprites, drawing the screen etc.
    """
    def __init__(self, width, height, image):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = pygame.image.load(image)
        self.clock = pygame.time.Clock()
        self.player1pos = ()
        self.player2pos = ()
        self.player1Score, self.player2Score = 0,0
        self.goal = 0

    def addSpritesToGroup(self, group, sprites):
        for sprite in sprites:
            group.add(sprite)
    # Refreshes the position of every player and the ball
    def refresh(self, all_players, all_opponents, ball):
        for player in all_players:
            player.refresh()
        for opponents in all_opponents:
            opponents.refresh()
        ball.refresh()

    def mainLoop(self, ip_add, playernumber):

        done = True
        # attaching = False
        all_sprites=pygame.sprite.Group()
        all_players=pygame.sprite.Group()
        all_opponents=pygame.sprite.Group()
        net_bound = pygame.sprite.Group()
        net_score = pygame.sprite.Group()
        # ball_group=pygame.sprite.Group()
        # player2 = Player('player.png', (30,30))
        # self.refresh(playernumber)

        global client, server

        client = MastermindClientTCP(5.0,10.0)
        try:
            client.connect(ip_add,port)
            print("Connected!")
        except MastermindError:
            print("Cannot find a Server; Starting Server!!")
            client.connect(ip_add,port)
            pos_recieved=[]

        # Initialization of all sprites
        if playernumber == 1:
            player1 = Player(True)
            player2 = Player(False)
            player3 = Player(False, True)
            player4 = Player(False, True)
        else:
            player1 = Player(True)
            player2 = Player(False)
            player3 = Player(False, True)
            player4 = Player(False, True)

        scoreLeft = goalnet((10,220), 2)
        scoreRight = goalnet((751,220), 2)
        netLTop = goalnet((10,200), 1)
        netLBot = goalnet((10,320), 1)
        netRTop = goalnet((739,200), 1)
        netRBot = goalnet((739,320), 1)
        netLeft = goalnet((10,200))
        netRight = goalnet((739,200))

        ball = SoccerBall()

        # Adds all sprites to group
        self.addSpritesToGroup(all_sprites, [player1, player2, player3, player4,
                                            ball,
                                            netLeft, netRight,
                                            netLTop, netLBot,
                                            netRTop, netRBot,
                                            scoreLeft, scoreRight])
        self.addSpritesToGroup(all_players, [player1, player2])
        self.addSpritesToGroup(all_opponents, [player3, player4])
        self.addSpritesToGroup(net_bound, [netLTop, netLBot, netRTop, netRBot])
        self.addSpritesToGroup(net_score, [scoreLeft, scoreRight])

        # Initialize the position
        while done:
            if playernumber == 1:
                player1.setPosition((200,100))
                player2.setPosition((200,350))
                player3.setPosition((600,100))
                player4.setPosition((600,350))
            else:
                player1.setPosition((600,100))
                player2.setPosition((600,350))
                player3.setPosition((200,100))
                player4.setPosition((200,350))
            ball.setPosition(self.width, self.height)
            ball.accel_x, ball.accel_y = 0,0

            while done:

                self.screen.fill((0,0,0))
                self.screen.blit(self.background_image,(0,0))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Disconnecting")
                        client.disconnect()
                        done=False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        done=False

                #Data
                if pygame.sprite.spritecollide(ball, all_opponents, False):
                    player1.posession = False
                    player2.posession = False

                #Main Loop to update Characters
                for player in all_players:
                    player.move(ball)
                    player.update(ball, net_bound)
                ball.update(net_bound)

                if playernumber == 1:
                    if pygame.sprite.collide_rect(ball, scoreRight):
                        self.player1Score += 1
                        ball.refresh()
                        player1.refresh()
                        player2.refresh()

                elif playernumber == 2:
                    if pygame.sprite.collide_rect(ball, scoreLeft):
                        self.player2Score += 1
                        ball.refresh()
                        player1.refresh()
                        player2.refresh()


                #Always 1 in control
                if (player1.control == True and player2.control == True) or (player1.control == False and player2.control == False):
                    if math.hypot(abs(player1.rect.x-ball.rect.x), abs(player1.rect.y-ball.rect.y)) <= math.hypot(abs(player2.rect.x-ball.rect.x), abs(player2.rect.y-ball.rect.y)):
                        player1.control = True
                        player2.control = False
                    else:
                        player1.control = False
                        player2.control = True


                #CLIENT SEND DATA TO SERVER =========================
                self.player1pos = (player1.rect.x, player1.rect.y)
                self.player2pos = (player2.rect.x, player2.rect.y)
                if playernumber == 1:
                    self.scoresend = self.player1Score
                else:
                    self.scoresend = self.player2Score

                client.send([playernumber,
                            self.player1pos,self.player2pos,
                            (player1.posession or player2.posession),
                            ball.rect.x, ball.rect.y,
                            self.scoresend])
                #RECEIVE DATA
                #Receiving Format =
                pos_recieved=client.receive()
                print(pos_recieved)

                # Update Player / Ball Positions / Score
                try:
                    if playernumber == 1:
                        player3.update_opponent(pos_recieved[1][0])
                        player4.update_opponent(pos_recieved[1][1])
                    else:
                        player3.update_opponent(pos_recieved[0][0])
                        player4.update_opponent(pos_recieved[0][1])
                except:
                    pass

                try:
                    # print(pos_recieved[3][0],pos_recieved[3][1])
                    ball.rect.x, ball.rect.y = pos_recieved[2][0],pos_recieved[2][1]
                except:
                    pass
                try:
                    self.player1Score, self.player2Score = pos_recieved[3],pos_recieved[4]
                except:
                    pass

                myfont = pygame.font.SysFont(None, 48)


                # Display Score on the Bottom
                label1 = myfont.render(str(self.player1Score), True, (255,255,0))
                label2 = myfont.render("-", True, (255,255,0))
                label3 = myfont.render(str(self.player2Score), True, (255,255,0))
                self.screen.blit(label1, (330, 540))
                self.screen.blit(label2, (395, 540))
                self.screen.blit(label3, (460, 540))

                # Draw All Sprites
                all_sprites.draw(self.screen)
                # Set Frame Rate
                self.clock.tick(50)
                # Draw
                pygame.display.flip()

class goalnet(pygame.sprite.Sprite):
    """
        Goalnet Class - This class is for goalnets.
        Upon initialization, it takes hittest 0, 1, or 2.
        0 = Net
        1 = Side Net Posts to ensure that the ball doesnt go through
        2 = Hitbox of the Next
    """
    def __init__(self, position, hitTest=0):
        # hitTest 0=net, 1=sides, 2=box that determines whether its a goal
        super().__init__()
        if hitTest == 0:
            self.image = pygame.image.load('images/net.jpg')
        elif hitTest == 1:
            self.image = pygame.image.load('images/netbar.png')
        else:
            self.image = pygame.image.load('images/netscore.jpg')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

class Player(pygame.sprite.Sprite):
    """
        Player Class
        This Class is responsible for most of the events that occur involving any player.

    """
    def __init__(self, control, opponent=False):
        super().__init__()
        if opponent == False:
            self.image = pygame.image.load('images/player.png')
        else:
            self.image = pygame.image.load('images/opponent.png')
        self.rect = self.image.get_rect()
        self.accel_x = 0
        self.accel_y = 0
        self.control = control
        self.noball = True
        self.changeready = False
        self.opponent = opponent
        self.posession = False

    # Sets the position in the beginning
    def setPosition(self, position):
        self.rect.x, self.rect.y = position
        self.initialPosition = position

    # Refreshes the player to the initial position
    def refresh(self):
        self.rect.x, self.rect.y = self.initialPosition
        self.accel_x = 0
        self.accel_y = 0
        self.posession = False

    # Updates the position of the opponent player
    def update_opponent(self, coord):
        self.rect.x = coord[0]
        self.rect.y = coord[1]

    # This function handles the movement of the player
    def move(self, ball):
        """ Handles Keys """
        if self.opponent == False:
            key = pygame.key.get_pressed()

            # Movement with Keys
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

                # Decelerate if nothing is pressed
                if sum(key)==0:
                    if self.accel_x > 0:
                        self.accel_x -= 0.5
                    elif self.accel_x < 0:
                        self.accel_x += 0.5
                    if self.accel_y>0:
                        self.accel_y -= 0.5
                    elif self.accel_y<0:
                        self.accel_y += 0.5

                # if ball.canKick == True:
                if self.posession == True:
                    if key[pygame.K_SPACE]:
                        ball.kick()
                        self.posession = False
                        self.control = False

            #Player Automove if not in control
            else:
                if ball.rect.x >= self.rect.x:
                    if self.accel_x < 5:
                        self.accel_x += 0.5
                elif ball.rect.x <= self.rect.x:
                    if self.accel_x > -5:
                        self.accel_x -= 0.5

                self.accel_y = 0

            # Update Player Position
            self.rect.x += self.accel_x
            self.rect.y += self.accel_y

            # Switching players with 'Q'
            if key[pygame.K_q] and self.noball == True:
                if self.changeready == True:
                    if self.control == True:
                        self.control = False
                    else:
                        self.control = True
                    self.changeready = False
            if not key[pygame.K_q] and self.changeready == False:
                self.changeready = True

            # Boundaries of the character
            if self.rect.x <= 0:
                self.rect.x = 0
            elif self.rect.x >= 800-self.rect.width:
                self.rect.x = 800-self.rect.width
            if self.rect.y <= 0:
                self.rect.y = 0
            elif self.rect.y >= 521-self.rect.height:
                self.rect.y = 521-self.rect.height

    # Updates the Player
    def update(self, ball, net_bound):
        # Change the image of the player whether its in control
        # in order to avoid confusion of the player
        if self.control == False:
            self.image = pygame.image.load('images/player.png')
        else:
            self.image = pygame.image.load('images/currplayer.png')

        # Set the player to be in control if its touching the ball
        if pygame.sprite.collide_rect(ball, self):
            self.posession = True
            self.control = True

        # Attach the ball to the player and the ball is within a certain radius
        if self.posession == True and abs(self.rect.y-ball.rect.y)<70:
            ball.attach(self.rect.x, self.rect.y, net_bound)
        else:
            self.posession = False
            ball.attached = False


class SoccerBall(pygame.sprite.Sprite):
    """
        SoccerBall Class
        This class is responsible for events that happens with the soccer ball
    """
    def __init__(self):
        super().__init__()
        # import math
        self.image = pygame.image.load('images/soccerball.jpg').convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.size=self.image.get_rect().size
        self.accel_x, self.accel_y = 0,0
        self.attached = False
        self.mouseX, self.mouseY = 0,0
        self.angleX, self.angleY = 0,0
        self.canKick = True

    # Sets the position of the ball
    def setPosition(self, width, height):
        self.rect.x = width/2-(self.size[0]/2)
        self.rect.y = height/2-(self.size[1]/2)
        self.initialPosition = (self.rect.x, self.rect.y)

    # Refreshes and brings the ball back to the middle
    def refresh(self):
        self.rect.x, self.rect.y = self.initialPosition
        self.attached = False
        self.accel_x, self.accel_y = 0,0

    # Attach the ball to the player
    def attach(self, x, y, net_bound):
        import math
        self.attached = True
        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        # Using Try because sometimes it divides by zero
        try:
            self.angleX = math.acos((self.mouseX-x)/math.hypot(self.mouseX-x,self.mouseY-y))
            self.angleY = math.asin((self.mouseY-y)/math.hypot(self.mouseX-x,self.mouseY-y))
        except:
            pass

        # Moves the ball around the player. If its touching the net, only moves in x-axis
        if pygame.sprite.spritecollide(self, net_bound, False) == []:
            self.rect.y = y+math.sin(self.angleY)*50
        self.rect.x = x+math.cos(self.angleX)*50


    def update(self, net_bound):
        import math

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

        # Apply ball Position according to mouse
        if pygame.sprite.spritecollide(self, net_bound, False) == []:
            self.rect.x += self.accel_x
            self.rect.y += self.accel_y

        # Ball Boundaries
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= (800 - self.rect.width):
            self.rect.x = (800 - self.rect.width)
        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= (521 - self.rect.height):
            self.rect.y = (521 - self.rect.height)
        key = pygame.key.get_pressed()

    # Activates when the ball is kicked
    def kick(self):
        import math
        self.rect.x += (math.cos(self.angleX)*3)
        self.accel_y += (math.sin(self.angleY)*3)
        self.accel_x += (math.cos(self.angleX)*30)
        self.accel_y += (math.sin(self.angleY)*30)
        self.attached = False

# This function is called when the game is started
def start(ip_input, playernumber):
    MainWindow = gameMain(800, 580, 'images/field.png')
    MainWindow.mainLoop(ip_input, playernumber)

# Used ONLY when debugging
if __name__ == "__main__":
    MainWindow = gameMain(800, 580, 'images/field.png')
    MainWindow.mainLoop(ip_input, playernumber)
    # Snake1 = Snake()
