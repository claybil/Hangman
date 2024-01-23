import pygame
import sys
import random
import time
import nltk
from nltk.corpus import wordnet
import ssl

pygame.init()
clock = pygame.time.Clock()
width = 1400
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Hangman")
icon = pygame.image.load("leg2.png")
pygame.display.set_icon(icon)
game_over = False
row = 2
col = 13
gap = 20
size = 40
boxes = []
for row in range(row):
    for col in range(col):
        x = ((col * gap) + gap) + (size * col) + 500
        y = ((row * gap) + gap) + (size * row) + 400
        box = pygame.Rect(x, y, size, size)
        boxes.append(box)

buttons = []
A = 65

for ind, box in enumerate(boxes):
    letter = chr(A + ind)
    button = [box, letter]
    buttons.append(button)
    
def draw_buttons(buttons):
    for box, letter in buttons:
        btn_text = font.render(letter, True, (0,0,0))
        btn_rect = btn_text.get_rect(center=(box.x+20,box.y+20))
        screen.blit(btn_text, btn_rect)
        pygame.draw.rect(screen, (0,0,0), box, 2)

def display_guess():
    display_text = ''
    for letter in word:
        if letter in guessed:
            display_text += f"{letter} "
        else:
            display_text += '_ '
    text = letter_font.render(display_text,True,(0,0,0))
    screen.blit(text, (400, 200))

images = []
hangman_status = 0

ssl._create_default_https_context = ssl._create_unverified_context
# Download WordNet data (only need to run this once)
nltk.download("wordnet")

def get_random_word():
    synsets = list(wordnet.all_synsets(pos=wordnet.NOUN))
    words = [lemma.name() for synset in synsets for lemma in synset.lemmas()]

    return random.choice(words)

# Example usage:
rand_word = get_random_word()
while len(rand_word) > 10:
    rand_word = get_random_word()

for element in rand_word:
    if element == "_":
        rand_word = get_random_word()

word = rand_word.upper()


#words = ['PYGAME','PYTHON','JAVA','HELLO','WORLD','HANGMAN','TIME','TURTLE','RANDOM']
guessed = []

image = pygame.image.load("hangman.png")
images.append(image)

font = pygame.font.SysFont("arial", 30)
game_font = pygame.font.SysFont("arial", 60)
letter_font = pygame.font.SysFont("arial", 60)

title = "Hangman"
title_text = game_font.render(title, True, (0,0,0))
title_rect = title_text.get_rect(center=(width // 2, title_text.get_height() // 2 + 10))

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = event.pos

            for button, letter in buttons:
                if button.collidepoint(click_pos):
                    if letter not in word:
                        hangman_status += 1
                    if hangman_status == 6:
                        game_over = True
                    guessed.append(letter)
                    buttons.remove([button, letter])

            for i in range(5):
                if hangman_status == 1:
                    image = pygame.image.load("head1.png")
                    images.append(image)
                elif hangman_status == 2:
                    image = pygame.image.load("body.png")
                    images.append(image)
                elif hangman_status == 3:
                    image = pygame.image.load("arm1.png")
                    images.append(image)
                elif hangman_status == 4:
                    image = pygame.image.load("arm2.png")
                    images.append(image)
                elif hangman_status == 5:
                    image = pygame.image.load("leg1.png")
                    images.append(image)
                elif hangman_status == 6:
                    image = pygame.image.load("leg2.png")
                    images.append(image)
                    running = False
                    
    screen.blit(image, (150, 150))
    for box in boxes:
        pygame.draw.rect(screen, (0,0,0), box, 2)
    
    won = True
    for letter in word:
        if letter not in guessed:
            won = False

    if won:
        game_over = True
        game_text = "YOU WON!"
    else:
        game_text = "YOU LOST! THE WORD WAS " + word

    draw_buttons(buttons)
    display_guess()
    screen.blit(title_text, title_rect)
    clock.tick(50)
    pygame.display.update()

    if game_over:
        screen.fill((255, 255, 255))
        text = game_font.render(game_text, True, (0,0,0))
        text_rect = text.get_rect(center=(width//2,height//2))
        screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()
        sys.exit()
pygame.quit()