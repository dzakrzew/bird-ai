import pygame, random
from brain import Brain

class Bird(pygame.sprite.Sprite):
    IMGS = [pygame.image.load("sprites/bird1.png"),pygame.image.load("sprites/bird2.png"),pygame.image.load("sprites/bird3.png")]
    def __init__(self, id, x, y, population, game):
        super().__init__()
        self.id = id
        self.game = game
        self.is_killed = False
        self.result = 0
        self.population = population
        self.brain = Brain()
        self.image = self.IMGS[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.force = 0.0
        self.img_count = 0

    def killed(self, result):
        self.result = result
        self.is_killed = True
        if result > self.game.best:
            self.game.best = result
        
        self.kill()
    def update_sprite(self,win):
        self.img_count += 1

        if self.img_count < 5:
            self.image = self.IMGS[0]
        elif self.img_count < 10:
            self.image = self.IMGS[1]
        elif self.img_count < 15:
            self.image = self.IMGS[2]
        elif self.img_count < 20:
            self.image = self.IMGS[1]
        elif self.img_count < 21:
            self.image = self.IMGS[0]
            self.img_count=0



    def update(self):
        if self.is_killed:
            return
        
        next_block_data = self.game.get_next_bottom_block_data()
        next_block_distance = next_block_data['x'] - 100
        next_block_height_diff = next_block_data['y'] - self.rect.y - 60

        dec = self.brain.decision(next_block_distance, next_block_height_diff)

        if dec == Brain.DECISION_JUMP:
            self.jump()

        self.rect.y -= self.force
        self.force = max(self.force - 0.1, -5.0)
        self.mask = pygame.mask.from_surface(self.image)

    def jump(self):
        self.force = 3.0
