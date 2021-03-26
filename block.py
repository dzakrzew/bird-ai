import pygame

class Block(pygame.sprite.Sprite):
    TYPE_TOP = 'top'
    TYPE_BOTTOM = 'bottom'
    GAP_SIZE = 120

    def __init__(self, block_type, x, h):
        super().__init__()

        if block_type == Block.TYPE_TOP:
            self.image = pygame.image.load('sprites/block_top.png')
            self.image = pygame.transform.scale(self.image, (60, 500))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, 0 - 500 + h
        else:
            self.image = pygame.image.load('sprites/block_bottom.png')
            self.image = pygame.transform.scale(self.image, (60, 500))
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, h + Block.GAP_SIZE
        
    def update(self):
        self.rect.x -= 4
        self.mask = pygame.mask.from_surface(self.image)