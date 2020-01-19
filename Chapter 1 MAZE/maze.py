import random
import arcade
import timeit
import json
from typing import List
from arcade import *

sprite_scaling = 0.25
sprite_size = 128 * sprite_scaling

screen_width = 670
screen_height = 670

title = "Maze"

speed = 4

tile_empty = 0
tile_brick = 1

sorted_list = []

maze_height = 21
maze_width = 21


def create_empty_grid(width: int, height: int, value=tile_empty) -> List:
    """ Creates an empty grid.
    Args:
        width: the width of the grid
        height: the height of the grid
        value: empty tiles
    Returns:
        the empty grid
    """

    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            grid[row].append(value)
    return grid


def create_outside_walls(maze: List[int]) -> List[int]:
    """ Creates outside border walls.
    Args:
        maze: the empty grid
    Returns:
        maze with border walls
    """

    # Create left and right walls
    for row in range(len(maze)):
        maze[row][0] = tile_brick
        maze[row][len(maze[row]) - 1] = tile_brick

    # Create top and bottom walls
    for column in range(1, len(maze[0]) - 1):
        maze[0][column] = tile_brick
        maze[len(maze) - 1][column] = tile_brick


def make_maze_recursive_call(maze: List[int], top: int, bottom: int, left: int, right: int) -> List[int]:
    """
    Recursive function to divide up the maze in four sections
    and create three gaps.
    Walls go on even numbered rows/columns.
    Gaps go on odd numbered rows/columns.
    Maze must have an odd number of rows and columns.
    Args:
        maze: the maze with border walls
        top: maze height
        bottom: maze height
        left: maze width
        right: maze width
    Returns:
        maze with gaps and walls
    """

    # Figure out where to divide horizontally
    start_range = bottom + 2
    end_range = top - 1
    y = random.randrange(start_range, end_range, 2)

    # Do the division
    for column in range(left + 1, right):
        maze[y][column] = tile_brick

    # Figure out where to divide vertically
    start_range = left + 2
    end_range = right - 1
    x = random.randrange(start_range, end_range, 2)

    # Do the division
    for row in range(bottom + 1, top):
        maze[row][x] = tile_brick

    # Make a gap on 3 of the 4 walls.
    # Figure out which wall does NOT get a gap.
    wall = random.randrange(4)
    if wall != 0:
        gap = random.randrange(left + 1, x, 2)
        maze[y][gap] = tile_empty

    if wall != 1:
        gap = random.randrange(x + 1, right, 2)
        maze[y][gap] = tile_empty

    if wall != 2:
        gap = random.randrange(bottom + 1, y, 2)
        maze[gap][x] = tile_empty

    if wall != 3:
        gap = random.randrange(y + 1, top, 2)
        maze[gap][x] = tile_empty

    # If there's enough space, to a recursive call.
    if top > y + 3 and x > left + 3:
        make_maze_recursive_call(maze, top, y, left, x)

    if top > y + 3 and x + 3 < right:
        make_maze_recursive_call(maze, top, y, x, right)

    if bottom + 3 < y and x + 3 < right:
        make_maze_recursive_call(maze, y, bottom, x, right)

    if bottom + 3 < y and x > left + 3:
        make_maze_recursive_call(maze, y, bottom, left, x)


def make_maze_recursion(maze_width: int, maze_height: int) -> List[int]:
    """ Make the maze
    Args:
        maze_width: maze width
        maze_height: maze height
    Returns:
        the maze after processed through the functions
    """

    maze = create_empty_grid(maze_width, maze_height)
    # Fill in the outside walls
    create_outside_walls(maze)

    # Start the recursive process
    make_maze_recursive_call(maze, maze_height - 1, 0, 0, maze_width - 1)
    return maze


def merge_sort(numbers: List[int]) -> List[int]:
    """Sorts the items in a list
    Args:
        numbers: list of integers
    Returns:
        the list of integers from smallest to largest value
    """
    # merge sort
    # Base case
    if len(numbers) == 1:
        return numbers

    midpoint = len(numbers) // 2

    # Two recursive steps
    # Mergesort left
    left_side = merge_sort(numbers[:midpoint])
    # Mergesort right
    right_side = merge_sort(numbers[midpoint:])
    # Merge the two together
    sorted_list = []

    # Loop through both lists with two markers
    left_marker = 0
    right_marker = 0
    while left_marker < len(left_side) and right_marker < len(right_side):
        # If left value less than right value, add right value to sorted
        # increase left marker
        if left_side[left_marker] < right_side[right_marker]:
            sorted_list.append(left_side[left_marker])
            left_marker += 1
        # If right value less than left value, add left value to sorted
        # increase right marker
        else:
            sorted_list.append(right_side[right_marker])
            right_marker += 1

    # Create a while loop to gather the rest of the values from either list
    while right_marker < len(right_side):
        sorted_list.append(right_side[right_marker])
        right_marker += 1

    while left_marker < len(left_side):
        sorted_list.append(left_side[left_marker])
        left_marker += 1

    # Return the sorted list
    return sorted_list


class MenuScreen(arcade.View):
    """Class to display menu screen"""

    def on_show(self):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    def on_draw(self):
        # Shows the menu screen and controls
        arcade.start_render()
        arcade.draw_text("LOCKDOWN", screen_width / 2, screen_height - 100,
                         arcade.color.TEAL, font_size=50, anchor_x="center")
        arcade.draw_text("You wake up in your office and you realize there is a zombie apocalypse.",
                         screen_width / 2, screen_height - 200,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("Get out of the building to go to the nearest safe zone.",
                         screen_width / 2, screen_height - 250,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("Controls:", screen_width / 2, screen_height - 300,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("W - Up", screen_width / 2, screen_height / 2,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("S - Down", screen_width / 2, screen_height / 2 - 50,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("A - Left", screen_width / 2, screen_height / 2 - 100,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("D - Right", screen_width / 2,
                         screen_height / 2 - 150,
                         arcade.color.TEAL, font_size=12, anchor_x="center")
        arcade.draw_text("Click to start game", screen_width / 2,
                         screen_height / 2 - 200,
                         arcade.color.TEAL, font_size=12, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # After user clicks, transition to the maze
        maze = Maze()
        maze.setup()
        self.window.show_view(maze)


class Maze(arcade.View):
    """Class to display the maze"""

    def __init__(self):
        super().__init__()

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.staircase_list = arcade.SpriteList()

        # Creates player and staircase
        self.player_sprite = arcade.Sprite("images/persone.png",
                                           sprite_scaling)
        self.player_list.append(self.player_sprite)
        self.staircase_sprite = arcade.Sprite("images/staircase.jpg",
                                              sprite_scaling)
        self.staircase_list.append(self.staircase_sprite)

        # Counter to stop the game
        self.counter = 0

        # Time
        self.time = 0

        # movement list
        self.movement_queue = []

    def on_show(self):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    def setup(self):
        """ Set up the game"""

        self.wall_list = arcade.SpriteList()

        # Physics engine
        self.physics_engine = PhysicsEngineSimple(self.player_sprite,
                                                  self.wall_list)

        maze = make_maze_recursion(maze_width, maze_height)

        # Create sprites based on 2D grid
        # Each grid location is a sprite.
        # searching
        for row in range(maze_height):
            for column in range(maze_width):
                if maze[row][column] == 1:
                    wall = arcade.Sprite("images/brick.png", sprite_scaling)
                    wall.center_x = column * sprite_size + sprite_size / 2
                    wall.center_y = row * sprite_size + sprite_size / 2
                    self.wall_list.append(wall)

        # Place the player. If in a wall, repeat until it isn't.
        placed = False
        while not placed:

            # Positions player
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 50

            # Checks if in a wall
            walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall
                placed = True

            # Positions staircase
            self.staircase_sprite.center_x = 625
            self.staircase_sprite.center_y = 625

            # Checks if in a wall
            walls_hit = arcade.check_for_collision_with_list(self.staircase_sprite, self.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall
                placed = True

    def on_draw(self):
        """Render the screen."""

        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.staircase_list.draw()

        # Displays the time
        output = f"Time: {self.time:.3f} seconds"
        arcade.draw_text(output,
                         20,
                         screen_height - 20,
                         arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. Stores in a queue"""
        if key == arcade.key.W:
            self.movement_queue.insert(0, 'u')
        elif key == arcade.key.S:
            self.movement_queue.insert(0, 'd')
        elif key == arcade.key.A:
            self.movement_queue.insert(0, 'l')
        elif key == arcade.key.D:
            self.movement_queue.insert(0, 'r')

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. Stores in a queue"""
        if key == arcade.key.W:
            self.movement_queue.remove('u')
        elif key == arcade.key.S:
            self.movement_queue.remove('d')
        elif key == arcade.key.A:
            self.movement_queue.remove('l')
        elif key == arcade.key.D:
            self.movement_queue.remove('r')

    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update on all sprites
        self.wall_list.update()
        self.player_list.update()
        self.staircase_list.update()
        self.physics_engine.update()

        # Queue for movement. Key release stops movement
        if len(self.movement_queue) > 0:
            if self.movement_queue[0] == 'u':
                self.player_sprite.change_y = speed
                self.player_sprite.change_x = 0
            elif self.movement_queue[0] == 'd':
                self.player_sprite.change_y = -speed
                self.player_sprite.change_x = 0
            elif self.movement_queue[0] == 'l':
                self.player_sprite.change_x = -speed
                self.player_sprite.change_y = 0
            elif self.movement_queue[0] == 'r':
                self.player_sprite.change_x = speed
                self.player_sprite.change_y = 0
        else:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0

        # Start adding the time
        self.time += delta_time

        # Check to see if player touches the staircase
        for player in self.player_list:
            hit_list = arcade.check_for_collision_with_list(player, self.staircase_list)

        # If player touches the staircase, maze randomly generates again
        for player in hit_list:
            self.setup()
            self.counter += 1

            # If maze generates 3 times, game will transition to results
            if self.counter == 1:
                global time
                time = self.time
                escaped_building = EscapedBuilding()
                self.window.show_view(escaped_building)


class EscapedBuilding(arcade.View):
    """Shows player's time after completing the maze"""

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        # Time used to complete the maze rounded to two decimals
        maze_time = round(time, 2)
        arcade.draw_text(f"You Have Escaped The Building In {maze_time} Seconds", screen_width / 2, screen_height / 2,
                         arcade.color.TEAL, font_size=20, anchor_x="center")

    def on_show(self):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # Time used to complete the maze rounded to two decimals
        maze_time = round(time, 2)
        # Add the time to highscore list
        with open("data.json", "r") as f:
            data = json.load(f)

        data[f"time {len(data) + 1}"] = maze_time

        with open("data.json", 'w') as f:
            json.dump(data, f)

        # Transition to highscore view
        highscores = Highscores()
        self.window.show_view(highscores)


class Highscores(arcade.View):
    """Shows a list of scores"""

    @classmethod
    def on_show(cls):
        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

    @classmethod
    def on_draw(cls):
        """Render the screen."""
        arcade.start_render()
        # Time used to complete the maze rounded to two decimals
        maze_time = round(time, 2)
        height_decrease = 120
        sorted_list = []
        with open("data.json", "r") as f:
            data = json.load(f)

        # Displaying the scores from shortest to longest times
        for values in data.values():
            sorted_list.append(values)
            sorted_list2 = merge_sort(sorted_list)
        arcade.draw_text(f"Shortest Times: \n", screen_width / 2,
                         screen_height - 200,
                         arcade.color.TEAL, font_size=18, anchor_x="center")

        # Only displays 5 scores
        for i in reversed(range(0, 5)):
            arcade.draw_text(f"{i + 1}: {sorted_list2[i]} \n",
                             screen_width / 2,
                             screen_height - 200 - height_decrease,
                             arcade.color.TEAL, font_size=18,
                             anchor_x="center")
            height_decrease -= 20

        # Display text
        arcade.draw_text(f"Your Time: {maze_time}", screen_width / 2,
                         screen_height / 2 - 100,
                         arcade.color.TEAL, font_size=18, anchor_x="center")
        arcade.draw_text("Click to continue", screen_width / 2,
                         screen_height / 2 - 250,
                         arcade.color.TEAL, font_size=20, anchor_x="center")


class PhysicsEngineSimple:
    """Move everything and take care of collisions."""

    def __init__(self, player_sprite, walls):
        """Create a simple physics engine.

        Args:
            player_sprite: The moving sprite
            walls: The sprites it can't move through
        """
        self.player_sprite = player_sprite
        self.walls = walls

    def update(self):
        """Move everything and resolve collisions.

        Returns:
            Sprite list with all sprites contacted.
            Empty list if no sprites.
        """

        # Move in the x direction
        self.player_sprite.center_x += self.player_sprite.change_x

        # Check for wall hit
        hit_list_x = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # Hit a wall, move so the edges are at the same point
        if len(hit_list_x) > 0:
            if self.player_sprite.change_x > 0:
                for item in hit_list_x:
                    self.player_sprite.right = min(item.left,
                                                   self.player_sprite.right)
            elif self.player_sprite.change_x < 0:
                for item in hit_list_x:
                    self.player_sprite.left = max(item.right,
                                                  self.player_sprite.left)

        # Move in the y direction
        self.player_sprite.center_y += self.player_sprite.change_y

        # Check for wall hit
        hit_list_y = \
            check_for_collision_with_list(self.player_sprite,
                                          self.walls)

        # Hit a wall, move so the edges are at the same point
        if len(hit_list_y) > 0:
            if self.player_sprite.change_y > 0:
                for item in hit_list_y:
                    self.player_sprite.top = min(item.bottom,
                                                 self.player_sprite.top)
            else:
                for item in hit_list_y:
                    self.player_sprite.bottom = max(item.top,
                                                    self.player_sprite.bottom)

        # Return list of encountered sprites
        complete_hit_list = hit_list_x
        for sprite in hit_list_y:
            complete_hit_list.append(sprite)
        return complete_hit_list


def main():
    # Main method
    window = arcade.Window(screen_width, screen_height, title)
    # Start with menu screen
    menu_screen = MenuScreen()
    window.show_view(menu_screen)
    arcade.run()

if __name__ == "__main__":
    main()
