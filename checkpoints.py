import pygame
import math

# Individual checkpoints for rewards, given 2 points, it creates a line with thickness 5 (rectangle technically)
class Checkpoint:
    def __init__(self, start, end, color=(0, 255, 0, 128)):
        self.start = start
        self.end = end
        # Color is green by default
        self.color = color
        self.thickness = 5 
        self.surface = self.create_surface()
        # Creates a mask from the surface for collision
        self.mask = pygame.mask.from_surface(self.surface)
        self.reached = False

    def create_surface(self):
        # Gets the start and end and gets the line between the 2
        x1, y1 = self.start
        x2, y2 = self.end
        
        width = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        height = self.thickness
        
        # Draws a straight rectangle then rotates it accordingly, since it isnt an image it doesnt get distorted and
        # can use the pygame rotate
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, (0, 0, width, height))
        
        angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        
        rotated_surface = pygame.transform.rotate(surface, -angle)
        
        return rotated_surface

    # Draws it on the screen
    def draw(self, window):
        center_x = (self.start[0] + self.end[0]) // 2
        center_y = (self.start[1] + self.end[1]) // 2
        
        rect = self.surface.get_rect(center=(center_x, center_y))
        
        window.blit(self.surface, rect.topleft)

    def get_position(self):
        return self.start

# Class used for drawing and creating a checkpoints for players
class CheckpointManager:
    def __init__(self, checkpoints_inp = None):
        # Checkpoints (have to manually do) coordinates
        if checkpoints_inp:
            checkpoints = checkpoints_inp
        else:
            checkpoints = [
                ((204, 202), (344, 202)),
                ((368, 30), (368, 156)),
                ((500, 40), (500, 140)),
                ((638, 45), (638, 130)),
                ((668, 130), (750, 130)),
                ((640, 179), (700, 217)),
                ((574, 261), (682, 314)),
                ((528, 318), (618, 380)),
                ((472, 400), (562, 466)),
                ((390, 540), (554, 540)),
                ((405, 596), (512, 596)),
                ((376, 656), (490, 716)),
                ((364, 720), (364, 804)), 
                ((230, 692), (368, 692)), # For whatever reason, lines with positive slopes dont work too well
                ((204, 630), (344, 630)),
                ((204, 520), (344, 520)),
                ((204, 412), (344, 412))
            ]
        self.checkpoints = []
        # Initializes them
        for check_point in checkpoints:
            self.checkpoints.append(Checkpoint(check_point[0], check_point[1]))



    # Draws them
    def draw_checkpoints(self, window):
        for checkpoint in self.checkpoints:
            checkpoint.draw(window)

    # Checks for collison with the checkpoint, makes sure the checkpoint wasnt previously reached, not actually used though
    def check_collision(self, car):
        for i, checkpoint in enumerate(self.checkpoints):
            if car.collide(checkpoint.mask, *checkpoint.get_position()):
                if checkpoint.reached != True:
                    checkpoint.reached = True
                    return i
        return None
    def create_player_checkpoints(self):
        return PlayerCheckpoints(self.checkpoints)

    # Not used, instead new ones are just created
    def reset_checkpoints(self):
        for checkpoint in self.checkpoints:
            checkpoint.reached = False

# Used and given to every player via create checkpoints function
class PlayerCheckpoints:
    def __init__(self, checkpoints):
        self.checkpoints = checkpoints
        self.current_checkpoint = 0
        self.lap = 0

    # Checks for collision and makes sure that it doesnt go through same checkpoint nultiple times
    def check_collision(self, car):
        if self.current_checkpoint < len(self.checkpoints):
            checkpoint = self.checkpoints[self.current_checkpoint]
            if car.collide(checkpoint.mask, *checkpoint.get_position()):
                self.current_checkpoint += 1
                return self.current_checkpoint
        return None


    def reset(self):
        self.current_checkpoint = 0
        self.lap = 0