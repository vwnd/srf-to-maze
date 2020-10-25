"""
srf-to-maze

generation of a maze path in a uv-surface
based on th randomized depth-first search

ref.: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_implementation
"""

__author__ = "Victor Wanderley"
__contact__ = "victorwanderleyb@gmail.com"

import rhinoscriptsyntax as rs
import Rhino
from random import randint

class Cell:
    def __init__(self, i, j, visited=False):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.visited = False
        self.vertices(i, j)

        
    def vertices(self, i, j):
        u_pos = self.j * width
        v_pos = self.i * height
        self.pt1 = rs.EvaluateSurface(inputSrf, u_pos, v_pos)
        self.pt2 = rs.EvaluateSurface(inputSrf, u_pos, v_pos + height)
        self.pt3 = rs.EvaluateSurface(inputSrf, u_pos + width, v_pos + height) 
        self.pt4 = rs.EvaluateSurface(inputSrf, u_pos + width, v_pos)


def index(i, j):
    if i < 0 or j < 0 or i > vDiv -1 or j > uDiv - 1:
        return -1
    return i + j * vDiv
    
        
def DrawMaze(grid):
    for i in grid:
        cell = i
        # Draw lines
        if cell.walls[0]:
            left = rs.AddLine(cell.pt1, cell.pt2)
            mazeFrames.append(left)
        if cell.walls[1]:
            top = rs.AddLine(cell.pt2, cell.pt3)
            mazeFrames.append(top)
        if cell.walls[2]:
            right = rs.AddLine(cell.pt3, cell.pt4)
            mazeFrames.append(right)
        if cell.walls[3]:
            bottom = rs.AddLine(cell.pt4, cell.pt1)
            mazeFrames.append(bottom)
        
        # Make panel surface
        
        fill = rs.AddSrfPt([cell.pt1, cell.pt2, cell.pt3, cell.pt4])
        mazePanels.append(fill)

def checkNeighbours(current):
    neighbours = []
    left = top = right = bottom = -1
    
    if index(current.i, current.j-1) != -1:
        left = grid[index(current.i, current.j-1)]
    if index(current.i+1, current.j) != -1:
        top = grid[index(current.i+1, current.j)]
    if index(current.i, current.j+1) != -1:
        right = grid[index(current.i, current.j+1)]
    if index(current.i-1, current.j) != -1:
        bottom = grid[index(current.i-1, current.j)]
    
    if left != -1 and left.visited == False:
        neighbours.append(left)
    if top != -1 and top.visited == False:
        neighbours.append(top)
    if right != -1 and right.visited == False:
        neighbours.append(right)
    if bottom != -1 and bottom.visited == False:
        neighbours.append(bottom)
    
    if len(neighbours) == 0:
        return -1
    else:
        next_index = randint(0, len(neighbours)-1)
        next = neighbours[next_index]
        
        return next

def removeWalls(current, next):
    x = next.j - current.j
    if x == 1:
        current.walls[2] = False
        next.walls[0] = False
    if x == -1:
        current.walls[0] = False
        next.walls[2] = False
    y = next.i - current.i
    if y == 1:
        current.walls[1] = False
        next.walls[3] = False
    if y == -1:
        current.walls[3] = False
        next.walls[1] = False

def countVisited(grid):
    c = 0
    for i in grid:
        if i.visited == True:
            c += 1
    return c



# Main

if inputSrf:
    mazePanels = []
    mazeFrames = []
 
    
    # Obtain surface domains
    domainU = rs.SurfaceDomain(inputSrf, 0)
    domainV = rs.SurfaceDomain(inputSrf, 1)
    
    # Cell width and height
    
    width = (domainU[1] - domainU[0]) / uDiv
    height = (domainV[1] - domainV[0]) / vDiv
    
    # Create cells array
    grid = []
    stack = []
    
    for j in range(uDiv):
        for i in range(vDiv):
            cell = Cell(i, j)
            grid.append(cell)
    
    
    # Forward maze path
    
    current = grid[0] # Initial cell
    current.visited = True
    
    c = countVisited(grid)

    test = len(grid)
    
    while c < len(grid):
        next = checkNeighbours(current)
        if next != -1:
            stack.append(current)
            removeWalls(current, next)
            current = next
            current.visited = True
            c = countVisited(grid)
        if next == -1:
            if len(stack) > 0:
                current = stack.pop(-1)
    
    DrawMaze(grid)

# end of main