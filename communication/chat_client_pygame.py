try:    name = raw_input("Enter a screen name: ")
except: name =     input("Enter a screen name: ")

import pygame
from pygame.locals import *
import traceback
pygame.display.init()
pygame.font.init()
screen_width=600
screen_height=600
screen = pygame.display.set_mode([screen_width,screen_height])
from mastermind_import import *
from settings import *
import chat_server

# screen_size = [400,300]
icon = pygame.Surface((1,1)); icon.set_alpha(0); pygame.display.set_icon(icon)
pygame.display.set_caption("Mastermind Chat Example - Ian Mallett - v.1.02 - 2013")
# surface = pygame.display.set_mode(screen_size,RESIZABLE)

pygame.key.set_repeat(400,25)
x1,y1=500,30
client = None
server = None

log = [None]*scrollback
import json
message = ""
to_send = [
    ["introduce",name]
]

font = pygame.font.SysFont("Times New Roman",12)
clock = pygame.time.Clock()
def get_input():
    global surface, screen_size, message
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if   event.type == QUIT: return False
        elif event.type == KEYDOWN:
            if   event.key == K_ESCAPE: return False
            elif event.key == K_RETURN:
                if message != "":
                    to_send.append(["add",""+name+": "+message])
                    message = ""
            elif event.key == K_BACKSPACE:
                if len(message) > 0:
                    message = message[:-1]
            else:
                try: message += str(event.unicode)
                except: pass
        # elif event.type == VIDEORESIZE:
        #     surface = pygame.display.set_mode(event.size,RESIZABLE)
        #     screen_size = event.size
    return True

def send_next_blocking():
    global log, to_send, continuing
    global x1,y1
    print("ssssss",x1,y1)
    try:
        if len(to_send) == 0:
            client.send(["update"],None)
        else:
            client.send(to_send[0],None)
            to_send = to_send[1:]

        reply = None
        while reply == None:
            reply = client.receive(False)
        log = reply
        # for i in reply:
        #     print(i)
        # print(log)
        # print()
        # try:
        # print("in try")
        print(reply[2])

        print(reply[2].split(" ",1))
        s=reply[2].split(" ",1)
        g=s[1]
        print("pp",g , type(g))
        try:
            b=json.loads(g)
            print(b)
            if b['x'] > 0 and b['x']<500:
                x1 = b["x"]
            if b['y'] > 0 and b['y']<500:
                y1 = b['y']
        except:
            print("==")
        # print(reply[2][20:23] , reply[2][])
    except MastermindError:
        continuing = False

def draw():
    for event in pygame.event.get():
            if event.type == pygame.QUIT and event.key == pygame.K_ESCAPE:
                pygame.quit()
    print("aaa")
    global x1,y1
    print("kkkkkk",x1,y1)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y1 -= 3
    if pressed[pygame.K_DOWN]: y1 += 3
    if pressed[pygame.K_LEFT]: x1 -= 3
    if pressed[pygame.K_RIGHT]: x1 += 3

    screen.fill((0, 0, 0))
    color1 = (255, 0, 0)
    pygame.draw.rect(screen, color1, pygame.Rect(x1, y1, 10, 80))

    pygame.display.flip()
    clock.tick(60)

def main():
    global client, server, continuing

    client = MastermindClientTCP(client_timeout_connect,client_timeout_receive)
    try:
        print("Client connecting on \""+client_ip+"\", port "+str(port)+" . . .")
        client.connect(client_ip,port)
    except MastermindError:
        print("No server found; starting server!")
        server = chat_server.ServerChat()
        server.connect(server_ip,port)
        server.accepting_allow()

        print("Client connecting on \""+client_ip+"\", port "+str(port)+" . . .")
        client.connect(client_ip,port)
    print("Client connected!")

    clock = pygame.time.Clock()
    continuing = True
    while continuing:
        if not get_input():
            to_send.append(["leave",name])
            send_next_blocking()
            break
        send_next_blocking()
        draw()
        clock.tick(60)
    pygame.quit()

    client.disconnect()

    if server != None:
        server.accepting_disallow()
        server.disconnect_clients()
        server.disconnect()
if __name__ == "__main__":
    try:
        main()
    except:
        traceback.print_exc()
        pygame.quit()
        input()
