 
 
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
import json

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Platformer Game"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
COIN_COUNT = 100
COIN_SPEED = 5

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ANTIVIRUS = 1
SPRITE_SCALING_COIN = 0.1
ANTIVIRUS_COUNT = 20
ANTIVIRUS_SPEED = 5
SPRITE_SPEED = 0.5

MOVEMENT_SPEED = 10
GRAVITY = 10
PLAYER_JUMP_SPEED = 25

INSTRUCTIONS_PAGE_0 = 0
GAME_RUNNING = 1
GAME_OVER = 2
GAME_WIN = 3

# How many pixels to keep as a minimum margin between the player and the edge 
# of the screen. 
LEFT_VIEWPORT_MARGIN = 500
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 200

sorted_list = []

class ScoreBoard():
    sorted_list = []
    user = int(input("Enter a value: "))       

    def bubblesort(numbers):
        n = len(numbers)

        for i in range(n):
            for j in range(n - i - 1):
                if numbers[j] < numbers[j + 1]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

        return numbers

    with open("data.json", "r") as f:
        data = json.load(f)

    data[f"user {len(data) + 1}"] = user
        
    def score_board():
        with open("data.json", "r") as f:
            data = json.load(f)

        for values in data.values():
            sorted_list.append(values)
            bubblesort(sorted_list)
            

        for i in range(len(sorted_list)):
            print(f" {i + 1}. {sorted_list[i]}")
                
    result = score_board()
    print(result)

class AntiVirus(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(200) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Calculate how to get the bullet to the destination
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = math.cos(angle) * ANTIVIRUS_SPEED
            self.change_y = math.sin(angle) * ANTIVIRUS_SPEED


class Coin(arcade.Sprite):

    def follow_sprite(self, player_sprite):
        
        self.center_x += self.change_x
        self.center_y += self.change_y

        if random.randrange(100) == 0:
            start_x = self.center_x
            start_y = self.center_y

            # Get the destination location for the bullet
            dest_x = player_sprite.center_x
            dest_y = player_sprite.center_y

            # Calculate how to get the bullet to the destination
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            self.change_x = (math.cos(angle) * COIN_SPEED)
            self.change_y = (math.sin(angle) * COIN_SPEED)
        
        
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
        self.health = 3

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("SFX/buttonclick.wav")
        self.jump_sound = arcade.load_sound("SFX/EEnE Whoosh 8.wav")

        arcade.set_background_color(arcade.csscolor.BLACK)
        
        self.current_state = INSTRUCTIONS_PAGE_0
        self.instructions = []
        texture = arcade.load_texture("images/instructions.png")
        self.instructions.append(texture)

        self.background = None

    
    def setup(self):
        """Set up the game here. Call this function to restart the game"""

        self.total_time = 0.0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.set_mouse_visible(False)

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Used to keep track of the score
        self.score = 0
        self.health = 2

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.antivirus_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        image_source = "images/hacker.png" 
        self.player_sprite = arcade.Sprite(image_source, 0.1)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(0, 10000, 64):
            wall = arcade.Sprite("images/vaporwaveblock.png", 0.4)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list
        coordinate_list = [[512, 96]]
        
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite("images/vaporwaveblock.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)
        
        for x in range(COIN_COUNT):
            coin = AntiVirus("images/windowsxp.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH + 1000)
            coin.center_y = random.randrange(SCREEN_HEIGHT + 1000)

            self.coin_list.append(coin)

        for i in range(ANTIVIRUS_COUNT):
            antivirus = AntiVirus("images/zombie.png", SPRITE_SCALING_ANTIVIRUS)

            # Position the antivirus
            antivirus.center_x = random.randrange(SCREEN_WIDTH)
            antivirus.center_y = random.randrange(600, 900)

            self.antivirus_list.append(antivirus)


        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)


    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(550 + self.view_left, 350 + self.view_bottom,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        
    def draw_game(self):
        """
        Draw all the sprites, along with the score.
        """
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()

        highscores_text = ScoreBoard()
        arcade.draw_text(highscores_text, self.view_left, self.view_bottom, arcade.color.WHITE, 50)

        health_text = f"trojan_integrity: {self.health + 1}"
        arcade.draw_text(health_text, 10 + self.view_left, 600 + self.view_bottom, arcade.color.WHITE, 32)
        
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left + 600, 600 + self.view_bottom, arcade.color.WHITE, 32)

        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output,self.view_left, self.view_bottom, arcade.color.WHITE, 32)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Hacking Failed, Reload Trojan"
        arcade.draw_text(output, self.view_left, self.view_bottom + 300, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, self.view_left + 60, self.view_bottom + 200, arcade.color.WHITE, 24)

    def draw_game_win(self):
        """
        Draw "You win" across the screen.
        """
        output = "Mainframe successfully hacked."
        arcade.draw_text(output, self.view_left, self.view_bottom + 300, arcade.color.WHITE, 54)
        
        output_highscores = self.total_time
        
        arcade.draw_text(str(output_highscores), self.view_left, self.view_bottom, arcade.color.WHITE, 54)

    

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        n = len(self.antivirus_list)

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.antivirus_list.draw()


        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)
        
        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        elif self.current_state == GAME_WIN:
            self.draw_game_win()
            
        else:
            self.draw_game_over()



    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        # Change states as needed.
        if self.current_state == INSTRUCTIONS_PAGE_0:
            # Next page of instructions.
            self.setup()
            self.current_state = GAME_RUNNING  

        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING 

        elif self.current_state == GAME_WIN:
            self.setup()
            self.current_state = INSTRUCTIONS_PAGE_0
            
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

            

    def on_update(self, delta_time):
        """ Movement and game logic """
        
        if self.current_state == GAME_RUNNING:
            # Move the player with the physics engine
            self.physics_engine.update()

            self.total_time += delta_time

            # Calculate speed based on the keys pressed
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

            if self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
            elif self.down_pressed and not self.up_pressed:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = MOVEMENT_SPEED

            # Call update to move the sprite
            # If using a physics engine, call update on it instead of the sprite
            # list.
            for coin in self.coin_list:
                coin.follow_sprite(self.player_sprite)
                
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
                    self.health -= 1
            
            if self.health <= -1:
                self.current_state = GAME_OVER
                self.set_mouse_visible(True)

            if self.score >= 10:
                self.current_state = GAME_WIN
                self.set_mouse_visible(True)

            for antivirus in self.antivirus_list:

                antivirus.center_x += antivirus.change_x
                walls_hit = arcade.check_for_collision_with_list(antivirus, self.wall_list)
                for wall in walls_hit:
                    if antivirus.change_x > 0:
                        antivirus.right = wall.left
                    elif antivirus.change_x < 0:
                        antivirus.left = wall.right
                if len(walls_hit) > 0:
                    antivirus.change_x *= -1

                antivirus.center_y += antivirus.change_y
                walls_hit = arcade.check_for_collision_with_list(antivirus, self.wall_list)
                for wall in walls_hit:
                    if antivirus.change_y > 0:
                        antivirus.top = wall.bottom
                    elif antivirus.change_y < 0:
                        antivirus.bottom = wall.top
                if len(walls_hit) > 0:
                    antivirus.change_y *= -1

        
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
    
