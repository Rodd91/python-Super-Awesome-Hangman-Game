import pygame
from pygame import mixer
import os as operatingSystem
import random
import time
import screeninfo
from screeninfo import get_monitors

operatingSystem.environ['SDL_VIDEO_CENTERED'] = '1'

m = get_monitors()[0]
windowWidth = m.width
windowHeight = m.height

pygame.init()
FPS = 120
#Colors
White=(255,255,255)
Black=(0,0,0)
Blue=(0,0,255)
Yellow=(255,255,0)
Red=(255,0,0)
Green=(0,255,0)
Subtle_Green=(71, 129, 65)
Deepish_Light_Blue=(0, 217, 225)
#Fonts
font_multiplier =10
font_Letters = pygame.font.SysFont(None,font_multiplier*4)
font_Answer_Letters = pygame.font.SysFont(None,font_multiplier*12)
#Display Dimensions

displayDimensions = [int(windowWidth),int(windowHeight-40)]
pygame.display.set_caption('Super Awesome Pinata Game') #Piñata

clock = pygame.time.Clock()
# mixer.init()
# mixer.music.load("music.mp3")
# mixer.music.play(-1)
# mixer.music.set_volume(0.5)
#Button Class
class Button:
    def __init__(self, color, x,y, width, height, label=''):
        self.label = label
        self.height = height
        self.width = width
        self.y = y
        self.x = x
        self.unclicked = True
        self.color = color
        self.isHovering()
    def draw(self, win):
        pygame.draw.ellipse(win, self.color, (self.x,self.y,self.width,self.height), 0)
        if self.label != '':
            text = font_Letters.render(self.label, True, White)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))) #POTENTIAL PROBLEM
    def isHovering(self):
        position = pygame.mouse.get_pos()
        if position[0] > self.x and position[0] < self.x + self.width:
            if position[1] > self.y and position[1] < self.y + self.height:
                return True
        return False



screen = pygame.display.set_mode(displayDimensions, pygame.RESIZABLE)
#clock = pygame.display.Clock()
background = pygame.image.load('fallest2.jpg')

bg = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))

width = 1000

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
def play_game():
    words=["SCARY", "SPIDER", "MONSTER"]
    game_word = random.choice(words)
    wordLength = len(game_word)
    FilledBlanks =[False]*wordLength
    isplaying = True
    letter_btns = []
    blanks = []
    num_wrong = 0
    #BUTTONS 
    alpha_num = 1
    while alpha_num < 11:
        letter_button = Button(Black, displayDimensions[0]*(.205+(alpha_num*.05)), displayDimensions[1]*.70, displayDimensions[0]*.04, displayDimensions[1]*.04,chr(alpha_num+64))
        if letter_button not in letter_btns:
            letter_btns.append(letter_button)
        alpha_num+=1
    while alpha_num < 21:
        letter_button = Button(Black, displayDimensions[0]*(.205+((alpha_num-10)*.05)), displayDimensions[1]*.75, displayDimensions[0]*.04, displayDimensions[1]*.04,chr(alpha_num+64))
        if letter_button not in letter_btns:
            letter_btns.append(letter_button)
        alpha_num+=1
    while alpha_num < 27:
        letter_button = Button(Black, displayDimensions[0]*(.305+((alpha_num-20)*.05)), displayDimensions[1]*.80, displayDimensions[0]*.04, displayDimensions[1]*.04,chr(alpha_num+64))
        if letter_button not in letter_btns:
            letter_btns.append(letter_button)
        alpha_num+=1
    while isplaying:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                new_screen = [event.size[0],event.size[1]-40]
                displayDimensions[0] = int(new_screen[0])
                displayDimensions[1] = int(new_screen[1])
            if event.type == pygame.MOUSEBUTTONDOWN:
                for BTN in letter_btns:
                    if BTN.isHovering():
                        if BTN.unclicked:
                            BTN.unclicked = False
                            if BTN.label in game_word:
                                BTN.color = Green
                                word_index = game_word.index(BTN.label)
                                for i in find(game_word,game_word[word_index]):
                                    if FilledBlanks[i] == False:
                                        FilledBlanks[i] = True
                                        #FIX ME ADD CORRECT LENGTH TO WIN SCREEN
                            else:
                                BTN.color = Red
                            break
                                    
                        
            
        screen.blit(bg, (0,0))
        #BLANKS
        blank_num = 1
        space=0
        while blank_num <= wordLength:
            starting_pos = [displayDimensions[0] * (.39+(blank_num*.05))+space,displayDimensions[1]*.61]
            ending_pos = [starting_pos[0]+(displayDimensions[0]*.03),displayDimensions[1]*.61]
            blanks.append(pygame.draw.line(screen, White, starting_pos, ending_pos,3))
            space+=(displayDimensions[0]*.02)
            blank_num +=1
        #Filling blanks with answers
        for pos in range(len(game_word)): 
            if FilledBlanks[pos]:
                letter_fill = font_Answer_Letters.render(game_word[pos],True, Black)
                screen.blit(letter_fill,(blanks[pos].x + (blanks[pos].width/2 - letter_fill.get_width()/2), blanks[pos].y+ (blanks[pos].height/2 - letter_fill.get_height())))
        alpha_num = 1
        while alpha_num < 11:
            letter_btns[alpha_num-1].draw(screen)
            alpha_num +=1
        while alpha_num < 21:
            letter_btns[alpha_num-1].draw(screen)
            alpha_num +=1
        while alpha_num < 27:
            letter_btns[alpha_num-1].draw(screen)
            alpha_num +=1
        pygame.display.update()
        

def start_screen():
    
    playing = True
    startingBtns = [] 
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #gameEnd()
                pass
            if event.type == pygame.MOUSEMOTION:
                for BTN in startingBtns:
                    if BTN.isHovering():
                        if BTN.unclicked:
                            BTN.color = Yellow
                        else:
                            BTN.color = Black
            if event.type == pygame.MOUSEBUTTONDOWN:
                if startingBtns[0].isHovering():
                    print(startingBtns[0].label + " is clicked")
                    play_game()
                if startingBtns[2].isHovering():
                    #quit_game()
                    pass
                    
            screen.blit(bg, (0,0))
            start_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.4, displayDimensions[0]*.2, displayDimensions[1]*.1,"Play Game")
            start_button.draw(screen)
            if start_button not in startingBtns:
                startingBtns.append(start_button)
            help_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.55, displayDimensions[0]*.2, displayDimensions[1]*.1,"Help")
            help_button.draw(screen)
            if help_button not in startingBtns:
                startingBtns.append(help_button)
            quit_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.7, displayDimensions[0]*.2, displayDimensions[1]*.1,"Quit")
            quit_button.draw(screen)
            if quit_button not in startingBtns:
                startingBtns.append(quit_button)
        clock.tick(FPS)
        pygame.display.update()

def gamePlay():
    start_screen()
    # play_game()
    # gameOver()
gamePlay()
