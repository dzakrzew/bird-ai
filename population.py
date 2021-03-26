from bird import Bird
import random

class Population:
    def __init__(self, game, n):
        self.n = n
        self.game = game
        self.population = []
    
    def getAliveCount(self):
        c = len(self.population)
        for bird in self.population:
            if bird.isKilled:
                c -= 1
        return c

    def over(self):
        top = self.getTop()
        for b in top:
            print('Bird#' + str(b.id) + ', result: ' + str(b.result))
        self.newPopulation()
        #self.initPopulation()

    def getTop(self):
        population_sorted = sorted(self.population, key=lambda b: b.result, reverse=True)
        return population_sorted

    def crossover(self, birdA, birdB):
        childA = Bird(0, 100, 100, self, self.game)
        childB = Bird(1, 100, 100, self, self.game)

        for x in range(len(birdA.brain.l1)):
            for y in range(len(birdA.brain.l1[x])):
                r = random.randint(0, 100)
                
                b = birdA
                if r < 50:
                    b = birdB
                
                childA.brain.l1[x][y] = b.brain.l1[x][y]

        for x in range(len(birdA.brain.l2)):
            for y in range(len(birdA.brain.l2[x])):
                r = random.randint(0, 100)
                
                b = birdA
                if r < 50:
                    b = birdB
                
                childA.brain.l2[x][y] = b.brain.l2[x][y]    

        for x in range(len(birdA.brain.l3)):
            for y in range(len(birdA.brain.l3[x])):
                r = random.randint(0, 100)
                
                b = birdA
                if r < 50:
                    b = birdB
                
                childA.brain.l3[x][y] = b.brain.l3[x][y] 

        return childA, childB

    def mutate(self, bird):
        for x in range(len(bird.brain.l1)):
            for y in range(len(bird.brain.l1[x])):
                if random.randint(0, 100) < 30:
                    bird.brain.l1[x][y] = bird.brain.l1[x][y] * random.uniform(-1, 1)

        for x in range(len(bird.brain.l2)):
            for y in range(len(bird.brain.l2[x])):
                if random.randint(0, 100) < 30:
                    bird.brain.l2[x][y] = bird.brain.l2[x][y] * random.uniform(-1, 1)

        for x in range(len(bird.brain.l3)):
            for y in range(len(bird.brain.l3[x])):
                if random.randint(0, 100) < 30:
                    bird.brain.l3[x][y] = bird.brain.l3[x][y] * random.uniform(-1, 1)
        return bird

    def newPopulation(self):
        top = self.getTop()
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
            bird = Bird(i + 4, 100, 100, self, self.game)
            
            bird.brain.l1 = self.mutate(top[i]).brain.l1

            self.population.append(bird)
            self.game.all_sprites.add(bird)
            self.game.birds.add(bird)

    def initPopulation(self):
        for bird in self.population:
            bird.kill()
        
        self.population = []
        
        for i in range(self.n):
            bird = Bird(i, 100, 100, self, self.game)
            
            self.population.append(bird)
            self.game.all_sprites.add(bird)
            self.game.birds.add(bird)