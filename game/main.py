import turtle
import time
import os

import constants
import player
import level
import hitbox

constants.FPS = 60

wn = turtle.Screen()
wn.title("Oli's Platformer")
wn.bgcolor("black")
wn.setup(700, 500)
wn.tracer(0)

message = turtle.Turtle()
message.speed(0)
message.color("white")
message.penup()
message.hideturtle()
message.goto(0, 0)
message.write("Actions Required In Console", align="center", font=("Courier", 24, "normal"))

active_hitbox = hitbox.Hitbox((), ())

player1 = player.Player()

# ----- load a level -----
while True:
    level_name = input("input the name of the level you want to load: ")
    try:
        current_level = level.Level(f"..\levels\{level_name}.txt")
        print("level loading successful! Navigate to the game window to play")
        message.clear()
        break
    except FileNotFoundError:
        if level_name == "e":
            quit()
        print(f"no level named '{level_name}.txt' in the levels folder."
              f" try again, or type 'e' to exit")
current_level.draw_level()

while True:
    wn.update()

    player1.calculate_player_movement(constants.FPS)

# ----- check if player enters a hitbox -----
    player1.setx(player1.xcor() + player1.dx)
    hitbox_data = player1.check_is_in_any_hitbox(current_level)

    if player1.is_in_hitbox:
        collided_hitbox = hitbox.Hitbox(hitbox_data[0], hitbox_data[1])
        if player1.dx < 0:
            side_of_collision = constants.Sides.RIGHT
        elif player1.dx > 0:
            side_of_collision = constants.Sides.LEFT
        player1.collide_with_hitbox(collided_hitbox, side_of_collision)

    player1.sety(player1.ycor() + player1.dy)
    hitbox_data = player1.check_is_in_any_hitbox(current_level)

    if player1.is_in_hitbox:
        collided_hitbox = hitbox.Hitbox(hitbox_data[0], hitbox_data[1])
        active_hitbox = collided_hitbox  # a hitbox is active when a player stands on top of it
        if player1.dy < 0:
            side_of_collision = constants.Sides.TOP
        elif player1.dy > 0:
            side_of_collision = constants.Sides.BOTTOM
        player1.collide_with_hitbox(collided_hitbox, side_of_collision)

# ----- check if player has left the outer boundary -----
    if player1.ycor() < -180:
        player1.put_on_ground(current_level)

    if player1.xcor() < current_level.boundary_x_range[0] + 10:
        player1.setx(current_level.boundary_x_range[0] + 10)
        player1.dx = 0

    if player1.xcor() > current_level.boundary_x_range[1] - 10:
        player1.setx(current_level.boundary_x_range[1] - 10)
        player1.dx = 0

# ----- checks if the player has left an active hitbox -----
    try:
        if player1.xcor() - 11 > active_hitbox.x_range[1] or player1.xcor() + 11 < active_hitbox.x_range[0]:
            player1.is_on_ground = False
            active_hitbox.x_range = ()
            active_hitbox.y_range = ()
    except IndexError:
        pass
    time.sleep(0.000001)  # this limits the frame rate to ~60 fps
