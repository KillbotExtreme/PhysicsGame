from math import sqrt, atan2, sin, cos, pi, radians, degrees


def delta(point1: list[float], point2: list[float]) -> float:
    """
    Returns the differences in x and y between 2 coordinates.
         
    Args:
        point1 (list[float]): x and y positions of point 1
        point2 (list[float]): x and y positions of point 2

    Returns:
        deltaX, deltaY
    """
    deltaX = point2[0]-point1[0]
    deltaY = point2[1]-point1[1]
    
    return deltaX, deltaY
    

def distance_to_object(obj1, obj2) -> float:
    """
    Returns the distance between 2 objects.

    Args:
        obj1 (obj): Object1
        obj2 (obj): Object2

    Returns:
        float: distance
    """
    dX, dY = delta([obj1.x, obj1.y], [obj2.x, obj2.y])
    
    return sqrt(dX**2 + dY**2)


def nearest_object(originPoint: list[float], objectList: list):
    """
    Checks over a list of objects to find which is closest to the origin point.

    Args:
        originPoint (list[float]): x, y co-ordinates to check against
        objectList (list): List of objects to check

    Returns:
        object: nearest
    """
    dist = 9999999999
    nearest = 0
    for obj in objectList:
        dX, dY = delta([originPoint[0], originPoint[1]], [obj.x, obj.y])
        temp_dist = sqrt(dX**2 + dY**2)
        if temp_dist < dist:
            dist = temp_dist
            nearest = obj

    return nearest


def point_direction(obj1, obj2) -> float:
    """
    Returns the direction obj1 -> obj2 in decimal degrees.

    Args:
        obj1 (obj): Origin Object
        obj2 (obj): Destination object

    Returns:
        float: direction
    """
    dX, dY = delta([obj1.x, obj1.y], [obj2.x, obj2.y])
    bearing = -(degrees(atan2(-dY, dX))-90)
    direction = -(360 + bearing) if bearing < 0 else -bearing

    return direction


def point_direction_diff(dX, dY):
    
    bearing = -(degrees(atan2(-dY, dX))-90)
    direction = -(360 + bearing) if bearing < 0 else -bearing

    return direction

    
def RectToPolar(deltaX: float, deltaY: float) -> float:
    """
    Converts the differences in x and y between 2 coordinates into a bearing and a distance in degrees.
    
    Args:
        deltaX (float): Difference in x coordinates of 2 points
        deltaY (float): Difference in y coordinates of 2 points
         
    Returns:
        float: bearing, float: distance
    """
    bearing = atan2(-deltaY, deltaX)
    bearing = degrees(bearing)
    bearing = -(bearing-90)
    if bearing < 0:
        bearing = 360 + bearing
    distance = sqrt(deltaX**2 + deltaY**2)
    bearing = -bearing
    
    return bearing, distance


def PolarToRect(bearing: float, distance: float) -> float:
    """
    Converts a bearing and a distance into a difference in x and y coordinates.
    
    Args:
        bearing: The direction from 1 point to another
        distance: The straight line distance between the points
         
    Returns:
        deltaX, deltaY
    """
    deltaX = sin(radians(bearing))*distance
    deltaY = -cos(radians(bearing))*distance
    
    return deltaX, deltaY  


def lengthdir_x(length: float, direction: float) -> float:
    """
    Returns an updated x position from a length and a direction
    
    Args:
        length(pixels): length from start to destination
        direction(degrees): direction from start to destination
    
    Returns:
        float: x
    """
    x, y = PolarToRect(-direction, length)
    return x


def lengthdir_y(length: float, direction: float) -> float:
    """
    Returns an updated x position from a length and a direction
    
    Args:
        length(pixels): length from start to destination
        direction(degrees): direction from start to destination
    
    Returns:
        float: y
    """
    x, y = PolarToRect(-direction, length)
    return y
    

# def player_movement(up: bool, down: bool, left: bool, right: bool, x, y, speed, collision_objects: list):
#     """
#     Controls movement and collision of a player
    
#     Args:
#      - up, down, left, right (bool): Checks if the directions have an input
#      - rect: The current location of the object
#      - speed: speed of the object
#      - collision_objects: a list of all objects that can be  collided with
    
#     Returns:
#      - x, y
#     """
#     slow = sqrt((speed**2)/2)
#     Mintop, Minbot, Minleft, Minright = 999, 999, 999, 999
#     if collision_objects is not None:
#         for obj in collision_objects:
#             #top
#             if obj.rect.right > rect.left and obj.rect.left < rect.right:
#                 if obj.rect.bottom <= rect.top:
#                     Mintop = ((rect.y-16) - (obj.rect.y+16)) if ((rect.y-16) - (obj.rect.y+16)) < Mintop else Mintop
#             #bottom
#                 if obj.rect.top >= rect.bottom:
#                     Minbot = ((obj.rect.y-16)-(rect.y+16)) if ((obj.rect.y-16)-(rect.y+16)) < Minbot else Minbot
#             #left
#             if obj.rect.top < rect.bottom and obj.rect.bottom > rect.top:
#                 if obj.rect.right <= rect.left:
#                     Minleft = ((rect.x-16) - (obj.rect.x+16)) if ((rect.x-16) - (obj.rect.x+16)) < Minleft else Minleft
#             #right
#                 if obj.rect.left >= rect.right:
#                     Minright = ((obj.rect.x-16)-(rect.x+16)) if ((obj.rect.x-16)-(rect.x+16)) < Minright else Minright
#     if up:
#         if left or right:
#             y = y-Mintop if Mintop <= slow else y-slow
#         else:
#             y = y-Mintop if Mintop <= speed else y-speed
#     if down:
#         if left or right:
#             y = y+Minbot if Minbot <= slow else y+slow
#         else:
#             y = y+Minbot if Minbot <= speed else y+speed
#     if left:
#         if up or down:
#             x = x-Minleft if Minleft <= slow else x-slow
#         else:
#             x = x-Minleft if Minleft <= speed else x-speed
#     if right:
#         if up or down:
#             x = x+Minright if Minright <= slow else x+slow
#         else:
#             x = x+Minright if Minright <= speed else x+speed
#     return x, y




