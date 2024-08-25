import pygame as pg
from pygame import draw


def draw_image(orig_image: pg.image, rect: pg.rect, screen: pg.display, facing_direction=0, scaleX=1, scaleY=1, flip_x: bool=False, other_x=0, flip_y: bool=False, other_y=0):
    """
    Draws an image to the screen based on certain parameters
    
    Args:
        - orig_image: The original image before any transformations are applied.
        - rect: The image rect
        - screen: The display window to draw the image to
        - facing_direction: The direction the image should be facing
        - scaleX: Increase or decrease the size of the image on the X-axis
        - scaleY: Increase or decrease the size of the image on the Y-axis
        - flip_x: Allow the image to be flipped on the x-axis
        - other_x: The point at which the image flips
        - flip_y: Allow the image to be flipped on the y-axis
        - other_y: The point at which the image flips
    
    Returns:
        No returns, blits image directly to screen.
    """
    if flip_x == True:
        if other_x < rect.centerx:
            sprite = pg.transform.flip(orig_image, 1, 0)
        else:
            sprite = orig_image
    else:
        sprite = orig_image
    if flip_y == True:
        if other_y < rect.centery:
            sprite = pg.transform.flip(orig_image, 0, 1)
        else:
            sprite = orig_image
    scaleX = scaleX*rect.width
    scaleY = scaleY*rect.height
    sprite = pg.transform.smoothscale(sprite, (scaleX, scaleY))
    sprite = pg.transform.rotozoom(sprite, facing_direction, 1)
    # Create a new rect with the center of the old rect.
    rect = sprite.get_rect(center=rect.center)
    screen.blit(sprite, rect)