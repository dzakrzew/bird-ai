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
        self.iteration = 1
        self.running = False
        self.all_sprites = pygame.sprite.Group()
        self.bottom_blocks = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.birds = pygame.sprite.Group()
        self.bg = pygame.image.load('sprites/bg.png')
        self.population = Population(self, 50)
        self.population.init_population()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def get_next_bottom_block_data(self):
        next_block = None
        next_block_id = 0

        for block in self.bottom_blocks:
            if 100 < block.rect.x:
                next_block = block
                break

        return {'x': next_block.rect.x, 'y': next_block.rect.y}

    def remove_unused_blocks(self):
        for block in self.blocks:
            if block.rect.x <= -60:
                block.kill()

    def generate_block(self):
        h = random.randint(100, 300)
        block_top = Block(Block.TYPE_TOP, 700, h)
        block_bottom = Block(Block.TYPE_BOTTOM, 700, h)
        
        self.all_sprites.add(block_top)
        self.all_sprites.add(block_bottom)
        self.blocks.add(block_top)
        self.bottom_blocks.add(block_bottom)
        self.blocks.add(block_bottom)

    def update(self):
        for bird in self.birds:
            if not bird.is_killed:
                if pygame.sprite.spritecollide(bird, self.blocks, False):
                    bird.killed(self.x)
                elif bird.rect.y < -100 or 500 < bird.rect.y:
                    bird.killed(self.x)
        
        if self.population.get_alive_count() == 0:
            self.reset()
            return

        if self.x % 100 == 0:
            self.generate_block()

        self.x += 1
        self.remove_unused_blocks()
        self.all_sprites.update()

    def reset(self):
        self.x = 0
        self.birds.empty()
        self.blocks.empty()
        self.bottom_blocks.empty()
        self.all_sprites.empty()
        self.population.over()
        self.iteration += 1

    def redraw(self):
        self.screen.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.screen)
        textsurface = self.font.render('Iteration: ' + str(self.iteration) + '  Current: ' + str(self.x) + '  Alive birds: ' + str(self.population.get_alive_count()) + '  Best result: ' + str(self.best), True, (255, 255, 255))
        self.screen.blit(textsurface, (0, 0))

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.redraw()
            
            pygame.display.flip()
            self.clock.tick_busy_loop(self.fps)