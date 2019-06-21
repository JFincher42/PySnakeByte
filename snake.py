""" Snake

A Python3 implementation of Snake Byte

Uses arcade to allow the user to control a snake
The snake moves at a set pace
Apples appear on the screen at random locations
The snake eats an apple, and gets longer
If the snake hits a wall, or it's own body, the game is over

"""

# IMPORTS
import random
import arcade

# CONSTANTS
SNAKEBODYCOLOR = arcade.color.APPLE_GREEN  # What color to draw the snake
SNAKEHEADCOLOR = arcade.color.CANARY_YELLOW  # Color of the snake's head
BORDERCOLOR = arcade.color.ALMOND  # Color of the screen border
APPLECOLOR = arcade.color.CANDY_APPLE_RED  # What color to draw the apple
BGCOLOR = arcade.color.SMOKY_BLACK  # What color is the background

SIZE = 40  # How big is each block?
APPLEPOINTS = 10  # How many points per appls?

SCREENX = 50  # How wide is the screen
SCREENY = 40  # How tall is the screen
TITLE = "PySnake"  # What is the window title

INITAPPLES = 3  # How many apples to start with
APPLETIMER = 10  # How long before a new set of apples show up
SNAKEFADE = -3  # How many segments to fade out

# Directions
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# WHich direction is next if you turn?
CLOCKWISE = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
COUNTERCLOCKWISE = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}

# The Snake_Game class


class Snake_Game(arcade.Window):
    """Snake_Game class

    Contains all the logic to run a snake game

    """

    def __init__(self, width, height, title, background_color):
        super().__init__(width, height, title)
        arcade.set_background_color(background_color)

    def setup(self):
        """Setup the game for initial playback.
        """
        # Game Variables
        self.expand_snake = 0  # How many segments to add to the snake
        self.running = True  # Are we still playing? False if we need to exit
        self.paused = False  # Are we paused?

        # Setup the initial list of apples
        self.apple_list = [
            self.get_random_point(SCREENX - 1, SCREENY - 1)
            for i in range(INITAPPLES)
        ]

        # Setup the initial snake position and direction
        self.snake_list = [
            (28, 14),
            (27, 14),
            (26, 14),
            (25, 14),
            (25, 13),
            (25, 12),
            (25, 11),
            (25, 10),
        ]
        self.snake_direction = UP  # Current snake direction
        self.snake_speed = 0.500  # Current snake speed
        self.frame_time = 0.0  # How much time
        self.score = 0  # Current game score

        self.shape_list = arcade.ShapeElementList()  # What gets drawn

    def get_random_point(self, x, y):
        """Returns a random points between 2 and the given x,y coords"""
        return (random.randint(2, x), random.randint(2, y))

    def get_next_point(self, point):
        """Accepts a point and a direction.
        Returns the next point in that direction
        """
        if self.snake_direction == UP:
            return (point[0], point[1] + 1)
        elif self.snake_direction == DOWN:
            return (point[0], point[1] - 1)
        elif self.snake_direction == LEFT:
            return (point[0] - 1, point[1])
        else:
            return (point[0] + 1, point[1])

    def add_shape_to_shape_list(self, point, color):
        """Calculates the proper sized shape to add to the shape_list"""

        # First, find the center of the shape to draw
        center_x = (2 * point[0] - 1) * SIZE // 2
        center_y = (2 * point[1] - 1) * SIZE // 2

        # Now add the shape to draw to the list
        # SIZE - 2 means there will be a small border around each cell
        self.shape_list.append(
            arcade.create_rectangle_filled(
                center_x, center_y, SIZE - 2, SIZE - 2, color
            )
        )

    def draw_screen(self):
        """Draw the current screen"""

        # Define the outer border rectangle to enclose the screen
        outer_bottom_left = (0, 0)
        outer_bottom_right = (SCREENX * SIZE, 0)
        outer_top_right = (SCREENX * SIZE, SCREENY * SIZE)
        outer_top_left = (0, SCREENY * SIZE)
        outer = [
            outer_bottom_left,
            outer_bottom_right,
            outer_top_right,
            outer_top_left,
        ]

        # Define the inner border rectangle to enclose the game play area
        inner_bottom_left = (SIZE, SIZE)
        inner_bottom_right = ((SCREENX - 1) * SIZE, SIZE)
        inner_top_right = ((SCREENX - 1) * SIZE, (SCREENY - 1) * SIZE)
        inner_top_left = (SIZE, (SCREENY - 1) * SIZE)
        inner = [
            inner_bottom_left,
            inner_bottom_right,
            inner_top_right,
            inner_top_left,
        ]

        # Define the colors for each
        outer_colors = [BORDERCOLOR] * 4
        inner_colors = [BGCOLOR] * 4

        # Now add each shape to the shape_list
        self.shape_list.append(
            arcade.create_rectangles_filled_with_colors(outer, outer_colors)
        )
        self.shape_list.append(
            arcade.create_rectangles_filled_with_colors(inner, inner_colors)
        )

    def draw_apples(self):
        """Draws the apples from apple_list on the display surface"""

        for apple in self.apple_list:
            self.add_shape_to_shape_list(apple, APPLECOLOR)

    def draw_snake(self):
        """ Draws the snake on the display.
        The complete snake body lives in snake_list.
        The first element is the head, and is drawn in SNAKEHEADCOLOR
        The next elements are the body, and are drawn in SNAKEBODYCOLOR
        The last SNAKEFADE segments are the tail.
        We calculate a fade and draw each segment in a new color
        """

        # First, draw the snake's head
        self.add_shape_to_shape_list(self.snake_list[0], SNAKEHEADCOLOR)

        # Now, draw the body of the snake
        for snake in self.snake_list[1:SNAKEFADE]:
            self.add_shape_to_shape_list(snake, SNAKEBODYCOLOR)

        # Now fade out the last few segments
        colorFade = -180 // SNAKEFADE
        greenFade = SNAKEBODYCOLOR[1] - colorFade
        for snake in self.snake_list[SNAKEFADE:]:
            SNAKEFADECOLOR = (SNAKEBODYCOLOR[0], greenFade, SNAKEBODYCOLOR[2])
            self.add_shape_to_shape_list(snake, SNAKEFADECOLOR)
            greenFade -= colorFade

    def add_snake_segment(self):
        """Add a new segment by adding a new head
        Remove the tail if we're just moving
        If we're expanding, we leave the tail in place
        """

        self.snake_list.insert(0, self.get_next_point(self.snake_list[0]))
        if self.expand_snake == 0:
            del self.snake_list[-1]
        else:
            self.expand_snake -= 1

    # Check if the snake hit something
    def check_snake_hit(self):
        """ Did we hit something?
        If the head is in the same place as another object, then...

        If it's an apple:
            Remove the apple
            Give them the points
            Add a new apple to the board

        If it's the border:
            Game over

        If it's the body of the snake:
            Game over
        """
        # global snakeList, points, running, speed, expandSnake
        snake_head = self.snake_list[0]

        # Did we hit an apple? Good!
        if snake_head in self.apple_list:
            # Remove the apple and score some points
            self.apple_list.remove(snake_head)
            self.score += APPLEPOINTS

            # Since we're still a continuous game, add a new apple to eat
            # If it's under something else, get a new position
            new_apple = self.get_random_point(SCREENX - 1, SCREENY - 1)
            while new_apple in self.apple_list or new_apple in self.snake_list:
                new_apple = self.get_random_point(SCREENX - 1, SCREENY - 1)
            self.apple_list.append(new_apple)

            # Make the snake longer, and speed things up
            # Do this by taking 5% off the wait time
            self.expand_snake = 3
            self.snake_speed *= 0.95

        # Did we hit our own body?
        # We need to ignore the actual head, so look from the 2nd element on
        elif snake_head in self.snake_list[1:]:
            self.running = False
            print("Ouroboros not permitted!")

        # Did we run out of room?
        elif (
            snake_head[0] <= 0
            or snake_head[0] >= SCREENX
            or snake_head[1] <= 0
            or snake_head[1] >= SCREENY
        ):
            self.running = False
            print("Off screen!")

    def on_update(self, delta_time):
        """Update everything on the screen
        """

        # Are we done?
        if not self.running:
            arcade.close_window()

        # Should we move at all?
        # Check if we're paused - do nothing if so
        if not self.paused:

            # Not paused, so check if enough time has passed
            # If so, reset it and make the moves
            self.frame_time += delta_time
            if self.frame_time >= self.snake_speed:
                self.frame_time = 0.0

                # Move the snake
                self.add_snake_segment()

                # Check if the snake hit something
                self.check_snake_hit()

        # No matter what, clear the shape_list so we can use it again
        for shape in self.shape_list:
            self.shape_list.remove(shape)

    def on_draw(self):
        """Draw everything on the screen
        """

        # Required to render everything
        arcade.start_render()

        # Draw everything from back to front
        self.draw_screen()
        self.draw_apples()
        self.draw_snake()

        # Now draw all the shapes
        self.shape_list.draw()

    def on_key_press(self, key, modifiers):
        """Handle movement via keypresses
        """

        # Set the initial direction as unchanged
        newDirection = self.snake_direction

        # Our cardinal directions use I, J, K, and L
        # We also restrict you from moving straight backwards
        if key == arcade.key.L:
            if self.snake_direction == UP or self.snake_direction == DOWN:
                newDirection = RIGHT
        elif key == arcade.key.J:
            if self.snake_direction == UP or self.snake_direction == DOWN:
                newDirection = LEFT
        elif key == arcade.key.I:
            if self.snake_direction == RIGHT or self.snake_direction == LEFT:
                newDirection = UP
        elif key == arcade.key.K:
            if self.snake_direction == RIGHT or self.snake_direction == LEFT:
                newDirection = DOWN

        # You can also move relative to the direction, left or right
        # Using the arrows or the period and comma
        elif key == arcade.key.RIGHT or key == arcade.key.PERIOD:
            newDirection = CLOCKWISE[self.snake_direction]
        elif key == arcade.key.LEFT or key == arcade.key.COMMA:
            newDirection = COUNTERCLOCKWISE[self.snake_direction]

        # If the user presses Q or ESC, quit the game
        elif key == arcade.key.Q:
            self.running = False

        # If the user presses P, pause the game
        elif key == arcade.key.P:
            self.paused = not self.paused

        self.snake_direction = newDirection


if __name__ == "__main__":

    snake_game = Snake_Game(SCREENX * SIZE, SCREENY * SIZE, TITLE, BGCOLOR)
    snake_game.setup()

    # Start the render cycle
    arcade.run()
    print(f"Points: {snake_game.score}")
