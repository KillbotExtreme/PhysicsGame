import draw
from helper_functions import point_direction_diff, PolarToRect, delta

class Inverse_kinematics():

    class Coords():
        def __init__(self):
            self.x = 0
            self.y = 0

    class Segment():

        def __init__(self, length, parent):
            self.length = length
            self.parent = parent
            self.start = Inverse_kinematics.Coords()
            self.end = Inverse_kinematics.Coords()
        
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

        def draw(self, screen, color):    
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

        def step(self, screen, mouse_x, mouse_y, lockX, lockY):
            i=0
            for seg in self.segments:
                if seg.parent is None:
                    seg.step(lineType=0, mouse=[mouse_x, mouse_y])
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
                        seg2.draw(screen, (255, 0, 0))
                i += 1
