import pygame
import math
import time
# Utilities for scaling and rotating img

def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def rotate_img(win, image, top_left, angle):
    rotated_img = pygame.transform.rotate(image, angle)
    new_rect = rotated_img.get_rect(center=image.get_rect(topleft = top_left).center)
    win.blit(rotated_img, new_rect.topleft)