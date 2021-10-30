import pygame
import os
import random
import sys
import neat
import math

pygame.init()

# Global Variables
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1100
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
GEN = 0

DINO_RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
                pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

DINO_JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]

LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)

class Dinossaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VELOCITY = 8.5
    
    def __init__(self, img=DINO_RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VELOCITY
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.step_index = 0
    
    def update(self):
        if self.dino_run:
            self.run()
            
        if self.dino_jump:
            self.jump()
        
        if self.step_index >= 10:
            self.step_index = 0
    
    def jump(self):
        self.image = DINO_JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        
        if self.jump_vel <= -self.JUMP_VELOCITY:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VELOCITY
        
    def run(self):
        self.image = DINO_RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1
        
    def draw(self, WINDOW):
        WINDOW.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(WINDOW, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 4)
        for obstacle in obstacles:
            pygame.draw.line(WINDOW, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 3)

class Obstacle:
    def __init__(self, image, number_of_cactus):
        self.image = image
        self.type = number_of_cactus
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WINDOW_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, WINDOW):
        WINDOW.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cactus):
        super().__init__(image, number_of_cactus)
        self.rect.y = 300

def remove(index):
    dinossaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2+dy**2)

def displayScore():
    global score, game_speed, dino_population
    score += 1
    if score % 100 == 0:
        game_speed += 1
        
    score_draw = FONT.render("Score: " + str(score), 1, (0,0,0))
    WINDOW.blit(score_draw, (950,50))
    fps_draw = FONT.render("Speed: " + str(game_speed), 1, (0,0,0))
    WINDOW.blit(fps_draw, (950,70))
    pop_draw = FONT.render("Pop: " + str(len(dinossaurs)), 1, (0,0,0))
    WINDOW.blit(pop_draw, (950,90))
    pop_draw = FONT.render("Gen: " + str(GEN), 1, (0,0,0))
    WINDOW.blit(pop_draw, (950,110))

def background():
    global x_pos_bg, y_pos_bg
    image_width = BACKGROUND.get_width()
    WINDOW.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
    WINDOW.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
    if x_pos_bg <= -image_width:
        x_pos_bg = 0
        
    x_pos_bg -= game_speed

def fitnessFunction(genomes, config):
    
    global game_speed, x_pos_bg, y_pos_bg, score, obstacles, ge, nets, dinossaurs, GEN
    
    clock = pygame.time.Clock()
    score = 0
    GEN += 1
    obstacles = []
    dinossaurs = []
    ge = []
    nets = []
    
    x_pos_bg = 0
    y_pos_bg = 380
    
    game_speed = 30

    for genome_id, genome in genomes:
        dinossaurs.append(Dinossaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        WINDOW.fill((255, 255, 255))
        
        for dinossaur in dinossaurs:
            dinossaur.update()
            dinossaur.draw(WINDOW)

        if len(dinossaurs) == 0:
            break
        
        if len(obstacles) == 0:
            rand_int = random.randint(0, 1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))

        for obstacle in obstacles:
            obstacle.draw(WINDOW)
            obstacle.update()
            for i, dino in enumerate(dinossaurs):
                if dino.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)

        #user_input = pygame.key.get_pressed()
        
        for i, dino in enumerate(dinossaurs):
            output = nets[i].activate((dino.rect.y,
                                        distance((dino.rect.x, dino.rect.y),
                                        obstacle.rect.midtop)))
            if output[0] > 0.5 and dino.rect.y == dino.Y_POS:
                dino.dino_jump = True
                dino.dino_run = False
        
        displayScore()
        background()
        clock.tick(game_speed)
        pygame.display.update()
        

# NEAT Setup
def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    global dino_population 
    dino_population = neat.Population(config)
    dino_population.run(fitnessFunction, 50)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)