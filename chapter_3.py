"""
Hack&/

To-do:
sort the highscores using bubble sort  
recursively spawn enemies based on level
GUI
"""

import arcade
import math
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer Game"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ANTIVIRUS = 0.2
ANTIVIRUS_COUNT = 5
ANTIVIRUS_SPEED = 0.5
SPRITE_SPEED = 0.5

PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 2
PLAYER_JUMP_SPEED = 25

# How many pixels to keep as a minimum margin between the player and the edge 
# of the screen. 
LEFT_VIEWPORT_MARGIN = 400
RIGHT_VIEWPORT_MARGIN = 400
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class AntiVirus(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x

            # Calculate how to get the bullet to the destination
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * COIN_SPEED
            self.change_y = math.sin(angle) * COIN_SPEED
        
        
class MyGame(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.view_bottom = 0
        self.view_left = 0 

        # Keep track of score
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("SFX/buttonclick.wav")
        self.jump_sound = arcade.load_sound("SFX/EEnE Whoosh 8.wav")

        arcade.set_background_color(arcade.csscolor.BLACK)
        
        self.background = None


    def setup(self):
        """Set up the game here. Call this function to restart the game"""

        self.background = arcade.load_texture("images/matrix.jpeg")
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Used to keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.antivirus_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/boxCrate_double.png" 
        self.player_sprite = arcade.Sprite(image_source, 0.2)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("images/boxCrate_double.png")
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list
        coordinate_list = [[512, 96]]
        
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        for x in range(128, 1250, 256):
            coin = arcade.Sprite("images/boxCrate_double.png", 0.2)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        for i in range(ANTIVIRUS_COUNT):
            antivirus = AntiVirus("images/coin_01.png", SPRITE_SCALING_ANTIVIRUS)

            # Position the antivirus
            antivirus.center_x = random.randrange(SCREEN_WIDTH)
            antivirus.center_y = random.randrange(SCREEN_HEIGHT)

            self.antivirus_list.append(antivirus)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()
       
        
        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.antivirus_list.draw()


        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 600 + self.view_bottom, arcade.color.WHITE, 32)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player with the physics engine
        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the score
            self.score += 1

        for antivirus in self.antivirus_list:
            antivirus.follow_sprite(self.player_sprite)

            hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.antivirus_list)

            for antivirus in hit_list:
                antivirus.kill()
                self.score -= 1


        # ---Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        
        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.bottom > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= self.player_sprite.bottom + bottom_boundary
            changed = True
         
        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

        arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__== "__main__":
    main()





