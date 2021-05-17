from bird import Bird
import random

class Population:
    MUTATION_PROBABILITY = 10
    CROSSOVER_TRESHOLD = 50

    def __init__(self, game, n):
        self.n = n
        self.game = game
        self.population = []
    
    def get_alive_count(self):
        c = len(self.population)
        for bird in self.population:
            if bird.is_killed:
                c -= 1
        return c

    def over(self):
        self.new_population()

    def get_top(self):
        population_sorted = sorted(self.population, key=lambda b: b.result, reverse=True)
        return population_sorted

    def crossover(self, birdA, birdB):
        childA = Bird(0, 100, 400, self, self.game)
        childB = Bird(1, 100, 400, self, self.game)

        for l in range(len(birdA.brain.layers)):
            for x in range(len(birdA.brain.layers[l])):
                for y in range(len(birdA.brain.layers[l][x])):
                    r = random.randint(0, 100)
                    
                    a = birdA
                    b = birdB
                    if r < Population.CROSSOVER_TRESHOLD:
                        a = birdB
                        b = birdA
                    
                    childA.brain.layers[l][x][y] = a.brain.layers[l][x][y]
                    childB.brain.layers[l][x][y] = b.brain.layers[l][x][y]

        return childA, childB

    def mutate(self, bird):
        for l in range(len(bird.brain.layers)):
            for x in range(len(bird.brain.layers[l])):
                for y in range(len(bird.brain.layers[l][x])):
                    if random.randint(0, 100) < Population.MUTATION_PROBABILITY:
                        bird.brain.layers[l][x][y] = bird.brain.layers[l][x][y] * random.uniform(-1., 1)

        return bird

    def new_population(self):
        top = self.get_top()
        childA, childB = self.crossover(top[0], top[1])
        childC, childD = self.crossover(top[0], top[2])
        
        for bird in self.population:
            bird.kill()

        self.population = []

        self.population.append(childA)
        self.population.append(childB)
        self.game.all_sprites.add(childA)
        self.game.all_sprites.add(childB)
        self.game.birds.add(childA)
        self.game.birds.add(childB)

        self.population.append(childC)
        self.population.append(childD)
        self.game.all_sprites.add(childC)
        self.game.all_sprites.add(childD)
        self.game.birds.add(childC)
        self.game.birds.add(childD)

        for i in range(self.n - 4):
            bird = Bird(i + 4, 100, 400, self, self.game)
            mutated = self.mutate(top[i])
            bird.brain.layers = mutated.brain.layers

            self.population.append(bird)
            self.game.all_sprites.add(bird)
            self.game.birds.add(bird)

    def init_population(self):
        for bird in self.population:
            bird.kill()
        
        self.population = []
        
        for i in range(self.n):
            bird = Bird(i, 100, 400, self, self.game)
            
            self.population.append(bird)
            self.game.all_sprites.add(bird)
            self.game.birds.add(bird)
