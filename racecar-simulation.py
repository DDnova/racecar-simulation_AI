import pygame
import os
import random
import math
import sys
import neat

pygame.init()
# Global Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
TRACK = pygame.image.load("Assets/map8.png")

current_generation = 0 # Generation counter

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.car_image =  pygame.image.load("Assets/car1.png")
        self.image = self.car_image
        # Starting Position ->the chequered strip
        # self.position = [830, 920]
        self.position = [585, 836]
        # specify rectangle of image
        self.rect = self.image.get_rect(center=self.position)
        
        self.center = self.rect.center
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []

    def update(self, screen):
        self.radars.clear()
        self.rotate(screen)
        self.drive()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(SCREEN, radar_angle)
        self.data()
        self.collision(screen)


        #print(self.radar(SCREEN, 0)[0])

    def drive(self):
        self.rect.center += self.vel_vector*6

    def collision(self, screen):
        len = 25
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(360+18-self.angle))*len),
                           int(self.rect.center[1] + math.sin(math.radians(360+18-self.angle))*len)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(360-18-self.angle))*len),
                           int(self.rect.center[1] + math.sin(math.radians(360-18-self.angle))*len)]

        # print(screen.get_at(collision_point_right))
        if screen.get_at(collision_point_right) == pygame.Color(255, 255, 255, 255) \
                or screen.get_at(collision_point_left) == pygame.Color(255, 255, 255, 255):
            self.alive = False
            # print("collision")

        # Draw Collision Points - (draw this after getting the color(!) using get_at)
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(screen, (0, 255, 255, 0), collision_point_left, 4)

    def rotate(self, screen):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.car_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)
        # pygame.draw.rect(screen, (255, 255, 255, 255), self.rect)

    def radar(self, screen, radar_angle):
        length = 0
        x = int(self.rect.center[0] + math.cos(math.radians(360-self.angle+radar_angle)) * length)
        y = int(self.rect.center[1] + math.sin(math.radians(360-self.angle+radar_angle)) * length)

        while not screen.get_at((x, y)) == pygame.Color(255, 255, 255, 255) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(360-self.angle+radar_angle)) * length)
            y = int(self.rect.center[1] + math.sin(math.radians(360-self.angle+radar_angle)) * length)

        # Draw Radar
        pygame.draw.line(screen, (0,255,0,0), self.rect.center, (x, y), 1)
        pygame.draw.circle(screen, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2)
                             + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])

    def data(self):
        radars = self.radars
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            input[i] = int(radar[1])
        return input
    

def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)

def eval_genomes(genomes, config):
    global cars, ge, nets
    clock = pygame.time.Clock()

    cars = []
    ge = []
    nets = []

    # Font Settings & Loading Map
    generation_font = pygame.font.SysFont("Arial", 30)

    global current_generation
    current_generation += 1

        
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        SCREEN.blit(TRACK, (0, 0))

        for car in cars:
            car.update(SCREEN)
            car.draw(SCREEN)

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1
            if not car.sprite.alive:
                remove(i)

        for i, car in enumerate(cars):
            # print(car.sprite.data())
            output = nets[i].activate(car.sprite.data())
            #print(output)
            if output[0] > 0.7:
                car.sprite.direction = -1
            if output[1] > 0.7:
                car.sprite.direction = 1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0
                
        # Display Info
        text = generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        SCREEN.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)
        pygame.display.update()


# Setup the NEAT Neural Network
def run(config_path):
    global population
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    population.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
