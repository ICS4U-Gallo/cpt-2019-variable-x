import arcade
import math
import os
import random
import json
from typing import List, Dict
from final_master import *

# Constants
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Cracking the Code!"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
COIN_COUNT = 20
COIN_SPEED = 4

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ANTIVIRUS = 0.2
SPRITE_SCALING_COIN = 0.1
ANTIVIRUS_COUNT = 10
ANTIVIRUS_SPEED = 6
SPRITE_SPEED = 0.5

MOVEMENT_SPEED = 10
GRAVITY = 10
PLAYER_JUMP_SPEED = 25

INSTRUCTIONS_PAGE_0 = 0
INSTRUCTIONS_PAGE_1 = 1
GAME_RUNNING = 2
GAME_OVER = 3
GAME_WIN = 4
# How many pixels to keep as a minimum margin between the player and the edge
# of the screen.
LEFT_VIEWPORT_MARGIN = 550
RIGHT_VIEWPORT_MARGIN = 500
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 200


def binary_search(lst: List[int], target: int) -> int:
    """ Creates an empty grid.
    Args:
        lst: the numbers to be sorted.

    Returns:
        the sorted numbers.
    """
    start = 0
    end = len(lst) - 1

    while start < end:
        mid = (start + end)//2

        if lst[mid] == target:
            return mid
        elif lst[mid] < target:
            end = mid - 1
        else:
            start = mid + 1
    return -1


def bubblesort(numbers: List[int]) -> List[int]:
    """ Creates an empty grid.
    Args:
        numbers: the numbers to be sorted.
    Returns:
        the sorted numbers.
    """
    n = len(numbers)

    for i in range(n):
        for j in range(n - i - 1):
            if numbers[j] > numbers[j + 1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
    return numbers


class AntiVirus(arcade.Sprite):
    """Class to create antivirus enemies"""

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

            self.change_x = math.cos(angle) * ANTIVIRUS_SPEED
            self.change_y = math.sin(angle) * ANTIVIRUS_SPEED


class Coin(arcade.Sprite):
    """Class to create the Windows icons"""

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

            self.change_x = (math.cos(-angle) * COIN_SPEED)
            self.change_y = (math.sin(-angle) * COIN_SPEED)


class MyGame(arcade.Window):
    """
    Main application class.
    """
    def __init__(self):
        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # 'Lists' that keep track of the sprites.
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

        # Background color
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Load instructions
        self.current_state = INSTRUCTIONS_PAGE_0
        self.instructions = []
        texture = arcade.load_texture("images/GameStart.png")
        self.instructions.append(texture)

        texture1 = arcade.load_texture("images/no.png")
        self.instructions.append(texture1)

        # Keep track of background
        self.background = None

    def setup(self):
        """Set up the game here. Call this function to restart the game"""

        self.total_time = 0.0

        self.background = arcade.load_texture("images/desktopwin.png")

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
        image_source = "images/trojan.png"
        self.player_sprite = arcade.Sprite(image_source, 0.1)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 500
        self.player_list.append(self.player_sprite)

        # Create the ground
        for x in range(-200, 2000, 64):
            wall = arcade.Sprite("images/vaporwaveblock.png", 0.4)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        for x2 in range(-200, 2000, 64):
            wall = arcade.Sprite("images/vaporwaveblock.png", 0.4)
            wall.center_x = x2
            wall.center_y = 1300
            self.wall_list.append(wall)

        for coordinate in range(0, 1200, 200):
            # Create left wall
            wall = arcade.Sprite("images/vaporwaveblock.png", 0.4)
            wall.center_x = -200
            wall.center_y = coordinate
            self.wall_list.append(wall)

        for coordinate2 in range(0, 1200, 200):
            # Create right wall
            wall = arcade.Sprite("images/vaporwaveblock.png", 0.4)
            wall.center_x = 1500
            wall.center_y = coordinate2
            self.wall_list.append(wall)

        for x in range(COIN_COUNT):
            coin = Coin("images/windowsxp.png", SPRITE_SCALING_COIN)

            coin.center_x = random.randrange(SCREEN_WIDTH + 1000)
            coin.center_y = random.randrange(200, SCREEN_HEIGHT + 500)

            self.coin_list.append(coin)

        for i in range(ANTIVIRUS_COUNT):
            antivirus = AntiVirus("images/macafee.png",
                                  SPRITE_SCALING_ANTIVIRUS)

            # Position the antivirus
            antivirus.center_x = random.randrange(SCREEN_WIDTH)
            antivirus.center_y = random.randrange(600, 900)

            self.antivirus_list.append(antivirus)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
                                                            self.player_sprite,
                                                            self.wall_list,
                                                            GRAVITY)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(550 + self.view_left, 410 +
                                      self.view_bottom,
                                      page_texture.width // 1.7,
                                      page_texture.height // 1.7, page_texture,
                                      0)

    def draw_game(self):
        """
        Draw all the sprites, along with the score.
        """
        # Draw all the sprites.
        self.player_list.draw()
        self.coin_list.draw()

        health_text = f"trojan_integrity: {self.health + 1}"
        arcade.draw_text(health_text, 10 + self.view_left, 650 +
                         self.view_bottom, arcade.color.WHITE, 32)

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left + 600, 650 +
                         self.view_bottom, arcade.color.WHITE, 32)

        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, self.view_left, self.view_bottom,
                         arcade.color.WHITE, 32)

    def store_score(self, score: int) -> None:
        """stores the time when game is over
        Args:
            score(int): the player's time
        """
        with open("hack_times.json", "r") as f:
            data = json.load(f)
        data[f"user {len(data) + 1}"] = score
        with open("hack_times.json", "w") as f:
            json.dump(data, f)

        self._stored_score = True

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """

        output = "Hacking Failed, Trojan Compromised"
        arcade.draw_text(output, self.view_left, self.view_bottom + 300,
                         arcade.color.RED, 44)

        output = "Click to restart hacking"
        arcade.draw_text(output, self.view_left + 60, self.view_bottom + 200,
                         arcade.color.WHITE, 24)

    def draw_game_win(self):
        """
        Draw "You win" across the screen.
        """
        output = "Door lock successfully hacked."
        arcade.draw_text(output, self.view_left, self.view_bottom + 600,
                         arcade.color.GREEN, 54)

        output_highscores = (f"Hacked in {round(self.total_time, 2)} seconds. "
                             "Click to escape.")

        arcade.draw_text(str(output_highscores), self.view_left,
                         self.view_bottom, arcade.color.GREEN, 44)

        arcade.draw_text("Fastest Hacks:", self.view_left,
                         self.view_bottom + 400, arcade.color.GREEN, 34)

        height_decrease = 0
        sorted_list = []
        with open("hack_times.json", "r") as f:
            data = json.load(f)

        for values in data.values():
            sorted_list.append(values)
            sorted_list2 = bubblesort(sorted_list)

        for i in range(0, 5):
            arcade.draw_text(f"{i + 1}: {sorted_list2[i]} seconds \n",
                             self.view_left + 60,
                             self.view_bottom + 300 - height_decrease,
                             arcade.color.WHITE, 24)
            height_decrease += 40

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        arcade.start_render()

        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2 + 200,
                                      SCREEN_HEIGHT // 2 + 300,
                                      self.background.width * 1.5,
                                      self.background.height * 1.5,
                                      self.background)

        n = len(self.antivirus_list)

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()
        self.antivirus_list.draw()

        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

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
            # Game start screen.
            self.setup()
            self.current_state = INSTRUCTIONS_PAGE_1

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            # Next page of instructions.
            self.current_state = GAME_RUNNING

        elif self.current_state == GAME_OVER:
            # Restart the game.
            self.setup()
            self.current_state = GAME_RUNNING

        elif self.current_state == GAME_WIN:
            self.store_score(round(self.total_time, 2))
            arcade.close_window()
            game = Game(500, 500)
            game.setup()
            arcade.run()

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
            for coin in self.coin_list:
                coin.follow_sprite(self.player_sprite)

                coin_hit_list = arcade.check_for_collision_with_list(
                                                            self.player_sprite,
                                                            self.coin_list)

                for coin in coin_hit_list:
                    coin.remove_from_sprite_lists()
                    # Play a sound
                    arcade.play_sound(self.collect_coin_sound)
                    # Add one to the score
                    self.score += 1

            for coin in self.coin_list:
                coin.center_x += coin.change_x
                walls_hit = arcade.check_for_collision_with_list(
                                                                coin,
                                                                self.wall_list)
                for wall in walls_hit:
                    if coin.change_x > 0:
                        coin.right = wall.left
                    elif coin.change_x < 0:
                        coin.left = wall.right
                if len(walls_hit) > 0:
                    coin.change_x *= -1

                coin.center_y += coin.change_y
                walls_hit = arcade.check_for_collision_with_list(
                                                                coin,
                                                                self.wall_list)
                for wall in walls_hit:
                    if coin.change_y > 0:
                        coin.top = wall.bottom
                    elif coin.change_y < 0:
                        coin.bottom = wall.top
                if len(walls_hit) > 0:
                    coin.change_y *= -1

            for antivirus in self.antivirus_list:
                antivirus.follow_sprite(self.player_sprite)

                hit_list = arcade.check_for_collision_with_list(
                                                        self.player_sprite,
                                                        self.antivirus_list)

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
                walls_hit = arcade.check_for_collision_with_list(
                                                                antivirus,
                                                                self.wall_list)
                for wall in walls_hit:
                    if antivirus.change_x > 0:
                        antivirus.right = wall.left
                    elif antivirus.change_x < 0:
                        antivirus.left = wall.right
                if len(walls_hit) > 0:
                    antivirus.change_x *= -1

                antivirus.center_y += antivirus.change_y
                walls_hit = arcade.check_for_collision_with_list(
                                                                antivirus,
                                                                self.wall_list)
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
            right_boundary = (
                self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN)
            if self.player_sprite.right > right_boundary:
                self.view_left += self.player_sprite.right - right_boundary
                changed = True

            top_boundary = (
                self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN)
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

            arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,
                                self.view_bottom, SCREEN_HEIGHT +
                                self.view_bottom)


def main():
    """Main method"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
