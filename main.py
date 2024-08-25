import game_loop, io, physics
from helper_functions import *
import pygame as pg



screen, color, center, clock, running, mouse_x, mouse_y, mouse_down = game_loop.setup(width=1280, height=800, colour="black")


# Arbitrary variables
floor_height = 740
# leg movement
modef1 = 0 # 0 = hold | 1 = move right | 2 = move left
modef2 = 0 # 0 = hold | 1 = move right | 2 = move left
foot1_y = floor_height
foot1_x = 200
foot2_y = floor_height
foot2_x = 100

# Body movement
lower_x = 100
lower_y = 670

upper_x = 100
upper_y = 590



class Human():
    def __init__(self):
        pass
        self.upper = physics.Coords(upper_x, upper_y)
        self.lower = physics.Coords(lower_x, lower_y)

    def step(self):
        self.upper.x += 2
        self.lower.x = self.upper.x
        self.lower.y = self.upper.y+80

    def draw(self):
        pg.draw.line(screen, (255,0,0), [self.lower.x, self.lower.y], [self.upper.x, self.upper.y], 8)

gravity =  physics.Gravity(strength=0.04, limit=30, direction=180)
friction = physics.Friction(0.22)

player = Human()
leg1 = physics.Inverse_kinematics.Arm(2, 40, (222, 0, 0))
leg2 = physics.Inverse_kinematics.Arm(2, 40, (222, 0, 0))

# Grass Test
grass1 = physics.Grass(physics.Coords(640, 400))




while running:
    
    running, mouse_x, mouse_y, mouse_down = game_loop.loop_start(screen, color,
                                              mouse_x, mouse_y, mouse_down)
    player.step()

    if modef1 == 0:
        if foot1_x <= player.lower.x - 55:
            modef1 = 1
    elif modef1 == 1:
        if foot1_x < player.lower.x:
            foot1_y -= 0.8
        else:
            foot1_y += 0.8
        foot1_x += 4
        if foot1_x >= player.lower.x + 50:
            modef1 = 0
            foot1_y = floor_height
    if modef2 == 0:
        if foot2_x <= player.lower.x - 55:
            modef2 = 1
    elif modef2 == 1:
        if foot2_x < player.lower.x:
            foot2_y -= 0.8
        else:
            foot2_y += 0.8
        foot2_x += 4
        if foot2_x >= player.lower.x + 50:
            modef2 = 0
            foot2_y = floor_height

    player.lower.y = lower_y + abs(foot1_x-player.lower.x)/4
    player.upper.y = player.lower.y - 80

    leg1.step(screen, [foot1_x, foot1_y], player.lower.x, player.lower.y)
    leg2.step(screen, [foot2_x, foot2_y], player.lower.x, player.lower.y)

    player.draw()


    # Grass Test
    grass1.step(screen)



    game_loop.loop_end(clock, 120)
    
game_loop.Quit()