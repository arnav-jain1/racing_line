import pygame
import math
import time
from util import *
from car import *
from checkpoints import *
from gai import *

FPS = 60

# Load stuff
TRACK = scale_image(pygame.image.load("img/track.png"),2)
TRACK_BORDER = scale_image(pygame.image.load("img/track.png"),2)
TRACK_MASK = pygame.mask.from_surface(TRACK_BORDER)
CAR = scale_image(pygame.image.load("img/car.png"), .4)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Algorithm")

# Finish line
FINISH_LINE_WIDTH = 150
FINISH_LINE_HEIGHT = 5
FINISH_LINE_POS = (200, 340)  
finish_line_surface = pygame.Surface((FINISH_LINE_WIDTH, FINISH_LINE_HEIGHT), pygame.SRCALPHA)
finish_line_surface.fill((0, 0, 255, 255))  
FINISH_MASK = pygame.mask.from_surface(finish_line_surface)

checkpoint_manager = CheckpointManager()


pygame.font.init()
FONT = pygame.font.Font(None, 30)  

# Draws the screen
def draw(window, images, cars, generation, player_car = None):
    window.fill("white")
    for img, pos in images:
        window.blit(img, pos)
    if player_car:
        player_car.draw(window)
    window.blit(finish_line_surface, FINISH_LINE_POS)
    checkpoint_manager.draw_checkpoints(window)

    for car in cars:
        if car.alive:
            car.draw(window)
    # To get mouse position when drawing checkpoints
    cursor_pos = pygame.mouse.get_pos()
    cursor_text = FONT.render(f"Cursor: {cursor_pos}", True, (0, 0, 0))
    window.blit(cursor_text, (WIDTH - cursor_text.get_width() - 10, 200)) 
    generation_text = FONT.render(f"Generation: {generation}", True, (0, 0, 0))
    window.blit(generation_text, (WIDTH - generation_text.get_width() - 10, 10))  

    pygame.display.update()

# To move the player car, not currently being used
def move_player(player_car):
    moved = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)

    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backwards()

    if not moved:
        player_car.coast()





def main():
    # Initialize vars and cars
    images = [(TRACK, (0,0))]
    # player_car = PlayerCar(3,2, checkpoint_manager)


    gai = GeneticAlgorithm(checkpoint_manager)
    ai_cars = gai.start()
    loop = True
    clock = pygame.time.Clock()
    while loop:
        clock.tick(FPS)


        draw(window, images, ai_cars, gai.generation)



        # End
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                break
        
        # Get all the alive cars
        alive_cars = [car for car in ai_cars if car.alive]
        for car in alive_cars:
            # Change their position
            car.update()
            
            # Check collisions after moving
            if car.collide(TRACK_MASK) is not None:
                car.alive = False
            if car.collide(FINISH_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1]) and car.checkpoints.current_checkpoint == len(checkpoint_manager.checkpoints):
                car.checkpoints.lap += 1
                print(f"Lap {car.checkpoints.lap} completed!")
                car.checkpoints.current_checkpoint = 0
            # Check collitions with checkpoints
            car.checkpoints.check_collision(car)

        # If all the cars are dead
        if not any(car.alive for car in ai_cars):
            # Get the best performing cars and print the results
            ai_cars.sort(key=lambda x: x.calculate_score(), reverse=True)
            
            print(f"\nGeneration {gai.generation} results:")
            for i, car in enumerate(ai_cars[:gai.TOP_PERFORMERS], 1):
                print(f"Car {i}: Score = {car.calculate_score()}, Path length = {int(car.total_distance)}")

            # Keep top cars and create a new generation with them
            top_cars = ai_cars[:gai.TOP_PERFORMERS]
            
            # To draw the cars path
            for car in top_cars:
                if car.checkpoints.lap > 0:
                    car.draw_path(window)
                    pygame.display.update()
                    time.sleep(5)

            
            ai_cars = gai.create_next_generation(top_cars)
            
            
            gai.generation += 1 
        
        # For moving a player car (bug testing purposes)
        # move_player(player_car)
        # collide = player_car.collide(TRACK_MASK)
        # if collide != None:
            # player_car.reset()
        
        
        # if player_car.collide(FINISH_MASK, FINISH_LINE_POS[0], FINISH_LINE_POS[1]) and player_car.checkpoints.current_checkpoint == len(checkpoint_manager.checkpoints):
        #     player_car.checkpoints.lap += 1
        #     print(f"Lap {player_car.checkpoints.lap} completed!")
        #     player_car.checkpoints.current_checkpoint = 0

        # checkpoint_hit = player_car.checkpoints.check_collision(player_car)
        # if checkpoint_hit is not None:
        #     print(f"Checkpoint {checkpoint_hit} reached!")
    pygame.quit()
if __name__ == "__main__":
    main()

