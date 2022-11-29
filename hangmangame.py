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
#hangman body parts loaded
platform = pygame.image.load('utils/hangpersonparts/hangperson0.png')
head_pic = pygame.image.load('utils/hangpersonparts/hangperson1.png')
torso_pic = pygame.image.load('utils/hangpersonparts/hangperson2.png')
left_arm_pic = pygame.image.load('utils/hangpersonparts/hangperson3.png')
right_arm_pic = pygame.image.load('utils/hangpersonparts/hangperson4.png')
legs_pic = pygame.image.load('utils/hangpersonparts/hangperson5.png')
right_foot_pic = pygame.image.load('utils/hangpersonparts/hangperson6.png')
left_foot_pic = pygame.image.load('utils/hangpersonparts/hangperson7.png')
lose_oof = pygame.image.load('utils/hangpersonparts/hangperson_lose_oof.png')

#resizing body parts to fit window
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
Orange = (255,127,0)
Purple = (221,160,221)
#Fonts
font_multiplier =10
font_Letters = pygame.font.SysFont(None,font_multiplier*4)
font_Answer_Letters = pygame.font.SysFont(None,font_multiplier*12)
#Display Dimensions

displayDimensions = (1600,1000)
pygame.display.set_caption('Super Awesome Family Feud Hangperson Game')
wrong_ctr = 0
score1 = 0
score2 = 0
Player1 = True
Player2 = False
rounds = 1
testing = True #if true play_game display updates
clock = pygame.time.Clock()
# mixer.init()
# mixer.music.load("utils/sound/scary.mp3")
# mixer.music.play(-1, 0.0)
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
background = pygame.image.load('utils/backgrounds/homescreen.jpg')
backgroundChristmas = pygame.image.load('utils/backgrounds/christmas_fireplace.jpg')
backgroundHalloween = pygame.image.load('utils/backgrounds/eerie.jpg')
bg = pygame.transform.scale(background, (pygame.display.Info().current_w, pygame.display.Info().current_h))
bgChristmas = pygame.transform.scale(backgroundChristmas, (pygame.display.Info().current_w, pygame.display.Info().current_h))
bgHalloween = pygame.transform.scale(backgroundHalloween, (pygame.display.Info().current_w, pygame.display.Info().current_h))

width = 1000

#finding if the letter is within the word
def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

#displaying parts of vaquero based on incorrect guesses
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

#Christmas theme version of the game    
def christmas_game():
    global score1
    global score2
    global wrong_ctr
    global testing
    ProperGuess = 0
    global Player1
    global Player2
    global rounds
    words= open('utils/words/ChristmasList.txt').readlines()
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
                                BTN.color = Green #When guessed correctly
                                word_index = game_word.index(BTN.label)
                                for i in find(game_word,game_word[word_index]):
                                    if FilledBlanks[i] == False: # if the letter is not guessed, fill in the blank according to the correctly guessed letter 
                                        FilledBlanks[i] = True
                                        if Player1 == True: #tracking player 1 score
                                            score1+=1
                                            Player1 = True
                                        elif Player2 == True: #tracking player 2 score
                                            score2+=1
                                            Player2 = True
                                        ProperGuess+=1
                                        #Tracking guess length and checking if matches with word length
                                        if ProperGuess == (len(game_word)-1): #Going to next round if word is guessed correctly
                                            ProperGuess = 0
                                            rounds+=1
                                            wrong_ctr = 0
                                            christmas_game()

                                        if wrong_ctr == 8: #Going to next round if incorrect guesses are used up
                                             rounds+=1
                                             wrong_ctr = 0
                                             score1 = 0
                                             christmas_game() 
                            else:
                                BTN.color = Red #when guessed incorrectly
                                wrong_ctr+=1       #counter tracking the number of wrong guesses 
                                if Player1 == True:     #determining whos turn it is
                                     Player2 = True
                                     Player1 = False

                                elif Player2 == True:  #determining whos turn it is
                                    Player1 = True
                                    Player2 = False
                                if wrong_ctr >= 8: #checking if the total number of wrong guesses >= 8
                                    rounds+=1
                                    wrong_ctr = 0
                                    christmas_game() 

                            break
        if rounds > 5: #After 5 rounds the game ends
            screen.blit(bgChristmas, (0,0))
            alpha_num = 0
            wrong_ctr = 0
            testing = False
            end_screen()    

                        
            
        screen.blit(bgChristmas, (0,0))
        drawVaquero(screen, wrong_ctr)
        score = font_Letters.render("Player1 Score: " + str(score1), True, Green)
        screen.blit(score, (windowWidth-650,windowHeight-250))
        scoreOth = font_Letters.render("Player2 Score: " + str(score2), True, Red)
        screen.blit(scoreOth, (windowWidth-650,windowHeight-200))
        
        roundslimit = font_Letters.render("ROUND: " + str(rounds), True, White)

        screen.blit(roundslimit, (windowWidth-650,windowHeight-150))
        #BLANKS displaying and determined amount by word length
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
           
#halloween theme version of the game          
def halloween_game():
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
    print(game_word) #printing the word to console for quick access & debugging
    #game letter buttons/keys
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
                                BTN.color = Orange
                                word_index = game_word.index(BTN.label)
                                for i in find(game_word,game_word[word_index]):
                                    if FilledBlanks[i] == False:
                                        FilledBlanks[i] = True
                                        if Player1 == True:
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
                                            halloween_game()

                                        if wrong_ctr == 8:
                                             rounds+=1
                                             wrong_ctr = 0
                                             score1 = 0
                                             halloween_game() 
                            else:
                                BTN.color = Purple
                                wrong_ctr+=1
                                if Player1 == True:
                                     Player2 = True
                                     Player1 = False

                                elif Player2 == True:
                                    Player1 = True
                                    Player2 = False
                                if wrong_ctr >= 8:
                                    rounds+=1
                                    wrong_ctr = 0
                                    halloween_game() 

                            break
        if rounds > 5:
            screen.blit(bg, (0,0))
            alpha_num = 0
            wrong_ctr = 0
            testing = False
            end_screen()    

                        
            
        screen.blit(bgHalloween, (0,0))
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


def help_screen():
    helptrue = True
    while helptrue:
        screen.blit(bg,(0,0))
        help_text = font_Letters.render("Welcome to Super Awesome Hangperson Pinata Game.", True, Orange)
        screen.blit(help_text, (windowWidth/25, windowHeight/4))      
        help_text2 = font_Letters.render("A two player turn based game.", True, Orange)
        screen.blit(help_text2, (windowWidth/25, windowHeight/3.5))
        help_text3 = font_Letters.render("Players take turns guessing letters to complete the word.", True, Orange)
        screen.blit(help_text3, (windowWidth/25, windowHeight/3.0))   
        help_text4 = font_Letters.render("Turns switch once the player makes an incorrect guess.", True, Orange)
        screen.blit(help_text4, (windowWidth/25, windowHeight/2.7)) 
        help_text5 = font_Letters.render("Score is accumulated for letters guessed correctly over the course of 5 rounds.", True,Orange)
        screen.blit(help_text5, (windowWidth/25, windowHeight/2.3)) 
        help_text6 = font_Letters.render("Highest score after 5 rounds wins.", True, Orange)
        screen.blit(help_text6, (windowWidth/25, windowHeight/1.9)) 
        help_text7 = font_Letters.render("After 8 incorrect guesses accumulated amongst both players, the round is over and a new word is given", True, Orange)
        screen.blit(help_text7, (windowWidth/25, windowHeight/1.5)) 
        help_text8 = font_Letters.render("Press 'Q' to go back ", True, Orange)
        screen.blit(help_text8, (windowWidth/25, windowHeight/1.2)) 
        pygame.key.set_repeat(1,25)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    start_screen()
        pygame.display.update()

#Screen showing up after 5 rounds occur in game
def end_screen():
    global score1
    global score2
    global testing
    screen.blit(bg,(0,0))
    #Displays player 1s score
    score = font_Letters.render("Player1 Score: " + str(score1), True, Green)
    screen.blit(score, (windowWidth/2, windowHeight/5))
    #Displays player 2s score
    scoreOth = font_Letters.render("Player2 Score: " + str(score2), True, Green)
    screen.blit(scoreOth, (windowWidth/2, windowHeight/4))
    #Displays whether the players tie, or whichever player has a higher score
    if score1 > score2:
        scoreWinner = font_Letters.render("Player 1 WINS THE GAME: " + str(score1), True, Green)
    elif score2 > score1:
        scoreWinner = font_Letters.render("Player 2 WINS THE GAME: " + str(score2), True, Green)
    elif score1 == score2:
        scoreWinner = font_Letters.render("BOTH PLAYERS TIED", True, Green)
    screen.blit(scoreWinner, (windowWidth/2, windowHeight/3))
    #Displays what button the player needs to click to quit the game
    ToQuit = font_Letters.render("PRESS Q TO QUIT THE GAME", True, Green)
    screen.blit(ToQuit, (windowWidth/2, windowHeight/2.5))
    pygame.key.set_repeat(1,25)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
             pygame.quit()
    pygame.display.update()

#The screen displaying which themes to choose from
def choose_theme():
    choosing = True
    startingBtns = []
    while choosing:
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
                    christmas_game()
                if startingBtns[1].isHovering():
                    halloween_game()
                if startingBtns[2].isHovering():
                    pygame.quit()
#theme selection buttons
            screen.blit(bg, (0,0))
            Halloween_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.4, displayDimensions[0]*.2, displayDimensions[1]*.1,"Christmas Theme")
            Halloween_button.draw(screen)
            if Halloween_button not in startingBtns:
                startingBtns.append(Halloween_button)
            Christmas_button = Button(Black,  displayDimensions[0]*.4, displayDimensions[1]*.55, displayDimensions[0]*.2, displayDimensions[1]*.1,"Halloween Theme")
            Christmas_button.draw(screen)
            if Christmas_button not in startingBtns:
                startingBtns.append(Christmas_button)
        clock.tick(FPS)
        pygame.display.update()   

#The screen that appears when the game is started
#Displays options that the player may click
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
                    choose_theme()
                if startingBtns[1].isHovering():
                    help_screen()
                if startingBtns[2].isHovering():
                    pygame.quit()
            #Buttons showing options the player can click
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
gamePlay()