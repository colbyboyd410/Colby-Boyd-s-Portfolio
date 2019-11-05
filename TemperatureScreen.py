#################################################################
#AUTHOR = JENNIFER JUNG, COLBY BOYD, ALAYNA JUNEAU
#TITLE = Tempoify
#Discription = This is the code for Tempoify. This is a game about
#		using your temperature to choose a song for you to
#		play a game with.
#Date = November 8, 2019
###################################################################

import pygame
import time
# Import the ADS1x15 module.
import Adafruit_ADS1x15

pygame.init()
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
GAIN = 1
# Start continuous ADC conversions on channel 0 using the previously set gain value.
adc.start_adc(1 , gain=GAIN)

# width and height of the screen
display_width = 800
display_height =450
gameDisplay = pygame.display.set_mode((display_width, display_height))
# load the image for the background
background = pygame.image.load("background.jpg")
# scale it so that it won't be pixelated!
background = pygame.transform.scale(background,(display_width,display_height))
# title of this program
pygame.display.set_caption('Tempoify')

# RGB needed to make the colors
white = (255, 255, 255)
blue = (0, 0, 128)
sky_blue = (122, 215, 240)
diamond = (183, 233, 247)

# help track time
clock = pygame.time.Clock()

# get fonts
smallfont = pygame.font.SysFont("tahoma", 25)
medfont = pygame.font.SysFont("tahoma", 50)
largefont = pygame.font.SysFont("tahoma", 75)

def text_objects(text, color, size="small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

# function that allows button to be created
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = round(buttonx + (buttonwidth / 2)), round(buttony + (buttonheight / 2))
    gameDisplay.blit(textSurf, textRect)

# function that allows message to be created
def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    x = int(round((display_width / 2)))
    y = int(round((display_height / 2) + y_displace))

    textRect.center = x, y
    gameDisplay.blit(textSurf, textRect)

def pause():
    paused = True
    message_to_screen("Paused",blue,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit", blue, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()        
        clock.tick(5)

# function to check if cursor is close to button and if user clicks it
def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
        if click[0] == 1 and action != None:
            if action == "play":
                import Main_Game
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
        text_to_button(text, blue, x, y, width, height)

# function to get the temperature of a person
def getValues():
    # Read channel 0 for 5 seconds and print out its values.
    start = time.time()
    while (time.time() - start) <= 1.0:
        # Read the last ADC conversion value
        value = adc.get_last_result()
    if value <= 19999:
        # returns a value that plays the slow song
        return 20
    elif value >= 21999:
        # returns a value that plays the fast song
        return 46
    else:
        # returns a value that plays the medium song
        return 30

def game_intro():
    intro = True
    while intro:
        gameDisplay.blit(background,(0,0))
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        # show messages on the screen for the user to read
        message_to_screen("Now, please pinch the thermistor!", blue, -100)
        message_to_screen("It will immediately start measuring your temperature.", blue, -50)
        message_to_screen("The song and tempo and will be fast, neutral, or slow according", blue, 0)
        message_to_screen("to your temperature. Press the Play button when you are ready!", blue, 50)
        # create the button
        button("Play", 350, 300, 100, 50, sky_blue, diamond, action="play")
        # update the screen so that everything appears one the screen, otherwise, it will be a black screen!
        pygame.display.update()
        clock.tick(15)

game_intro()
adc.stop_adc()
