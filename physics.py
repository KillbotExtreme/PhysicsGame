import pygame as pg
from pygame import draw
import math
from helper_functions import *


class Coords():
    def __init__(self, x:int = 0, y:int = 0):
        self.x = x
        self.y = y


class Gravity():
    """
    Creates a cravity object that just stores gravity details

    Args:
        strength (float): The strength of gravity
        limit (float): The maximum gravity
        direction (float): The direction of gravity
    """
    def __init__(self, strength: float, limit: float, direction: float):
        self.strength = strength
        self.limit = limit
        self.direction = direction


class Friction():
    """
    Creates a friction object that just stores friction details

    Args:
        amount (float): The amount of friction
    """
    def __init__(self, amount):
        self.amount = amount


class SoftBody():

    class Point():
        def __init__(self, screen, x, y, gravityObj: Gravity, max_speed=10, size=10, friction=0.1):
            self.x = x
            self.y = y
            self.hspeed = 0
            self.vspeed = 0
            self.screen = screen
            self.size = size
            self.gravityObj = gravityObj
            self.maxSpeed = max_speed
            self.friction = friction
        
        def step(self):
            
            # Gravity
            if self.vspeed < self.gravityObj.limit:
                self.vspeed += self.gravityObj.strength
            
            # Translate speed to movement
            if self.vspeed > self.maxSpeed:
                self.vspeed = self.maxSpeed
            elif self.vspeed < -self.maxSpeed:
                self.vspeed = -self.maxSpeed
            if self.hspeed > self.maxSpeed:
                self.hspeed = self.maxSpeed
            elif self.hspeed < -self.maxSpeed:
                self.hspeed = -self.maxSpeed
            
            self.x += self.hspeed
            self.y += self.vspeed
            
            # Bounding Box
            if self.x > self.screen.get_width():
                self.x = self.screen.get_width()
                self.hspeed = 0
            elif self.x < 0:
                self.x = 0
                self.hspeed = 0
            if self.y > self.screen.get_height():
                self.y = self.screen.get_height()
                self.vspeed = 0
            elif self.y < 0:
                self.y = 0
                self.vspeed = 0
            self.hspeed *= (1-self.friction)
            self.hspeed *= (1-self.friction)
        
        def draw(self):
            draw.circle(self.screen, (0, 255, 0), (self.x, self.y), self.size)


    class Spring():
        def __init__(self, pointA, pointB, resting_length=100, spring_power=1):
            self.pointA = pointA
            self.pointB = pointB
            self.resting_length = resting_length
            self.spring_power = spring_power
            self.mid = [self.pointB.x-self.pointA.x, self.pointB.y-self.pointA.y]
            self.speed1 = 0
            self.speed2 = 0
            self.k = -0.1
            
        def step(self):
            self.mid = [self.pointB.x-self.pointA.x, self.pointB.y-self.pointA.y]
            dX1, dY1 = delta((self.pointB.x, self.pointB.y), (self.pointA.x, self.pointA.y))
            dX2, dY2 = dX1, -dY1
            b1, d1 = RectToPolar(dX1, dY1)
            b2, d2 = RectToPolar(dX2, dY2)
            dX1 *= -self.k*(self.resting_length-d1)*self.spring_power
            dY1 *= self.k*(self.resting_length-d1)*self.spring_power
            dX2 *= -self.k*(d2-self.resting_length)*self.spring_power
            dY2 *= -self.k*(d2-self.resting_length)*self.spring_power
            self.pointA.hspeed += dX1/1000
            self.pointA.vspeed -= dY1/1000
            self.pointB.hspeed += dX2/1000
            self.pointB.vspeed -= dY2/1000
        
        def draw(self):
            draw.line(self.pointA.screen, (0, 0, 0), (self.pointA.x, self.pointA.y), (self.pointB.x, self.pointB.y))

    
    class Ball():
        def __init__(self, screen, gravityObj: Gravity, sides=6, size=100, centerx=320, centery=240, spring_power=2,
                    max_speed=10, friction=0.1, draw_points=False, draw_springs=False, draw_center=False):
            self.screen = screen
            self.sides = sides
            self.size = size
            self.centerx = centerx
            self.centery = centery
            self.spring_power = spring_power
            self.gravityObj = gravityObj
            self.max_speed = max_speed
            self.friction = friction
            self.draw_points = draw_points
            self.draw_springs = draw_springs
            self.draw_center = draw_center
            self.points = []
            self.springs = []
            self.pointPairs = []

            for i in range(self.sides):
                self.pointPairs.append((0,0))

            self.total_angles = (self.sides-2)*180
            self.single_angle = self.total_angles/self.sides
            self.long_size1 = math.sqrt(size**2+size**2-2*size*size*math.cos(math.radians(self.single_angle)))
            self.long_size2 = self.long_size1/(math.sin(math.radians(self.single_angle)))
            for s in range(self.sides):
                self.points.append(SoftBody.Point(self.screen, self.centerx+lengthdir_x(size, 360/self.sides*s), self.centery+lengthdir_y(size, 360/self.sides*s),
                                        self.gravityObj, size=5, max_speed=self.max_speed, friction=self.friction))
            for sp in range(self.sides):
                self.springs.append(SoftBody.Spring(self.points[sp], self.points[(sp-1)%self.sides], self.size, self.spring_power))
                self.springs.append(SoftBody.Spring(self.points[sp], self.points[(sp-2)%self.sides], self.long_size1, self.spring_power))
                self.springs.append(SoftBody.Spring(self.points[sp], self.points[(sp-3)%self.sides], self.long_size2, self.spring_power))
        def step(self, mouse, mouse_x, mouse_y):
            if mouse:
                nearest = nearest_object([mouse_x, mouse_y], self.points)
                nearest.x = mouse_x
                nearest.y = mouse_y

            i=0
            if self.draw_center:
                mid = [0,0]
            for point in self.points:
                point.step()
                if self.draw_center:
                    mid[0] += point.x
                    mid[1] += point.y
                self.pointPairs[i]=(point.x, point.y)
                i += 1
            for spring in self.springs:
                spring.step()

            draw.polygon(self.screen,(255, 0, 0), self.pointPairs)
            if self.draw_points:
                for point in self.points:
                    point.draw()
            if self.draw_springs:
                for spring in self.springs:
                    spring.draw()
            if self.draw_center:
                mid[0] /= len(self.points)
                mid[1] /= len(self.points)
                draw.circle(self.screen, (0, 0, 255), mid, 20)


class Inverse_kinematics():


    class Segment():

        def __init__(self, length, parent):
            self.length = length
            self.parent = parent
            self.start = Coords()
            self.end = Coords()
        
        def step(self, lineType: int=1, mouse: list=[0, 0]):
            """Performs the step function each frame.

            Args:
                mouse (list): [mouse_x, mouse_y]
                lineType (int, optional): 0 = Beginning line, 1 = Middle, 2 = End. Defaults to 1.
            """
            if lineType == 1:
                
                dX = self.parent.start.x - self.start.x
                dY = self.parent.start.y - self.start.y
                direction = point_direction_diff(dX, dY)

                self.end.x = self.parent.start.x
                self.end.y = self.parent.start.y

                dX, dY = PolarToRect(-direction, self.length)
                self.start.x = self.end.x - dX
                self.start.y = self.end.y - dY

            elif lineType == 0:
                dX = mouse[0] - self.start.x
                dY = mouse[1] - self.start.y
                direction = point_direction_diff(dX, dY)

                self.end.x = mouse[0]
                self.end.y = mouse[1]

                dX, dY = PolarToRect(-direction, self.length)
                self.start.x = self.end.x - dX
                self.start.y = self.end.y - dY

        def Draw(self, screen, color):    
            draw.line(screen, color, [self.start.x, self.start.y], [self.end.x, self.end.y], 2)


    class Arm():
        
        def __init__(self, num, length, color):
            self.num = num
            self.length = length
            self.color = color
            self.segments = []
            for i in range(self.num):
                if i == 0:
                    self.segments.append(Inverse_kinematics.Segment(self.length, None))
                else:
                    self.segments.append(Inverse_kinematics.Segment(self.length, self.segments[i-1]))

        def step(self, screen, end: list, lockX, lockY):
            i=0
            for seg in self.segments:
                if seg.parent is None:
                    seg.step(lineType=0, mouse=end)
                else:
                    seg.step()
                if i == self.num -1:
                    dX = lockX - seg.start.x
                    dY = lockY - seg.start.y
                    for seg2 in self.segments:
                        seg2.start.x += dX
                        seg2.start.y += dY
                        seg2.end.x += dX
                        seg2.end.y += dY
                        seg2.Draw(screen, (255, 0, 0))
                i += 1


class Grass():
    def __init__(self, baseCoords: Coords=Coords()):
        self.height = 12
        self.width = 3
        self.velocity = 0
        self.rotation = 0
        self.baseCoords = baseCoords
        self.topCoords = baseCoords

    def step(self, screen):
        # Movement
        if self.velocity > 0.1 or self.velocity < 0.1:
            self.rotation += self.velocity/5
            self.velocity /= 5
        elif self.rotation > 0.1 or self.rotation < 0.1:
            self.velocity = -self.rotation/2
        # End point
        self.topCoords.x = self.baseCoords.x + (sin(self.rotation) * self.height)
        self.topCoords.y = self.baseCoords.y + (cos(self.rotation) * self.height)
        

        draw.line(screen, (0, 222, 0), [self.baseCoords.x, self.baseCoords.y], [self.baseCoords.x, self.baseCoords.y - 12], self.width)
