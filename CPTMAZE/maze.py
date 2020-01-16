import random
import arcade
import timeit

sprite_scaling = 0.25
sprite_size = 128 * sprite_scaling

screen_width = 670
screen_height = 670

title = "Maze"

speed = 10

tile_empty = 0
tile_brick = 1

sorted_list = []

# Maze must have an ODD number of rows and columns.
# Walls go on EVEN rows/columns.
# Openings go on ODD rows/columns
maze_height = 21
maze_width = 21


def create_empty_grid(width, height, default_value=tile_empty):
    """ Create an empty grid. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            grid[row].append(default_value)
    return grid


def create_outside_walls(maze):
    """ Create outside border walls."""

    # Create left and right walls
    for row in range(len(maze)):
        maze[row][0] = tile_brick
        maze[row][len(maze[row])-1] = tile_brick

    # Create top and bottom walls
    for column in range(1, len(maze[0]) - 1):
        maze[0][column] = tile_brick
        maze[len(maze) - 1][column] = tile_brick


def make_maze_recursive_call(maze, top, bottom, left, right):
    """
    Recursive function to divide up the maze in four sections
    and create three gaps.
    Walls can only go on even numbered rows/columns.
    Gaps can only go on odd numbered rows/columns.
    Maze must have an odd number of rows and columns.
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


def make_maze_recursion(maze_width, maze_height):
    """ Make the maze by recursively splitting it into four rooms. """
    maze = create_empty_grid(maze_width, maze_height)
    # Fill in the outside walls
    create_outside_walls(maze)

    # Start the recursive process
    make_maze_recursive_call(maze, maze_height - 1, 0, 0, maze_width - 1)
    return maze


class HighscoreInput(arcade.Window):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        highscore = MyGame().SCORE
        arcade.start_render()
        arcade.draw_text(f"You Have Escaped The Building: {highscore}", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=12, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        highscore = MyGame().SCORE
        with open("data.json", "r") as f:
            data = json.load(f)
    
        data[f"highscore {len(data) + 1}"] = highscore

        with open("data.json", 'w') as f:
            json.dump(data, f)
        highscore_view = HighscoreView()
        self.window.show_view(highscore_view)


class HighscoreView(arcade.Window):
    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        sorted_list = []
        arcade.start_render()
        with open("data.json", "r") as f:
            data = json.load(f)

        for values in data.values():
            sorted_list.append(values)
            bubblesort(sorted_list)
        arcade.draw_text(f"Highscores: \n {sorted_list}", WIDTH/2, HEIGHT/2,
                         arcade.color.BLACK, font_size=18, anchor_x="center")
        arcade.draw_text("Click to continue", WIDTH/2, HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.staircase_list = None

        # Player info
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        self.counter = 0

        self.time = 0

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.staircase_list = arcade.SpriteList()

        maze = make_maze_recursion(maze_width, maze_height)

        # Create sprites based on 2D grid
        # if not merge_sprites:
        # Each grid location is a sprite.
        for row in range(maze_height):
            for column in range(maze_width):
                if maze[row][column] == 1:
                    wall = arcade.Sprite("CPTMAZE/images/brick.png", sprite_scaling)
                    wall.center_x = column * sprite_size + sprite_size / 2
                    wall.center_y = row * sprite_size + sprite_size / 2
                    self.wall_list.append(wall)

        # Set up the player
        self.player_sprite = arcade.Sprite("CPTMAZE/images/person.png", sprite_scaling)
        self.player_list.append(self.player_sprite)

        self.staircase_sprite = arcade.Sprite("CPTMAZE/images/staircase.jpg", sprite_scaling)
        self.staircase_list.append(self.staircase_sprite)

        # Randomly place the player. If in a wall, repeat until we aren't.
        placed = False
        while not placed:

            # Randomly position
            self.player_sprite.center_x = 50
            self.player_sprite.center_y = 50

            #  In a wall?
            walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall
                placed = True

            self.staircase_sprite.center_x = 625
            self.staircase_sprite.center_y = 625

            # In a wall?
            walls_hit = arcade.check_for_collision_with_list(self.staircase_sprite, self.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall
                placed = True
        
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the background color
        arcade.set_background_color(arcade.color.BONE)

        # Set the viewport boundaries
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Start timing how long this takes

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.staircase_list.draw()

        output = f"Time: {self.time:.3f} seconds"
        arcade.draw_text(output,
                         self.view_left + 20,
                         screen_height - 20 + self.view_bottom,
                         arcade.color.WHITE, 16)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = speed
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites
        self.physics_engine.update()

        for player in self.player_list:
            hit_list = arcade.check_for_collision_with_list(player, self.staircase_list)

        for player in hit_list:
            self.setup()

            if len(hit_list) >= 0:
                self.counter += 1
                print(self.counter)

            if self.counter == 3:
                highscoreinput = HighscoreInput(screen_width, screen_height, title) 
                self.window.show_view(highscoreinput)
                
        self.time += delta_time


def main():
    # Main method
    window = MyGame(screen_width, screen_height, title)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

