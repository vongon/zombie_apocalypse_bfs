"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
#import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7



class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list[:] = []
        self._zombie_list[:] = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        index = 0
        while (index < len(self._zombie_list)):
            yield self._zombie_list[index]
            index += 1
        return

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        index = 0
        while (index < len(self._human_list)):
            yield self._human_list[index]
            index += 1
        return
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        if(entity_type == HUMAN): 
            entity_list = self._human_list
        elif(entity_type == ZOMBIE): 
            entity_list = self._zombie_list
        else: 
            return #invalid input

        visited = poc_grid.Grid(self.get_grid_height(), self.get_grid_width())
        product = self._grid_width * self._grid_height
        distance_field = [[product for dummy_col in range(self._grid_width)]
                            for dummy_row in range(self._grid_height)] 

        boundary = poc_queue.Queue()
        for item in entity_list:
            boundary.enqueue(item)
            visited.set_full(item[0],item[1])
            distance_field[item[0]][item[1]] = 0

        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            for neighbor in self.four_neighbors(current_cell[0],current_cell[1]):
                if(visited.is_empty(neighbor[0], neighbor[1]) and self.is_empty(neighbor[0], neighbor[1])):
                    visited.set_full(neighbor[0], neighbor[1]) #add to visited
                    boundary.enqueue(neighbor) #add to boundary queue
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1

        return list(distance_field)
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for index, human in enumerate(self._human_list):
            neighbors = self.eight_neighbors(human[0], human[1])
            neighbors.append(human) #staying in place may be best move
            avaialable_neighbors = [ neighbor for neighbor in neighbors if self.is_empty(neighbor[0],neighbor[1]) ]
            max_dist = max(zombie_distance_field[neighbor[0]][neighbor[1]] for neighbor in avaialable_neighbors)
            max_moves = []
            for neighbor in avaialable_neighbors:
                if (zombie_distance_field[neighbor[0]][neighbor[1]] == max_dist and self.is_empty(neighbor[0],neighbor[1])):
                    max_moves.append(neighbor)
            if(len(max_moves) > 0):
                self._human_list[index] = random.choice(max_moves)

    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for index, zombie in enumerate(self._zombie_list):
            neighbors = self.four_neighbors(zombie[0], zombie[1])
            neighbors.append(zombie) #staying in place may be best move
            avaialable_neighbors = [ neighbor for neighbor in neighbors if self.is_empty(neighbor[0],neighbor[1]) ]
            min_dist = min(human_distance_field[neighbor[0]][neighbor[1]] for neighbor in avaialable_neighbors)
            min_moves = []
            for neighbor in avaialable_neighbors:
                if (human_distance_field[neighbor[0]][neighbor[1]] == min_dist and self.is_empty(neighbor[0],neighbor[1])):
                    min_moves.append(neighbor)
            if(len(min_moves) > 0):
                self._zombie_list[index] = random.choice(min_moves)

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))




