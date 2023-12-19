# Add background image and music

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.png").convert_alpha()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,14)*SIZE
        self.y = random.randint(1,9)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image2 = pygame.image.load("resources/block_head.png").convert()
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]  # El primer bloque, ahora será representado por image2
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # Actualizar el cuerpo de la serpiente
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # Actualizar la cabeza de la serpiente
        if self.direction == 'left':
            self.x[0] -= SIZE
            if self.x[0] < 0:  # Si se cruza por el lado izquierdo
                self.x[0] = 600 - SIZE  # Aparece en el lado derecho
        if self.direction == 'right':
            self.x[0] += SIZE
            if self.x[0] >= 600:  # Si se cruza por el lado derecho
                self.x[0] = 0  # Aparece en el lado izquierdo
        if self.direction == 'up':
            self.y[0] -= SIZE
            if self.y[0] < 0:  # Si se cruza por arriba
                self.y[0] = 400 - SIZE  # Aparece abajo
        if self.direction == 'down':
            self.y[0] += SIZE
            if self.y[0] >= 400:  # Si se cruza por abajo
                self.y[0] = 0  # Aparece arriba

        self.draw()

    def draw(self):
        for i in range(self.length):
            if i == 0:  # Si es la cabeza
                self.parent_screen.blit(self.image2, (self.x[i], self.y[i]))
            else:
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    # Resto del código sin cambios

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Codebasics Snake And Apple Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((600, 400))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music.mp3')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/comiendo.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))
        
    def render_background(self):
        bg_m = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg_m, (0,0))
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.Font("resources/Minecraft.ttf",30)
        score = font.render(f"{self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(290,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.Font("resources/Minecraft.ttf", 20)
        line1 = font.render(f"Game is over! Tu puntuaje es {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (HAT_CENTERED, 175))
        line2 = font.render("Para jugar de nuevo, presiona enter.", True, (255, 255, 255))
        self.surface.blit(line2, (HAT_CENTERED , 200))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == '__main__':
    game = Game()
    game.run()