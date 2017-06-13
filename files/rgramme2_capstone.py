import random
import csv
import copy
from collections import Counter
from Queue import PriorityQueue

terrain_costs = { '.': 1, '*': 3, '^': 5, '~': 7}
terrain_list = ['.','*','^','~']
map_moves = [(0,-1), (1,0), (0,1), (-1,0)]
move_probabilities = {'E': .65, 'F': .70, 'W': .75, 'A': .80, 'V': .85}
planes = {'E': 'Earth', 'A': 'Wind', 'F': 'Fire', 'W': 'Water', 'V': 'Void'}
sun = ['rising', 'setting']
moon = ['waxing', 'waning']
seasons = ['fall', 'winter', 'summer', 'spring']

#read files in
def read_world( filename):
    with open( filename, 'r') as f:
        world_data = [x for x in f.readlines()]
    f.closed
    world = []
    for line in world_data:
        line = line.strip()
        if line == "": continue
        world.append([x for x in line])
    return world


with open('map_characteristics.txt', 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    map_characteristics = list(spamreader)
random.shuffle(map_characteristics)

map01_grid = read_world('map01.txt')
map02_grid = read_world('map02.txt')
map03_grid = read_world('map03.txt')
map04_grid = read_world('map04.txt')
planes_map = read_world('planes_map_revised.txt')

#code for the game that Degi plays against the spirits
def game():
    game_choices = ['Safe Bridge', 'Haunted Forest', 'Cobra Bridge', 'Mine Field', 'Icy Mountain']
    spirit_choice = random.randint(0, 4)
    spirit_choice = game_choices[spirit_choice]
    print('Spirit chose ' + repr(spirit_choice) + '!')
    degi_choice = game_choices[2]
    print('Degi chose ' + repr(degi_choice) + '!')
    if spirit_choice == degi_choice:
        print("Same choices, play again!")
    elif spirit_choice == 'Safe Bridge':
        if degi_choice == 'Icy Mountain' or degi_choice == 'Mine Field':
            print("Spirit wins!")
            return True
        else:
            print("Degi wins!")
            return False
    elif spirit_choice == 'Cobra Bridge':
        if degi_choice == 'Haunted Forest' or degi_choice == 'Safe Bridge':
            print("Spirit wins!")
            return True
        else:
            print("Degi wins!")
            return False
    elif spirit_choice == 'Mine Field':
        if degi_choice == 'Cobra Bridge' or degi_choice == 'Icy Mountain':
            print("Spirit wins!")
            return True
        else:
            print("Degi wins!")
            return False
    elif spirit_choice == 'Haunted Forest':
        if degi_choice == 'Mine Field' or degi_choice == 'Safe Bridge':
            print("Spirit wins!")
            return True
        else:
            print("Degi wins!")
            return False
    elif spirit_choice == 'Icy Mountain':
        if degi_choice == 'Haunted Forest' or degi_choice == 'Cobra Bridge':
            print("Spirit wins!")
            return True
        else:
            print("Degi wins!")
            return False

#get classification data based on seasons, etc
def classify(training_data):
    class_values = []
    probabilities = {}
    for i in range(0, len(training_data)):
        class_values.append(training_data[i][3])
    class_keys = Counter(class_values).keys()
    class_counts = Counter(class_values).values()
    for r in range(0, len(class_keys)):
        probabilities[class_keys[r]] = {}
        probabilities[class_keys[r]][0] = class_counts[r]/len(training_data)
        for j in range(0, len(training_data[0])-1):
            probabilities[class_keys[r]][j] = []
            attribute_values = []
            for k in range(0, len(training_data)):
                if training_data[k][3] == class_keys[r]:
                    attribute_values.append(training_data[k][j])
            attribute_keys = Counter(attribute_values).keys()
            attribute_value_counts = Counter(attribute_values).values()
            for k in range(0, len(attribute_keys)):
                probabilities[class_keys[r]][j].append((attribute_keys[k], (attribute_value_counts[k]+1.0)/(len(attribute_values)+1.0))) 
            probabilities[class_keys[r]][j] = sorted(probabilities[class_keys[r]][j], key=lambda tup: tup[1], reverse = True)                        
    return probabilities, class_keys

#select map based on classification data
def selectMap():
    current_sun = sun[random.randint(0, 1)]
    current_moon = moon[random.randint(0, 1)]
    current_season = seasons[random.randint(0, 1)]
    print('The current sun is ' + repr(current_sun) + ', the current moon is ' + repr(current_moon) + ' and the current season is ' + repr(current_season))
    map_probabilities, map_names = classify(map_characteristics)
    map_counts = {map_names[0]: 0, map_names[1]: 0, map_names[2]: 0, map_names[3]: 0}
    for key in map_names:
        if(map_probabilities[key][0][0][0] == current_sun):
            map_counts[key] += 1
        if(map_probabilities[key][1][0][0] == current_moon):
            map_counts[key] += 1
        if(map_probabilities[key][2][0][0] == current_season):
            map_counts[key] += 1
    map_counts = sorted(map_counts, key=map_counts.get, reverse=True)
    map_choice = map_counts[0]
    print('This means that Degi will use ' + repr(map_choice) + ' to navigate')
    if(map_choice == 'map01'):
        map_choice = list(map01_grid)
    elif(map_choice == 'map02'):
        map_choice = list(map02_grid)
    elif(map_choice == 'map03'):
        map_choice = list(map03_grid)
    elif(map_choice == 'map04'):
        map_choice = list(map04_grid)
    return map_choice

#randomly place shrines on map, make sure no shrine is placed on water or where another shrine has been placed
def placeShrines(selected_map):
    water_location = []
    for y in range(0, len(selected_map)):
        for x in range(0, len(selected_map[0])):
            if selected_map[y][x] == '~':
                water_location.append((y, x))
    earth_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    water_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    wind_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    fire_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    void_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    while earth_shrine_location in water_location:
        earth_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    while water_shrine_location in water_location or water_shrine_location == earth_shrine_location:
        water_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    while wind_shrine_location in water_location or wind_shrine_location == earth_shrine_location or wind_shrine_location == water_shrine_location:
        wind_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    while fire_shrine_location in water_location or fire_shrine_location == earth_shrine_location or fire_shrine_location == water_shrine_location or fire_shrine_location == wind_shrine_location:
        fire_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    while void_shrine_location in water_location or void_shrine_location == earth_shrine_location or void_shrine_location == wind_shrine_location or void_shrine_location == water_shrine_location or void_shrine_location == fire_shrine_location:
        void_shrine_location = (random.randint(0, len(selected_map)-1), random.randint(0, len(selected_map[0])-1))
    selected_map[earth_shrine_location[0]][earth_shrine_location[1]] = 'E'
    selected_map[water_shrine_location[0]][water_shrine_location[1]] = 'W'
    selected_map[wind_shrine_location[0]][wind_shrine_location[1]] = 'A'
    selected_map[fire_shrine_location[0]][fire_shrine_location[1]] = 'F'
    selected_map[void_shrine_location[0]][void_shrine_location[1]] = 'V'
    
    return selected_map

#A* Search Stuff
def heuristic(goal, next_point):
    (x1, y1) = goal
    (x2, y2) = next_point
    return abs(x1 - x2) + abs(y1 - y2) 

def create_path(goal, start, came_from, cost_so_far):
    path = []
    transition_cost = PriorityQueue()
    path.append(goal)
    i = 1
    while path[i-1] != start:
        for state in came_from:
            if state == path[i-1]:
                transition_cost.put(came_from[state], cost_so_far[came_from[state]])
        path.append(transition_cost.get()) 
        while not transition_cost.empty():
            transition_cost.get()
        i += 1
    return path

def get_next_point(current, move):
    next_point_coordinates = map(sum, zip(current, move))
    next_point = next_point_coordinates[0], next_point_coordinates[1]
    return next_point

def determine_costs(world, costs, goal, cost_so_far, came_from, current, frontier, next_point):
    terrain = world[next_point[1]][next_point[0]]
    new_cost = terrain_costs.get(terrain) 
    old_cost = cost_so_far[current]
    try:
        total_cost = new_cost + old_cost
    except:
        total_cost = new_cost
    if (next_point not in cost_so_far or total_cost < cost_so_far[next_point]) and terrain != "x" : 
        cost_so_far[next_point] = total_cost
        priority = new_cost + heuristic(goal, next_point)
        frontier.put(next_point, priority)
        came_from[next_point] = current
    
    return cost_so_far, came_from, frontier

def a_star_search( world, costs, start, goal, moves):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = start
    cost_so_far[start] = 0 
    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break   
        for move in map_moves:
            next_point = get_next_point(current, move)
            if next_point[1] >= 0 and next_point[0] >= 0 and next_point[1] <= len(world)-1 and next_point[0] <= len(world[0])-1:
                cost_so_far, came_from, frontier = determine_costs(world, costs, goal, cost_so_far, came_from, current, frontier, next_point)
    path = create_path(goal, start, came_from, cost_so_far)
    return path 

#print Degis path on the map
def print_path( world, shrine_map, path):
    for point in path:
        world[point[1]][point[0]] = "@"
    for y in range(0, len(shrine_map)):
        for x in range(0, len(shrine_map[0])):
            if(shrine_map[y][x] not in terrain_list):
                world[y][x] = shrine_map[y][x]
    for i in range(0, len(world)):
        print(world[i])

#value iteration to determine desired next plane
def nextMove(planes_map, current_plane_coordinates):
    if(current_plane_coordinates[0] > current_plane_coordinates[1]):
        move = (0, 1)
    elif(current_plane_coordinates[0] < current_plane_coordinates[1]):
        move = (1, 0)
    else:
        move = (1, 1)
    desired_move_probability = random.uniform(0, 1)
    desired_move = map(sum, zip(current_plane_coordinates, move))
    desired_plane = planes_map[desired_move[0]][desired_move[1]]
    if(desired_move_probability < move_probabilities[desired_plane]):
        current_plane_coordinates = map(sum, zip(current_plane_coordinates, move))
    else:
        undesired_move = (random.randint(-1, 1), random.randint(-1, 1))
        next_plane = map(sum, zip(current_plane_coordinates, undesired_move))
        while(next_plane[0] < 0 or next_plane[0] > len(planes_map)-1 or next_plane[1] < 0 or next_plane[1] > len(planes_map[0])-1):
            undesired_move = (random.randint(-1, 1), random.randint(-1, 1))
            next_plane = map(sum, zip(current_plane_coordinates, undesired_move))
        current_plane_coordinates = copy.deepcopy(next_plane)
    current_plane_coordinates = (current_plane_coordinates[0], current_plane_coordinates[1])
    return current_plane_coordinates, desired_plane
    
def main():
    print("In a small village in modern day Japan lives Degi and his parents ")
    print("Degi's parents are custodians of the local tourist attraction, a Shinto shrine ")
    print("dedicated to the kami(spirits) of godai(the five elements): chi(earth), sui(water), ka(fire), ")
    print("fu(wind), and ku(void or sky). ")
    print("'Degi...you must believe us...there is a war brewing between the elements that ")
    print("treatens to spill out into the Human Plane' says Degi's father at dinner. He has ")
    print("shared this news before, but Degi questions why the elements would start a war let ")
    print("alone how that war would spread out into the peaceful world that he knows. ")
    print("Recently there had been a few cases of extreme natrual occurances such as the ")
    print("landslide, thee fires, a windstorm, and a flood but Degi didn't think much of ")
    print("of those events becasue there was increasingly extreme weather around the world ")
    print("much of which meterologists had been blaming on global warming. Degi went on with ")
    print("his life the next day, once again not listening to the warnings of his father just ")
    print("as many other humans went on with their lives as the warnigns of the effects of global warming ")
    print("were shared by scientists and meterologists around the world every day. ")
    print("This day however, would be the different...")
    print("Walking home from the schoolhouse one day, Degi was startled by something that sent shivers ")
    print("down his spine. A spirit that was eight feet tall and had a body outlined by glowing orange flames appeared ")
    print("in front of him. The spirit was friendly towards Degi despite his firey body. The spirit shared with ")
    print("Degi that his parents had been kidnapped and needed to be saved before it was too late. ")
    print("As suddenly as the spirit had appeared in front of Degi, it was gone...")
    print("Degi sprinted home as fast as he could fearing the worst for his parents. He immediately burst into ")
    print("his father's office where he pulled out all of his father's notebooks onto the office floor and began ")
    print("reading through them as fast as possible. ")
    print("When Degi had finished reading the books he felt prepared to begin the journey to rescue his parents. ")
    print("He was able to pull the following facts from the books that would help him on his journey:")
    print(" 1. The well in the garden is a portal to the Elemental Plane which is itself composed of ")
    print("    multiple minor planes")
    print(" 2. There are five types of minor plane, one for each element: earth, water, fire, wind and void. ")
    print(" 3. Travel between the (minor) planes is accomplished by using the appropriate ")
    print("    portal on the plane. The portal is located at a shrine. So if youre on an earth ")
    print("    plane and wish to go the adjacent fire plane, you need to go to the fire shrine ")
    print("    and use the portal there. Of course, the shrine for the plane youre on is not a ")
    print("    portal. There will not necessarily be a shrine for every element on every plane ")
    print(" 4. Travel using the portals is somewhat random because of the mystical energies ")
    print("    used to power them. From the notes, it appears that if you take portal, most of ")
    print("    the time you end up at the desired destination but sometimes you end up on a ")
    print("    different elemental plane. ")
    print(" 5. Each shrine is guarded by spirit who challenges you to a game. If you win, you ")
    print("    may use the portal. If you lose, well, it appears the spirits are supposed to kill ")
    print("    you but theyre so bored and like playing games so much, they simply offer to ")
    print("    play you another game! The game that the spirits will challenge Degi to is called ")
    print("    'Sherrif vs. Fugitive'. The spirits like to be the Sherrif becasue they are the guardians ")
    print("    of their portals. Each player picks a strategy, 'Safe Brdige', 'Cobra Bridge', 'Haunted Forest', ")
    print("    'Mine Field', or 'Icy Mountain'. The Fuguitive is running from the Sherrif and so he can ")
    print("    run from the Sherrif on any of these terrains but the Sherrif has a better chance of getting ")
    print("    the fugitive on the simpler terrains. Based on his fathers journals Degi knows that he has ")
    print("    an advantage choosing the 'Cobra Bridge' as the fugitive.")
    print(" 6. The portals deposit you at a random location on the destination plane (whether it ")
    print("    is the intended one or a different one). Each plane has one of four possible ")
    print("    geographies and these are determined by the positions of the sun (rising, ")
    print("    setting, noon), the moon (waxing, waning) and the seasons (spring, summer, ")
    print("    autumn, winter). Believe it or not, the seasons change by the minute on the ")
    print("    elemental planes and you wont like the Fire Winter!!")
    print("With that knowledge in hand Degi sprinted out to the garden.")
    print("         ,")
    print("     -   \O")
    print("   -     /\ ")
    print("  -   __/\ `")
    print("     `    \,")
    print("^^^^^^^^^^^^")
    print("Without hesitation, Degi jumped striaight into the well and was sent directly to the elemental plane. ")
    print("Degi starts on the elemental plane " + repr(planes[planes_map[0][0]]) + " at (0, 0) on the planes map ")
    print("and knows that his parents are at the Water shrine at (4, 4) on the map.")
    print("The elemental map is: ")
    print("[E F W A V]")
    print("[W A V E F]")
    print("[V E F W A]")
    print("[F W A V E]")
    print("[A V E F W]")
    print("Degi knows that as he travels across the planes, he will mostly try to travel on the plains (marked by '.') which are ")
    print("the easiest terrain to cross, but would consider crossing forest (marked by '*'), then hills (marked by '^') and then ")
    print("water (marked by '~') in that order to get to his desired location as fast as possible. He will mark his path with the ")
    print("'@' symbol on the maps.")
    current_plane_coordinates = (0, 0)
    previous_plane = 'E'
    planes_visited = []
    #start loop here
    while current_plane_coordinates != (len(planes_map)-1, len(planes_map[0])-1):
        map_choice = selectMap()
        map_choice = copy.deepcopy(map_choice)
        a_star_map = copy.deepcopy(map_choice) 
        #place shrines randomly
        current_map = placeShrines(list(map_choice))
        current_plane_coordinates, desired_plane = nextMove(planes_map, current_plane_coordinates)
        planes_visited.append(current_plane_coordinates)
        for y in range(0, len(current_map)):
            for x in range(0, len(current_map)):
                if current_map[y][x] == desired_plane:
                    desired_shrine_location = (x, y)
        print('Degi is now on the ' + repr(planes[previous_plane]) + ' plane and needs to go to the ' + repr(planes[desired_plane]) + ' shrine, he takes the following path based on the map:')
        previous_plane = planes_map[current_plane_coordinates[0]][current_plane_coordinates[1]]
        full_path = a_star_search(a_star_map, terrain_costs, (random.randint(0, len(current_map)-1), random.randint(0, len(current_map[0])-1)), desired_shrine_location, map_moves)
        print_path(a_star_map, current_map, full_path)
        print('Degi is now at the ' + repr(planes[desired_plane]) + ' shrine and will challenge the shrine spirit!')
        play_game = game()
        while play_game != False:
            play_game = game()
        if(desired_plane != planes_map[current_plane_coordinates[0]][current_plane_coordinates[1]]):
            print('Oh no! The mystical energies in the portal system caused Degi to go to the ' + repr(planes[planes_map[current_plane_coordinates[0]][current_plane_coordinates[1]]]) + ' plane instead!')
    print('After a long and harrowing journey Degi has made it to the plane where his parents are being held...')
    print('He must traverse this plane to the Water Shrine and battle the Elemental King for his parents!')
    print('He takes the following journey across the plane...')
    map_choice = selectMap()
    map_choice = copy.deepcopy(map_choice)
    a_star_map = copy.deepcopy(map_choice) 
    #place shrines randomly
    current_map = placeShrines(list(map_choice))
    for y in range(0, len(current_map)):
        for x in range(0, len(current_map)):
            if current_map[y][x] == 'W':
                desired_shrine_location = (x, y)
    full_path = a_star_search(a_star_map, terrain_costs, (random.randint(0, len(current_map)-1), random.randint(0, len(current_map[0])-1)), desired_shrine_location, map_moves)
    print_path(a_star_map, current_map, full_path)
    print("Degi's journey across the Elemental Plane was as follows, marked by the '@' symbol:")
    for y in range(0, len(planes_map)):
        for x in range(0, len(planes_map[0])):
            if ((y, x)) in planes_visited:
                planes_map[y][x] = '@'
    planes_map[0][0] = '@'
    for i in range(0, len(planes_map)):
        print(planes_map[i])
    print("'Hello Degi...' says the Elemental King in a bellowing voice. 'I am impressed by your determination to save your parents. If you can beat me in a game of Sherrif vs Fugitive")
    print("'you will see them once again, lets play!'")
    print('  \_/')
    print('\_(@)_/')
    print(' _/ |_')
    play_game = game()
    while play_game != False:
        play_game = game()
    print('The Elemental King vanishes and Degi runs into the shrine where his parents are!')
    print('Mother! Father! You are alive!')
    print("Finally, Degi and his parents return safely to their home...")
    print(" (')) ^v^  _           (`)_")
    print("(__)_) ,--j j-------, (__)_)")
    print("      /_.-.___.-.__/ \    ")
    print("    ,8| [_],-.[_] | oOo")
    print(",,,oO8|_o8_|_|_8o_|&888o,,,")
main()