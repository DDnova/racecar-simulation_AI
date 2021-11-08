import sys
import os
import math

import pygame
import neat

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# CAR_SIZE_X=1000
# CAR_SIZE_Y=1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
track = pygame.image.load("Assets/map5.png")


class Car(pygame.sprite.Sprite):
    def __init__(self):
        # initialize parent class
        super().__init__()
        # load car image
        self.car_image = pygame.image.load("Assets/car1.png")
        # self.car_image = pygame.transform.scale(self.car_image, (CAR_SIZE_X, CAR_SIZE_Y)) #Size of car

        # set image displayed on screen to original image
        self.image = self.car_image

        # Starting Position ->the chequered strip
        self.position = [830, 920]

        # specify rectangle of image
        self.rect = self.image.get_rect(center=self.position)

        self.drive_state = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5

        # 0 -> stright | -1 -> left | 1 -> right
        self.direction = 0
        
        self.alive=True

    def update(self):
        self.drive()
        self.rotate()
        for radar_angle in (-60,-30,0,30,60):
            self.radar(radar_angle)
        self.collison()

    def drive(self):
        if self.drive_state:
            # control how fast it goes by changing *6
            self.rect.center += self.vel_vector * 6

    def collison(self):
        length=25
        # on right headlight
        collison_point_right=[int(self.rect.center[0]+math.cos(math.radians(self.angle+18))*length),
                              int(self.rect.center[1]-math.sin(math.radians(self.angle+18))*length)]
        
        # on left headlight
        collison_point_left=[int(self.rect.center[0]+math.cos(math.radians(self.angle-18))*length),
                              int(self.rect.center[1]-math.sin(math.radians(self.angle-18))*length)]
        
        # die on collison
        if screen.get_at(collison_point_right)==pygame.Color(255,255,255,255)\
            or screen.get_at(collison_point_left)==pygame.Color(255,255,255,255):
                self.alive=False
                # print('car is dead')
        
        # draw collison points
        pygame.draw.circle(screen,(0,255,255,0),collison_point_right,4)
        pygame.draw.circle(screen,(0,255,255,0),collison_point_left,4)
        
    def rotate(self):
        # turn right
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        # turn left
        if self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.car_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def radar(self,radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while (
            not screen.get_at((x, y)) == pygame.Color(255, 255, 255, 255) and length < 200
        ):
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)

        # draw radar
        pygame.draw.line(screen, (0,255,0,0), self.rect.center, (x, y), 1)
        pygame.draw.circle(screen, (0,255,0,0),(x,y),3)


car = pygame.sprite.GroupSingle(Car())


def eval_genomes():
    run = True
    while run:
        # check for events happening
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        # display track on screen
        screen.blit(track, (0, 0))

        # user input
        user_input = pygame.key.get_pressed()
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            # direction 0 when no arrow keys are pressed
            car.sprite.direction = 0

        # drive
        if user_input[pygame.K_UP]:
            car.sprite.drive_state = True

        # steer
        if user_input[pygame.K_RIGHT]:
            car.sprite.direction = 1
        if user_input[pygame.K_LEFT]:
            car.sprite.direction = -1

        # update
        car.draw(screen)
        car.update()
        pygame.display.update()


eval_genomes()
