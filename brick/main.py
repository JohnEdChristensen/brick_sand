import pyxel
from enum import Enum

WIDTH = 80
HEIGHT = 80


class particleType(Enum):
    empty= 0
    sand = 10
    water = 1


def findOpenWaterSpace(grid,x,y):
    #check left
    xl = x
    while xl > 1:
        xl -=1
        if grid[xl][y] == particleType.empty:
            return (xl,y)
        if grid[xl][y] != particleType.water:
            break
    #check the right
    xr = x
    while xr  < WIDTH-1:
        xr +=1
        if grid[xr][y] == particleType.empty:
            return (xr,y)
        if grid[xr][y] != particleType.water:
            break
    return (x,y-1)

class App:
    grid: list[list[particleType]] = [[]]
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT)
        self.grid = [[particleType.empty]* WIDTH for _ in range(HEIGHT)]
        
        self.grid[WIDTH//2][HEIGHT//2] = particleType.sand
        pyxel.mouse(visible=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        #newGrid = deepcopy(self.grid)
        newGrid = [[particleType.empty]* WIDTH for _ in range(HEIGHT)]

            

        for x,row in enumerate(self.grid):
            for y,particle in enumerate(row):
                if particle == particleType.sand:
                    print(particle)

                match particle:
                    case particleType.sand:
                        if y>0 and y < HEIGHT-1 and x >0 and x < WIDTH-1:
                            if self.grid[x][y+1] == particleType.sand:
                                # Deterimine which way to fall
                                if self.grid[x-1][y+1] != particleType.sand:
                                    newGrid[x-1][y+1] = particleType.sand
                                elif self.grid[x+1][y+1] != particleType.sand:
                                    newGrid[x+1][y+1] = particleType.sand
                                else:
                                    newGrid[x][y] = particleType.sand
                            else:
                                newGrid[x][y+1] = particleType.sand
                        else:
                            newGrid[x][y] = particleType.sand
                    case particleType.water: # Does not work correctly!
                        if y>0 and y < HEIGHT-1 and x >0 and x < WIDTH-1:
                            if self.grid[x][y+1] != particleType.empty:
                                # Deterimine which way to fall
                                if self.grid[x-1][y+1] == particleType.empty:
                                    newGrid[x-1][y+1] = particleType.water
                                elif self.grid[x+1][y+1] == particleType.empty:
                                    newGrid[x+1][y+1] = particleType.water
                                else:
                                    newGrid[x][y] = particleType.water
                            # If there is water above, try to let it flow into the current row
                            if (self.grid[x][y-1] == particleType.water and self.grid[x][y-1] == particleType.water):
                                water_x,water_y = findOpenWaterSpace(self.grid,x,y)
                                newGrid[water_x][water_y] = particleType.water
                                newGrid[x][y] = particleType.empty
                            else:
                                newGrid[x][y+1] = particleType.water
                        else:
                            newGrid[x][y] = particleType.water
        self.grid = newGrid 
        
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            if y>1 and y < HEIGHT-1 and x >1 and x < WIDTH-1:
                self.grid[pyxel.mouse_x][pyxel.mouse_y] = particleType.sand
        if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            if y>1 and y < HEIGHT-1 and x >1 and x < WIDTH-1:
                self.grid[pyxel.mouse_x][pyxel.mouse_y] = particleType.water

    def draw(self):
        pyxel.cls(0)
        for x,row in enumerate(self.grid):
            for y,particle in enumerate(row):
                pyxel.rect(x,y,1,1,particle.value)
        pyxel.text(2,2,"Left Click: Sand",13)
        pyxel.text(2,10,"Right Click: Water",13)

App()
