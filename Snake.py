from designer import *
from random import randint

World = { 'snake': DesignerObject,
          'snake segments': [DesignerObject],
          'snake speed': int,
          'direction': str,
          'food': DesignerObject,
          'previous x':[int],
          'previous y':[int],
          'boundary': DesignerObject,
          'score': int,
          'timer': int,
          'counter': DesignerObject,
          'counter2': DesignerObject,
          'halve step rate': int
          }

SNAKE_SPEED = 20
SEGMENTS_TO_ADD_AFTER_FOOD_IS_EATEN = 4

def create_world() -> World:
    '''
    Creates the world for the game
    
    Args:
        No arguments
    Returns:
        World: The world containing all the DesignerObjects needed for the game to run
    '''
    return { 'snake': create_snake(),
             'snake segments': [],
             'snake speed': SNAKE_SPEED,
             'food': create_food(),
             'direction': 'right',
             'previous x':[],
             'previous y':[],
             'boundary': create_boundary(),
             'score': 0,
             'timer': 0,
             'counter': text('black', '', 25, get_width()/2, 25),
             'counter2': text('black', '', 25, get_width()/2, 60),
             'halve step rate': 0
            }

def create_snake() -> DesignerObject:
    '''
    Creates the snake DesignerObject
    
    Args:
        No arguments
    Returns:
        DesignerObject: Returns a 19x19 lightgreen rectangle as the snake
    '''
    snake = rectangle('lightgreen', 19, 19)
    snake['x'] += 10
    snake['y'] += 10
    return snake

def create_food() -> DesignerObject:
    '''
    Creates the food DesignerObject
    
    Args:
        No arguments
    Returns:
        DesignerObject: Returns a 20x20 red rectangle as the food
    '''
    food = rectangle('red', 20, 20)
    teleport_food(food)
    return food

def teleport_food(food: DesignerObject):
    '''
    Teleports the food DesignerObject
    
    Args:
        food (DesignerObject): The food DesignerObject that is expected to be teleported
    Returns:
        Changes the x and y positions of the food
    '''
    food['x'] = 10 + randint(0, get_width()/20 - 1)*20
    food['y'] = 90 + randint(0, get_height()/20 - 5)*20

def create_boundary() -> DesignerObject:
    '''
    Creates the boundary DesignerObject
    
    Args:
        No arguments
    Returns:
        DesignerObject: Returns 4 lines that are grouped together as the boundary
    '''
    line1 = line('black', 0, 79, 800, 79, 1)
    line2 = line('black', 800, 0, 800, 601, 1)
    line3 = line('black', 0, 600, 800, 600, 2)
    line4 = line('black', 0, 0, 0, 600, 1)
    boundary = group(line1, line2, line3, line4)
    return boundary

def snake_direction(world: World, key: str):
    '''
    Changes the direction the snake is going
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
        key (str): A string representing the direction the snake will go towards
    Returns:
        Changes the value of world['direction']
    '''
    if key == 'up' or key == 'down' or key == 'left' or key =='right':
        if world['direction'] == 'up':
            if key != 'down':
                world['direction'] = key
        elif world['direction'] == 'down':
            if key != 'up':
                world['direction'] = key
        elif world['direction'] == 'left':
            if key != 'right':
                world['direction'] = key
        elif world['direction'] == 'right':
            if key != 'left':
                world['direction'] = key

def updates_per_movement(world: World):
    '''
    Changes the number of updates needed for the snake to move once. It essentially reduces
    the step rate.
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Moves the snake once every 2 updates.
        Records the x and y positions of the snake every 2 updates.
    '''
    if world['halve step rate'] == 0:
        world['halve step rate'] += 1
    elif world['halve step rate'] >= 1:
        move_snake(world)
        world['halve step rate'] = 0
        add_previous_x_and_y(world)

def move_snake(world: World):
    '''
    Moves the snake
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Increases the x or y position of the snake based on the snake speed
    '''
    if world['direction'] == 'left':
        world['snake']['x'] -= world['snake speed']
    elif world['direction'] == 'right':
        world['snake']['x'] += world['snake speed']
    elif world['direction'] == 'up':
        world['snake']['y'] -= world['snake speed']
    elif world['direction'] == 'down':
        world['snake']['y'] += world['snake speed']

def snake_eats_food(world: World) -> DesignerObject:
    '''
    Adds more snake segments and increments the score if the snake collides with food
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Adds snake segments and increments the score by 10
    '''
    if colliding(world['snake'], world['food']):
        teleport_food(world['food'])
        add_snake_segment(world)
        world['score'] += 10
    for segment in world['snake segments'][2:]:
        if colliding(world['food'], segment):
            teleport_food(world['food'])

def add_snake_segment(world: World) -> DesignerObject:
    '''
    Adds snake segments that follow the snake
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Adds snake segments
    '''
    for i in range(SEGMENTS_TO_ADD_AFTER_FOOD_IS_EATEN):
        world['snake segments'].append(create_snake())

def add_previous_x_and_y(world: World):
    '''
    Records the x and y positions of the snake in lists
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Puts x and y positions of the snake in lists
    '''
    world['previous x'].append(world['snake']['x'])
    world['previous y'].append(world['snake']['y'])

def move_snake_segments(world: World) -> DesignerObject:
    '''
    Moves the snake segments using the previous position lists
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Moves each snake segment to the previous positions of the snake
    '''
    if world['snake segments']:
        for i in range(len(world['snake segments'])):
            world['snake segments'][i]['x'] = world['previous x'][-i-2]
            world['snake segments'][i]['y'] = world['previous y'][-i-2]

def snake_collision(world: World):
    '''
    Checks whether the snake has collided with one of its segments
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Whether the snake has collided with one of its segments
    '''
    snake_collided = False
    for segment in world['snake segments'][1:]:
        if colliding(world['snake'], segment):
            snake_collided = True
    return snake_collided

def hit_boundary(world: World):
    '''
    Checks whether the snake has crossed the boundary
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Whether the snake has crossed the boundary
    '''
    hit_boundary = False
    if world['snake']['x'] >= 800 or world['snake']['x'] <= 0:
        hit_boundary = True
    elif world['snake']['y'] >= 600 or world['snake']['y'] <= 80:
        hit_boundary = True
    return hit_boundary

def update_counter(world: World):
    '''
    Updates the counter with the score
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Updates the counter if the score has changed
    '''
    world['counter']['text'] = 'Score: ' + str(world['score'])

def update_timer(world: World):
    '''
    Updates the counter with the time passed since the game started
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Updates the timer with the time that has passed
    '''
    world['timer'] += 1/30
    world['counter2']['text'] = 'Timer: ' + str(int(world['timer']))

def game_over(world: World):
    '''
    Shows the game over screen if the snake has collided with itself or passed the boundary
    
    Args:
        world (World): The world whom the value of the DesignerObjects will be accessed and/or changed
    Returns:
        Shows the game over screen
    '''
    world['counter']['text'] = 'GAME OVER!  |  Final Score: ' + str(world['score'])
    world['counter2']['text'] = 'Game lasted ' + str(int(world['timer'])) + ' seconds'
    world['snake']['x'] = world['previous x'][-2]
    world['snake']['y'] = world['previous y'][-2]


when('starting', create_world)
when('typing', snake_direction)
when('updating', updates_per_movement)
when('updating', snake_eats_food)
when('updating', move_snake_segments)
when('updating', update_counter)
when('updating', update_timer)
when(snake_collision, pause, game_over)
when(hit_boundary, pause, game_over)

start()