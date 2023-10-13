"""
Pirates of the Caribbean Maze Game
COMP123 Spring 2022
Cat Martins and Sana Mohammed

Instructions: Use the arrow keys to move Captain Jack Sparrow through the maze.
Collect the treasure without colliding with any enemies (Davy Jones)!
"""

# -----------------------------------------------------------
import turtle
import math
import random

# -----------------------------------------------------------

# Set up 700x700 turtle screen with black background and title
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Maze Game")
wn.setup(700, 700)
wn.tracer(0)

# Register the images as turtle character shapes
turtle.register_shape("animatedCaptain.gif")
turtle.register_shape("animatedCaptainLeft.gif")
turtle.register_shape("treasure.gif")
turtle.register_shape("wall.gif")
turtle.register_shape("animatedDavyJones.gif")
turtle.register_shape("animatedDavyJonesLeft.gif")
turtle.register_shape("youwin.gif")

# Set up turtle and draw title text
penTitle = turtle.Turtle()
penTitle.speed(0)
penTitle.shape("square")
penTitle.color("white")
penTitle.penup()
penTitle.hideturtle()
penTitle.goto(10, 350)
penTitle.write("Pirates of the Caribbean Maze", align="center", font=("Courier", 36, "normal"))

# Set up turtle and draw player score text
penScore = turtle.Turtle()
penScore.speed(0)
penScore.shape("square")
penScore.color("gold")
penScore.penup()
penScore.hideturtle()
penScore.goto(10, 320)
penScore.write("Captain Jack Sparrow's Gold: 0", align="center", font=("Courier", 24, "normal"))


class Pen(turtle.Turtle):
    """ Set up standard turtle class to simplify creating pens. """

    def __init__(self):
        turtle.Turtle.__init__(self)
        self.color("white")
        self.shape("square")
        self.penup()
        self.speed(0)


class Player(turtle.Turtle):
    """ Set up player and abilities such as moving in different directions and figuring out if a collision occurred. """

    def __init__(self):
        """ Set up player turtle with animatedCaptain.gif as the shape. """
        turtle.Turtle.__init__(self)
        self.color("blue")
        self.shape("animatedCaptain.gif")
        self.penup()
        self.speed(0)

    def go_up(self):
        """ Gets player's x and y coordinates and sees if they are in the walls list. If they aren't, moves the player
         up 24 pixels (one "step"). """
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(self.xcor(), self.ycor() + 24)

    def go_down(self):
        """ Gets player's x and y coordinates and sees if they are in the walls list. If they aren't, moves the player
        down 24 pixels (one "step"). """
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(self.xcor(), self.ycor() - 24)

    def go_left(self):
        """ Gets player's x and y coordinates and sees if they are in the walls list. If they aren't, moves the player
        left 24 pixels (one "step"). Sets the turtle shape to the image facing left. """
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()
        self.shape("animatedCaptainLeft.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(self.xcor() - 24, self.ycor())

    def go_right(self):
        """ Gets player's x and y coordinates and sees if they are in the walls list. If they aren't, moves the player
        right 24 pixels (one "step"). Sets the turtle shape to the image facing right. """
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()
        self.shape("animatedCaptain.gif")
        if (move_to_x, move_to_y) not in walls:
            self.goto(self.xcor() + 24, self.ycor())

    def is_collision(self, other):
        """ Checks if the player was in a collision with the input turtle (enemy or treasure). Gets the coordinates
         for both and calculates distance, returns True/False. """
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < 5:
            return True
        else:
            return False


class Treasure(turtle.Turtle):
    """ Set up treasure turtle attributes. """

    def __init__(self, x, y):
        """ Set up treasure turtle with treasure.gif as the shape. """
        turtle.Turtle.__init__(self)
        self.color("gold")
        self.shape("treasure.gif")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        """ Moves the turtle to coordinates off the screen and hides it to "destroy." """
        self.goto(2000, 2000)
        self.hideturtle()


class Enemy(turtle.Turtle):
    """ Set up enemy turtle shape and attributes. Chooses and sets enemy turtle's next move. """

    def __init__(self, x, y):
        """ Set up enemy turtle with animatedDavyJones.gif as the shape and random direction choice. """
        turtle.Turtle.__init__(self)
        self.shape("animatedDavyJones.gif")
        self.penup()
        self.speed(10)
        self.gold = 25
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        """ Chooses enemy's next coordinate location and moves turtle there. Calculates if the enemy is close to the
        player to set coordinates to head towards player turtle, else chooses random heading. Calculates one step by
        adding 24 pixels to current x and/or y position. Checks if new coordinates are within the maze. Moves turtle."""

        # Set dx, dy coordinate variables according to result of random choice and is_close direction
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "left":
            self.shape("animatedDavyJonesLeft.gif")
            dx = -24
            dy = 0
        elif self.direction == "right":
            self.shape("animatedDavyJones.gif")
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        # If is_close to the player returns True, sets the direction to head towards the player
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = "left"
            elif player.xcor() > self.xcor():
                self.direction = "right"
            elif player.ycor() < self.ycor():
                self.direction = "down"
            elif player.ycor() > self.ycor():
                self.direction = "up"

        # Sets the enemy turtle coordinates according to the coordinates returned by self.direction if statement
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        # Checks if the set coordinates above are in the walls list. If they aren't, moves enemy turtle to the
        # coordinates. If they are, chooses another direction.
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        # Calls function self.move after random milliseconds
        turtle.ontimer(self.move, t=random.randint(180, 270))

    def is_close(self, other):
        """ Calculates the distance between the enemy and input other turtle. Returns True/ False. """

        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2))
        if distance < 75:
            return True
        else:
            return False

    def destroy(self):
        """ Moves the turtle to coordinates off the screen and hides it to "destroy." """
        self.goto(2000, 2000)
        self.hideturtle()


# Create levels list (can add more levels if desired)
levels = [""]

# Create level_1 list for maze set up
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXXE         XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "X       XX  XXX        XX",
    "XXXXXX  XX  XXXE       XX",
    "XXXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX TXXXXX",
    "X  XXXE       XXXX  XXXXX",
    "X  XXX  XXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXXXX     XXXXX  X",
    "XXXXXXXXXXXXXXX  XXXXX  X",
    "XXX  XXXXXXXXXX        TX",
    "XXXT                    X",
    "XXXE        XXXXXXXXXXXXX",
    "XXXXXXXXXX  XXXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX T XXXXXE             X",
    "XX   XXXXXXXXXXXXX  XXXXX",
    "XX    XXXXXXXXXXXX  XXXXX",
    "XX          XXXX  E     X",
    "XXXXE            T      X",
    "XXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Create treasure and enemies lists
treasures = []
enemies = []

# Adding level_1 to the levels list
levels.append(level_1)


def setup_maze(level):
    """ Set up the maze with player, enemies, and treasure by looping through the length of the input level list. """

    for y in range(len(level)):
        for x in range(len(level[y])):
            # Gets the character in the list and translates its position to coordinates that are on the screen.
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screeen_y = 288 - (y * 24)

            if character == "X":
                # Create maze wall by stamping turtle, adds screen coordinates to wall list
                pen.goto(screen_x, screeen_y)
                pen.shape("wall.gif")
                pen.stamp()
                walls.append((screen_x, screeen_y))

            if character == "P":
                # Moves the player to screen coordinates
                player.goto(screen_x, screeen_y)

            if character == "E":
                # Adds enemy location to enemies list
                enemies.append(Enemy(screen_x, screeen_y))
            if character == "T":
                # Adds treasure location to treasures list
                treasures.append(Treasure(screen_x, screeen_y))


pen = Pen()
player = Player()

# Create walls list
walls = []

# Set up maze with level 1
setup_maze(levels[1])

# Sets which direction the player goes according to arrow key press
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

wn.tracer(0)

# Moves the enemy turtle after 250 milliseconds
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

# Sets up the win turtle with youwin.gif shape
penss = turtle.Turtle()
penss.speed(0)
penss.shape("youwin.gif")
penss.penup()
penss.goto(2099, 2095)
player_gold = 0

while True:

    for enemy in enemies:
        # Sets the player position to the original location if a collision with enemy occurs
        if player.is_collision(enemy):
            player.goto(-264, 264)
            player.direction = "stop"

    for treasure in treasures:
        # Hides the treasure turtle if a collision with the player occurs. Increases the player score by 20 and writes
        # that score on the screen.
        if player.is_collision(treasure):
            treasure.destroy()
            treasures.remove(treasure)
            player_gold = player_gold + 20
            penScore.clear()
            penScore.write("Captain Jack Sparrow's Gold: {} ".format(player_gold), align="center",
                           font=("Courier", 24, "normal"))

        if player_gold == 100:
            # Shows the win turtle if all the treasure has been collected
            penss.goto(0, 0)

    wn.update()
