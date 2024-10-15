import pygame
import random
from util import *
CAR = scale_image(pygame.image.load("img/car.png"), .4)
# Abstract car from tech with tim vid + other additions
class AbstractCar:
    # Takes in movement info of the car
    def __init__(self, max_velocity, rotation_velocity, acceleration=.05, friction = .5):
        self.max_velocity = max_velocity
        self.velocity = 0
        self.max_rot = rotation_velocity
        self.angle = 0
        self.image = self.IMG
        self.acceleration = acceleration
        self.friction_constant = friction

        self.x, self.y  = self.START
        self.checkpoints = None  
        self.total_distance = 0  

    def rotate(self, left=False, right=False):
        if left and self.velocity != 0:
            self.angle += self.max_rot
        elif right and self.velocity != 0:
            self.angle -= self.max_rot
    
    def draw(self,win):
        rotate_img(win,self.image, (self.x, self.y), self.angle)

    def move_forward(self):
        self.velocity = min(self.velocity + self.acceleration, self.max_velocity)
        self.move()

    def move_backwards(self):
        self.velocity = max(self.velocity - self.acceleration, -self.max_velocity/2)
        self.move()
    
    def move(self):
        rads = math.radians(self.angle)
        y_change = math.cos(rads) * self.velocity
        x_change = math.sin(rads) * self.velocity

        new_x = self.x - x_change
        new_y = self.y - y_change

        # Calculates the total distance travelled for use in reward
        distance_traveled = math.sqrt((new_x - self.x)**2 + (new_y - self.y)**2)
        self.total_distance += distance_traveled

        self.x = new_x
        self.y = new_y
    
    # No backwards coasting because no model will go backwards, only for person
    def coast(self):
        self.velocity = max(self.velocity -self.acceleration*self.friction_constant, 0)
        self.move()
    
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x-x), int(self.y-y))
        poi = mask.overlap(car_mask, offset)
        return poi



class PlayerCar(AbstractCar):
    IMG = CAR
    START = (260,300)

    def __init__(self, max_velocity, rotation_velocity, checkpoint_manager):
        super().__init__(max_velocity, rotation_velocity)
        self.checkpoints = checkpoint_manager.create_player_checkpoints()
    def reset(self):
        self.x, self.y = self.START
        self.angle = 0
        self.velocity = 0
        self.checkpoints.reset()

class AiCar(AbstractCar):
    # Adjust the start and possible moves accordingly
    IMG = CAR
    START = (260,300)
    MOVES = ["forward", "forward_left", "forward_right"]
    # MOVES = ["forward", "forward_left", "forward_right", "right", "left"]
    # MOVES = ["forward", "left", "right", "foward", "foward"]

    def reset(self):
        self.x, self.y = self.START
        self.angle = 0
        self.velocity = 0
        self.checkpoints.reset()
        self.survival_time = 0
        self.alive = True
        self.score = 0
        self.total_distance = 0
    
    # Takes in a path to immitate previous results
    def __init__(self, max_velocity, rotation_velocity, checkpoint_manager, acceleration=0.05, friction=0.5, path = None, calcualte_score = None):
        super().__init__(max_velocity, rotation_velocity, acceleration, friction)
        self.index = 0
        self.checkpoints = checkpoint_manager.create_player_checkpoints()
        self.path = path if path is not None else []
        self.alive = True
        self.survival_time = 0
        self.score = 0
        # Stores current x and y to print to see total path
        self.point_path = []
    
    # Moves randomly, turns 3 times for sharper turns to keep speed. Can adjust
    def random_move(self):
        move = random.choice(self.MOVES)
        if move == "forward":
            self.move_forward()
        elif move == "forward_left":
            self.rotate(left=True)
            self.rotate(left=True)
            self.rotate(left=True)
            self.move_forward()
        elif move == "forward_right":
            self.rotate(right=True)
            self.rotate(right=True)
            self.rotate(right=True)
            self.move_forward()
        elif move == "right":
            self.rotate(right=True)
        elif move == "left":
            self.rotate(left=True)
        self.path.append(move)
        self.point_path.append((int(self.x), int(self.y)))
    
    # Does a preset move
    def set_move(self, move):
        if move == "forward":
            self.move_forward()
        elif move == "forward_left":
            self.rotate(left=True)
            self.rotate(left=True)
            self.rotate(left=True)
            self.move_forward()
        elif move == "forward_right":
            self.rotate(right=True)
            self.rotate(right=True)
            self.rotate(right=True)
            self.move_forward()
        elif move == "right":
            self.rotate(right=True)
        elif move == "left":
            self.rotate(left=True)
        self.point_path.append((int(self.x), int(self.y)))
    
    def draw_path(self, win):
        color=(0,255,255)
        for point in self.point_path:
            pygame.draw.circle(win, color, point, 5)
    
    def update(self):
        if self.alive:
            # If the path is longer than the current index then it does a moev on the path otherwise a random move
            if self.index < len(self.path) - 1:
                self.set_move(self.path[self.index])
            else:
                self.random_move()
            self.survival_time += 1
            self.index += 1

    def num_moves(self):
        return self.index
    
    # Reward func, change accordingly
    def calculate_score(self):
        return 1500 * (self.checkpoints.current_checkpoint) + 8 * int((self.total_distance*1.5) / self.survival_time*100) + int(self.total_distance*1.5)

