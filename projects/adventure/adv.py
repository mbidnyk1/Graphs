from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def get_opposite_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'

def bfs(traversal_graph,starting_room, target):
    q = Queue()
    visited = set()
    q.enqueue([starting_room])

    while q.size() > 0:
        
        path = q.dequeue()
        v = path[-1]
        # print(traversal_graph[v])
        # print(path)
        if v not in visited:
            for direction in traversal_graph[v]:
                if traversal_graph[v][direction] == target:
                    return path
            visited.add(v)

            for direction in traversal_graph[v]:
                new_path = list(path)
                new_path.append(traversal_graph[v][direction])
                # print(check_room.id)
                q.enqueue(new_path)
            

    return None
# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
# Print an ASCII map
world.print_rooms()
player = Player(world.starting_room)
# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
# visited_rooms.add(player.current_room)
traversal_graph = {}
came_from = ''
prev_id = 0
bfs_path=[]
while len(visited_rooms) != len(room_graph):
# for x in range(len(room_graph)):
    if player.current_room not in visited_rooms:
        exits = player.current_room.get_exits()
        unexplored_direction = {}
        for direction in exits:
            unexplored_direction[direction] = '?'
        traversal_graph[player.current_room.id] = unexplored_direction
        # print(traversal_graph[player.current_room.id])
        visited_rooms.add(player.current_room)
    
    if len(visited_rooms) > 1:
        traversal_graph[player.current_room.id][came_from] = prev_id
    
    possible_direction = []    
    
    for direction in traversal_graph[player.current_room.id]:
        if traversal_graph[player.current_room.id][direction] == '?':
            possible_direction.append(direction)
            # print(direction)
    if not possible_direction:
        path = bfs(traversal_graph,player.current_room.id,'?')
        if path == None:
            break
        else:
            i = 0 
            for i in range(len(path)-1):
                # print(path_id)
                for key in traversal_graph[path[i]]:
                    if traversal_graph[path[i]][key] == path[i+1]:
                        print(key)
                        traversal_path.append(key)
                        bfs_path.append(key)
            for move in bfs_path:
                # print(bfs_path)
                player.travel(move)
            if player.current_room not in visited_rooms:
                exits = player.current_room.get_exits()
                unexplored_direction = {}
                for direction in exits:
                    unexplored_direction[direction] = '?'
                traversal_graph[player.current_room.id] = unexplored_direction
                # print(traversal_graph[player.current_room.id])
                visited_rooms.add(player.current_room)
            for direction in traversal_graph[player.current_room.id]:
                if traversal_graph[player.current_room.id][direction] == '?':
                    possible_direction.append(direction)
            print(player.current_room.id)
            print(possible_direction)
            
        
    random.shuffle(possible_direction)
    rand_direction = possible_direction[0]
    prev_id = player.current_room.id
    next_room = player.current_room.get_room_in_direction(rand_direction)
    next_id = next_room.id
    traversal_graph[player.current_room.id][rand_direction] = next_id
    came_from = get_opposite_direction(rand_direction)
    player.travel(rand_direction)
    traversal_path.append(rand_direction)
    # print(rand_direction)
    print(traversal_graph)
   

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


# invalid_rooms = direction - player.current_room.get_exits()
# s = Stack()
# s.push(player.current_room)

# while s.size() > 0:
#     v = s.pop()
#     if v not in visited_rooms:
#         visited_rooms.add(v)
#         unexplored_direction = player.current_room.get_exits()
#         random.shuffle(unexplored_direction)
#         for rand_direction in unexplored_direction:
#             next_room = v.get_room_in_direction(rand_direction)
#             s.push(next_room)
#         player.travel(rand_direction)
#         traversal_path.append(rand_direction)




# for move in traversal_path:
#     player.travel(move)

    #chosen_direction is a (random direction - curr_direction)
    #and is unexplored from current room
    #move(chosen_direction)
    #add that direction to a log
    #loop
    
    # unexplored_direction = player.current_room.get_exits()
    # random.shuffle(unexplored_direction)
    # player.travel(unexplored_direction[0],False)
    # visited_rooms.add(player.current_room)
    
    # for prev_room in visited_rooms:
    #     if prev_room.get_exits() 
    
#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
