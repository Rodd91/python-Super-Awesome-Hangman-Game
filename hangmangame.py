import pygame
from pygame import mixer
import os as operatingSystem
import random
import time
import screeninfo
from screeninfo import get_monitors
m = get_monitors()[0]
windowWidth = m.width
windowHeight = m.height
#Pictures
platform = pygame.image.load('utils/hangpersonparts/hangperson0.png')
head_pic = pygame.image.load('utils/hangpersonparts/hangperson1.png')
torso_pic = pygame.image.load('utils/hangpersonparts/hangperson2.png')
left_arm_pic = pygame.image.load('utils/hangpersonparts/hangperson3.png')
right_arm_pic = pygame.image.load('utils/hangpersonparts/hangperson4.png')
legs_pic = pygame.image.load('utils/hangpersonparts/hangperson5.png')
right_foot_pic = pygame.image.load('utils/hangpersonparts/hangperson6.png')
left_foot_pic = pygame.image.load('utils/hangpersonparts/hangperson7.png')
lose_oof = pygame.image.load('utils/hangpersonparts/hangperson_lose_oof.png')
#operatingSystem.environ['SDL_VIDEO_CENTERED'] = '1'
platform = pygame.transform.scale(platform, (windowWidth/3,windowHeight/2))
head_pic = pygame.transform.scale(head_pic, (windowWidth/3,windowHeight/2))
torso_pic = pygame.transform.scale(torso_pic, (windowWidth/3,windowHeight/2))
left_arm_pic= pygame.transform.scale(left_arm_pic, (windowWidth/3,windowHeight/2))
right_arm_pic = pygame.transform.scale(right_arm_pic, (windowWidth/3,windowHeight/2))
legs_pic = pygame.transform.scale(legs_pic, (windowWidth/3,windowHeight/2))
right_foot_pic = pygame.transform.scale(right_foot_pic, (windowWidth/3,windowHeight/2))
left_foot_pic = pygame.transform.scale(left_foot_pic, (windowWidth/3,windowHeight/2))
lose_oof = pygame.transform.scale(lose_oof, (windowWidth/3,windowHeight/2))


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

displayDimensions = (1600,1000)#[int(windowWidth),int(windowHeight-40)]
pygame.display.set_caption('Super Awesome Family Feud Hangperson Piñata Game') #Piñata
wrong_ctr = 0
score1 = 0
score2 = 0
Player1 = True
Player2 = False
rounds = 0
testing = True #if true play_game display updates
clock = pygame.time.Clock()
# mixer.init()
# mixer.music.load("utils/sound/scary.mp3")
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
background = pygame.image.load('utils/backgrounds/eerie3.jpg')
backgroundChristmas = pygame.image.load('utils/backgrounds/christmas_fireplace.jpg')
bg = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))
bgChristmas = pygame.transform.scale(backgroundChristmas, (pygame.display.Info().current_w, pygame.display.Info().current_h))
width = 1000

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]
# def quitGame():
#     pygame.quit()
#     exit()
def drawVaquero(window, num_guesses):
    if num_guesses == 0:
        screen.blit(platform, (windowWidth/25,windowHeight/12))
    elif num_guesses == 1:
        window.blit(head_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 2: 
        window.blit(torso_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 3:
        window.blit(left_arm_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 4:
        window.blit(right_arm_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 5:
        window.blit(legs_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 6:
        window.blit(right_foot_pic, (windowWidth/25,windowHeight/12))
    elif num_guesses == 7:
        window.blit(left_foot_pic, (windowWidth/25,windowHeight/12))
    else:
        window.blit(lose_oof, (windowWidth/25,windowHeight/12))

def play_game():
    #Variables 
    
    global score1
    global score2
    global wrong_ctr
    global testing
    ProperGuess = 0
    global Player1
    global Player2
    global rounds
    words= open('utils/words/halloweenList.txt').readlines()
    game_word = random.choice(words)
    wordLength = len(game_word)
    FilledBlanks =[False]*wordLength
    isplaying = True
    letter_btns = []
    blanks = []
    print(game_word) ##FIXME
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
                                        if Player1 == True:
                                            #screen.blit(turn, (windowWidth-650,windowHeight-150))
                                            score1+=1
                                            Player1 = True
                                        elif Player2 == True:
                                            score2+=1
                                            Player2 = True
                                        ProperGuess+=1
                                        if ProperGuess == (len(game_word)-1):
                                            ProperGuess = 0
                                            rounds+=1
                                            wrong_ctr = 0
                                            play_game()

                                        if wrong_ctr == 8:
                                             rounds+=1
                                             wrong_ctr = 0
                                             score1 = 0
                                             play_game() 
                                        #FIX ME ADD CORRECT LENGTH TO WIN SCREEN
                            else:
                                BTN.color = Red
                                wrong_ctr+=1
                                if Player1 == True:
                                     Player2 = True
                                     Player1 = False

                                elif Player2 == True:
                                    Player1 = True
                                    Player2 = False
                                if wrong_ctr > 8:
                                    rounds+=1
                                    wrong_ctr = 0
                                    play_game() 

                            break
        if rounds >= 3:
            screen.blit(bg, (0,0))
            alpha_num = 0
            wrong_ctr = 0
            testing = False
            end_screen()    

                        
            
        screen.blit(bg, (0,0))
        drawVaquero(screen, wrong_ctr)
        score = font_Letters.render("Player1 Score: " + str(score1), True, White)
        screen.blit(score, (windowWidth-650,windowHeight-250))
        scoreOth = font_Letters.render("Player2 Score: " + str(score2), True, White)
        screen.blit(scoreOth, (windowWidth-650,windowHeight-200))
        
        roundslimit = font_Letters.render("ROUND: " + str(rounds), True, White)

        screen.blit(roundslimit, (windowWidth-650,windowHeight-150))
        #BLANKS
        blank_num = 1
        space=0
        while blank_num < wordLength:
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
        drawVaquero(screen, wrong_ctr)
        if testing == True:
            pygame.display.update()
        
def end_screen():
    global score1
    global score2
    global testing
    screen.blit(bg,(0,0))
    score = font_Letters.render("Player1 Score: " + str(score1), True, Red)
    screen.blit(score, (windowWidth/2, windowHeight/5))

    scoreOth = font_Letters.render("Player2 Score: " + str(score2), True, Red)
    screen.blit(scoreOth, (windowWidth/2, windowHeight/4))

    if score1 > score2:
        scoreWinner = font_Letters.render("Player 1 WINS THE GAME: " + str(score1), True, Red)
    elif score2 > score1:
        scoreWinner = font_Letters.render("Player 2 WINS THE GAME: " + str(score2), True, Red)
    elif score1 == score2:
        scoreWinner = font_Letters.render("BOTH PLAYERS TIED", True, Red)
    screen.blit(scoreWinner, (windowWidth/2, windowHeight/3))
    ToQuit = font_Letters.render("PRESS Q TO QUIT THE GAME", True, Red)
    screen.blit(ToQuit, (windowWidth/2, windowHeight/2.5))
    pygame.key.set_repeat(1,25)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
             pygame.quit()
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
            Halloween_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.55, displayDimensions[0]*.2, displayDimensions[1]*.1,"Halloween Theme")
            Halloween_button.draw(screen)
            if Halloween_button not in startingBtns:
                startingBtns.append(Halloween_button)
            Christmas_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.55, displayDimensions[0]*.2, displayDimensions[1]*.1,"Christmas Theme")
            Christmas_button.draw(screen)
            if Christmas_button not in startingBtns:
                startingBtns.append(Christmas_button)
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
gamePlay()