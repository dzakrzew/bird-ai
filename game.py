import sys, pygame, math, random, time
from block import Block
from population import Population

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        self.screen = pygame.display.set_mode((700, 500))
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.best = 0
        self.x = 0
        self.running = False
        self.all_sprites = pygame.sprite.Group()
        self.bottom_blocks = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.bg = pygame.image.load('sprites/bg.png')
        self.population = Population(self, 50)
        self.population.initPopulation()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def getNextBottomBlockData(self):
        next_block = None
        next_block_id = 0

        for block in self.bottom_blocks:
            if 100 < block.rect.x:
                next_block = block
                break

        return {'x': next_block.rect.x, 'y': next_block.rect.y}

    def removeUnusedBlocks(self):
        for block in self.blocks:
            if block.rect.x <= -60:
                block.kill()

    def generateBlock(self):
        h = random.randint(100, 300)

        print('generuje blok: x=' + str(self.x) + '  h=' + str(h))

        block_top = Block(Block.TYPE_TOP, 700, h)
        block_bottom = Block(Block.TYPE_BOTTOM, 700, h)
        
        self.all_sprites.add(block_top)
        self.all_sprites.add(block_bottom)
        self.blocks.add(block_top)
        self.bottom_blocks.add(block_bottom)
        self.blocks.add(block_bottom)

    def update(self):
        for bird in self.birds:
            if not bird.isKilled:
                if pygame.sprite.spritecollide(bird, self.blocks, False):
                    print('HIT ' + str(bird.id))
                    bird.killed(self.x)
                elif bird.rect.y < -100 or 500 < bird.rect.y:
                    print('OUT ' + str(bird.id))
                    bird.killed(self.x)
        
        if self.population.getAliveCount() == 0:
            self.reset()
            return

        if self.x % 100 == 0:
            self.generateBlock()

        self.x += 1
        self.removeUnusedBlocks()
        self.all_sprites.update()

    def reset(self):
        self.x = 0
        self.birds.empty()
        self.blocks.empty()
        self.bottom_blocks.empty()
        self.all_sprites.empty()
        self.population.over()

    def redraw(self):
        #self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        self.all_sprites.draw(self.screen)

        textsurface = self.font.render(str(self.x) + ', alive: ' + str(self.population.getAliveCount()) + ', best: ' + str(self.best), True, (255, 255, 255))
        self.screen.blit(textsurface, (0, 0))

    def run(self):
        while True:
            self.handleEvents()
            self.update()
            self.redraw()
            
            pygame.display.flip()
            self.clock.tick_busy_loop(self.fps)