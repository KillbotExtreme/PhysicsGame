import pygame as pg
from pygame import time
from pygame.locals import QUIT


def setup(width: int=640, height: int=480, caption: str="Test", colour:pg.color="white"):
    """
    Creates a PyGame display surface and calculates the center.
    Also sets up some initial variables.
    
    Args:
        width(int): Width in pixels
        height(int): Height in pixels
        caption(str): Title of the window
        colour: Screen background colour. "white", "black", or (xxx, xxx, xxx)
     
    Returns:
        screen, colour, center, clock, running, mouse_x, mouse_y, mouse_down
    """
    if colour.lower() == "white":
        colour = (255, 255, 255)
    elif colour.lower() == "black":
        colour = (0, 0, 0)
    pg.init()
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption(caption)
    center = (width/2, height/2)
    clock = time.Clock()
    running = True
    mouse_x, mouse_y, mouse_down = 0, 0, False
    
    return screen, colour, center, clock, running, mouse_x, mouse_y, mouse_down


def loop_start(screen, colour, mouse_x, mouse_y, mouse_down):
    """
    Returns mouse input and exit condition.
    Fills the screen with the background colour
    
    Args:
        screen: pg.display
        colour: Background colour
        mouse_x: The mouse's X position
        mouse_y: The mouse's Y position
        mouse_down: Is the left button held down?
     
    Returns:
        running, mouse_x, mouse_y, mouse_down
    """
    running = True
    for event in pg.event.get():
        mouse_x, mouse_y = pg.mouse.get_pos()
        if event.type == QUIT:
            running = False
        mouse_down = True if pg.mouse.get_pressed()[0] else False
    screen.fill(colour)
    
    return running, mouse_x, mouse_y, mouse_down


def loop_end(clock: time.Clock, frame_rate: int):
    """
    Flips the display and does clock.tick

    Args:
        clock (time.Clock): the clock object
        frame_rate (int): Game Frame Rate
    """
    pg.display.flip()
    clock.tick(frame_rate)


def Quit():
    """ Exits pygame """
    pg.display.quit()
    pg.quit()

