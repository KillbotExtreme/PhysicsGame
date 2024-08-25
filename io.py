import pygame as pg


def Input(scroll) -> bool:
    """
    Checks for keyboard/mouse inputs and returns as True or False
    
    Returns (bool):
     - up, down, left, right, MBL
    """
    keys = pg.key.get_pressed()
    up = True if keys[pg.K_w] else False
    down = True if keys[pg.K_s] else False
    left = True if keys[pg.K_a] else False
    right = True if keys[pg.K_d] else False
    MBM = True if pg.mouse.get_pressed()[1] else False
    MBL = True if pg.mouse.get_pressed()[0] else False
    CCW = True if keys[pg.K_q] else False
    CW = True if keys[pg.K_e] else False
    zoomIn = True if scroll == 1 else False
    zoomOut = True if scroll == -1 else False

    return up, down, left, right, MBM, MBL, CW, CCW, zoomIn, zoomOut


def level(level: str):
    """
    Loads a level .txt into an array
    
    Args:
     - level (str): level number of the file
    
    Returns:
     - Lvl (array[16][21])
    """
    LvlTxt = open("F:/91. Python/02. Test/resources/levels/level"+level+".txt","r+")
    temptxt = list(LvlTxt.read())
    for i in range(15):
        temptxt.remove("\n")
    for o in range(336):
        temptxt[o] = int(temptxt[o])
        temptxt2 = np.array(temptxt).reshape(16, 21)
    Lvl = temptxt2

    return Lvl


def Levels(*args):
    """
    Accepts unlimited string inputs and turns them into levels.
    
    Args:
     - *args: Level names. As many as needed.
    
    Returns:
     - levels (A list of arrays. Separate these when calling the function)
    """
    levels = []
    for a in args:
        levels.append(level(a))
        
    return levels