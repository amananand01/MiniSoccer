import pygame
import socket
from game import start


class Option:
    def __init__(self, text, position, go_to_page, hoverable, color=(0,0,0), fontsize=40):
        '''
        Create an instance of the Option class which has a position, rect_size,
        text, hoverable or not, color and its font size.
        '''
        self.text = text
        self.black = color
        self.red = (255,100,255)
        self.hovered = False
        self.menuFont = pygame.font.Font(None, fontsize)
        self.rend = self.menuFont.render(self.text, True, (0,0,0))
        self.rect = self.rend.get_rect()
        self.rect.center = position
        self.go_to_page = go_to_page
        self.hoverable = hoverable

    def update(self,screen):
        '''
        Updating the screen:
        Checks if hoverable is True and mouse gets colided on rect_text.
        Creates a new Surface with the specified text rendered on it.
        Drawing the text font on the screen.
        '''
        if self.hoverable and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

        # creates a new Surface with the specified text rendered on it.
        self.rend = self.menuFont.render(self.text, True, self.get_color())
        screen.blit(self.rend, self.rect)

    def get_color(self):
        '''
        Changes the color of text to red if hoovered is True else black.
        '''
        if self.hovered:
            return self.red
        else:
            return self.black

    def checkpress(self):
        '''
        Checks if hovered and mouse gets clicked on text.
        Returns: True if its clicked else False.
        '''
        if self.hovered and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

class Menu:
    def __init__(self):
        '''
        Create an instance of the menu class having a background_image, page no,
        ip_address, choice which is of type bool, setip as setting ip address if
        setip True, ip_input which is to be inputted by the user.
        '''
        self.screen = pygame.display.set_mode((800,521))
        self.background_image = pygame.image.load('images/background.png')
        self.choice = False
        self.page = 0
        self.ip_address = "Gettting IP Adress"
        self.setip = False
        self.ip_input = ""

    def MainMenu(self):
        '''
        Main loop for running all the menu screens.
        '''

        # loads the title of the game on the screen
        title_image = pygame.image.load('images/title.png')

        # try to get the ip address if not able to then prints an alert message
        # on screen
        try:
            self.ip_address = socket.gethostbyname(socket.gethostname())
        except:
            self.ip_address = "Cannot get your IP. Manually Do it"
            self.setip = True

        done = True # loop runs till done=True

        while done:

            # drawing the background_image on screen
            self.screen.blit(self.background_image,(0,0))

            # checks:
            # if user pressed Escape then exit
            # else check for the ip_input entered by the user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    done = False
                elif event.type == pygame.KEYDOWN and self.page == 1:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.ip_input) > 0:
                            self.ip_input = self.ip_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.page = 4
                    else:
                        try:
                            self.ip_input += str(event.unicode)
                        except:
                            pass

            # First page of the menu screen
            if self.page == 0:
                options = [Option("New Game", (400, 350), 1, True),
                            Option("Instructions", (400, 400), 2, True),
                            Option("Options", (400, 450), 3, True)]
                self.screen.blit(title_image, (50,100))

            # Second page of the menu screen showing the ip_address
            elif self.page == 1:

                # checks if ip_input is entered by user & if yes then show it
                # on screen else show 0.0.0
                if len(self.ip_input) == 0:
                    options = [
                                Option("Your IP Adress is:", (400, 100), 0, False),
                                Option(self.ip_address, (400,150), 0, False, (100, 255, 255)),
                                Option("Input your partner's IP adress", (400, 225), 0, False),
                                Option("0.0.0.0", (400, 275), 0, False, (100, 100, 255)),
                                Option("Start Game", (400, 450), 4, True, (0, 76, 255)),
                                Option("Go back", (250, 450), 0, True)]
                else:
                    options = [
                                Option("Your IP Adress is:", (400, 100), 0, False),
                                Option(self.ip_address, (400,150), 0, False, (100, 255, 255)),
                                Option("Input your partner's IP adress", (400, 225), 0, False),
                                Option(self.ip_input, (400, 275), 0, False,(100, 100, 255)),
                                Option("Start Game", (400, 450), 4, True, (0, 76, 255)),
                                Option("Go back", (250, 450), 0, True)]

            # Third page of the menu screen showing Instructions to play
            elif self.page == 2:
                options = [Option("Keys: W,A,S,D to Move", (400, 200), 0, False),
                            Option("Space bar to Shoot", (400, 250), 0, False),
                            Option("Mouse to Aim", (400, 300), 0, False),
                            Option("Go back", (250, 450), 0, True)]

            # Fourth page of the menu screen showing our names
            elif self.page == 3:
                options = [
                            Option("Made by", (400, 250), 0, False),
                            Option("Andrew Park and Aman Anand", (400, 300), 0, False),
                            Option("Go back", (250, 450), 0, True)]

            # Fifth page of the menu screen to ask for player no
            elif self.page == 4:
                options = [Option("Are you player 1 or player 2?", (400, 200), 0, False),
                            Option("Player 1", (300, 350), 5, True),
                            Option("Player 2", (500, 350), 6, True)]


            # Start Game as player1
            elif self.page == 5:
                start(self.ip_input, 1)
                break
            # Start Game as player2
            elif self.page == 6:
                start(self.ip_input, 2)
                break

            # update all options
            for option in options:
                option.update(self.screen)
                self.choice = option.checkpress()
                if self.choice == True:
                    self.page = option.go_to_page
                    break

            # updating the pygame screen everytime
            pygame.display.flip()

# initializing the pygame modules
pygame.init()

# creating an object of class Menu and and running Mainmenu Screen
menu=Menu()
menu.MainMenu()
