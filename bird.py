import pygame, random
from brain import Brain

class Bird(pygame.sprite.Sprite):
    def __init__(self, id, x, y, population, game):
        super().__init__()
        self.id = id
        self.game = game
        self.isKilled = False
        self.result = 0
        self.population = population
        self.brain = Brain()
        self.image = pygame.Surface([30, 30])
        self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.force = 0.0

    def killed(self, result):
        self.result = result
        self.isKilled = True
        if result > self.game.best:
            self.game.best = result
        
        self.kill()

    def update(self):
        if self.isKilled:
            return
        
        next_block_data = self.game.getNextBottomBlockData()
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