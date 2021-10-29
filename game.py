import pygame
import os
import random
import sys

pygame.init()

# Global Variables
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 1100
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

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

def main():
    
    global game_speed, x_pos_bg, y_pos_bg, score
    
    clock = pygame.time.Clock()
    score = 0
    fps = 30
    
    dinossaurs = [Dinossaur()]
    
    x_pos_bg = 0
    y_pos_bg = 380
    
    game_speed = 20
    
    def displayScore():
        global score, game_speed
        score += 1
        if score % 100 == 0:
            game_speed += 1
            
        score_draw = FONT.render("Score: " + str(score), 1, (0,0,0))
        WINDOW.blit(score_draw, (950,50))
        
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BACKGROUND.get_width()
        WINDOW.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        WINDOW.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
            
        x_pos_bg -= game_speed
        
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
        
        user_input = pygame.key.get_pressed()
        
        for i, dino in enumerate(dinossaurs):
            if user_input[pygame.K_SPACE]:
                dino.dino_jump = True
                dino.dino_run = False
        
        displayScore()
        background()
        clock.tick(fps)
        pygame.display.update()
        
        
if __name__ == "__main__":
    main()