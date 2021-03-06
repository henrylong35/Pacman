import pygame, random
from settings import *

vec = pygame.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        self.app = app
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.radius = int(self.app.cell_width//2.3)
        self.number = number
        self.color = self.set_color()
        self.direction = vec(1, 0)
        self.personality = self.set_personality()

    def update(self):
        self.pix_pos += self.direction
        if self.time_to_move:
            self.move()
        
        self.grid_pos[0] = (self.pix_pos[0]-top_bottom_buffer+self.app.cell_width//2)//self.app.cell_width+1
        self.grid_pos[1] = (self.pix_pos[1]-top_bottom_buffer+self.app.cell_height//2)//self.app.cell_height+1


    def draw(self):
        pygame.draw.circle(self.app.screen, self.color,(int(self.pix_pos.x), int(self.pix_pos.y)), self.radius)

    def time_to_move(self):
        if int(self.pix_pos.x+top_bottom_buffer//2) % self.app.cell_width == 0:
            if self.direction == vec(1,0) or self.direction == vec(-1,0):
                return True
        if int(self.pix_pos.y+top_bottom_buffer//2) % self.app.cell_height == 0:
            if self.direction == vec(0,1) or self.direction == vec(0,-1):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction()
        if self.personality == "speedy":
            self.direction = self.get_path_direction()
        if self.personality == "scared":
            self.direction = self.get_path_direction()
    
    def get_path_direction(self):
        next_cell = self.find_next_cell_in_path()
        xdir = next_cell[0] - self.grid_pos[0]
        ydir = next_cell[1] - self.grid_pos[1]
        return vec(xdir, ydir)

    def find_next_cell_in_path(self):
        path = self.BFS([int(self.grid_pos.x), int(self.grid_pos.y)], [int(self.app.player.grid_pos.x), int(self.app.player.grid_pos.y)]) 
        return path[1]

    def BFS(self, start, target):
        grid = [[0 for x in range(28)] for x in range(30)]
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                neighbors = [[0, -1],[1, 0],[0, 1],[-1, 0]]
                for neighbor in neighbors:
                    if neighbor[0]+current[0] >= 0 and neighbor[0]+current[0] < len(grid[0]):
                        if neighbor[1]+current[1] >= 0 and neighbor[1]+current[1] < len(grid):
                            next_cell = [neighbor[0] + current[0], neighbor[1] + current[1]]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        while target != start:
            for step in path:
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def get_random_direction(self):
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)



    def get_pix_pos(self):
        return vec((self.grid_pos.x*self.app.cell_width)+top_bottom_buffer//2+self.app.cell_width//2, (self.grid_pos.y*self.app.cell_height)+top_bottom_buffer//2+self.app.cell_height//2)

    def set_color(self):
        if self.number == 0:
            return (28, 0, 255)
        if self.number == 1:
            return (57, 255, 34)
        if self.number == 2:
            return (252, 85, 8)
        if self.number == 3:
            return (255, 0, 255)

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

