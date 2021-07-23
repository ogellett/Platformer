import turtle
import winsound
import keyboard

import constants


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.acceleration = 30
        self.deceleration = 60
        self.shape("square")
        self.color("blue")
        self.turtlesize(stretch_wid=2, stretch_len=1)
        self.penup()
        self.goto(-260, -175)
        self.dx = 0
        self.dy = 0
        self.is_on_ground = False
        self.is_in_hitbox = False
        self.sides_in_hitbox = []

    def calculate_player_movement(self, fps):
        if keyboard.is_pressed("a"):
            self.dx -= self.acceleration / fps
        elif keyboard.is_pressed("d"):
            self.dx += self.acceleration / fps
        else:
            if self.dx > 0:
                self.dx -= self.deceleration / fps
                if self.dx < 0:
                    self.dx = 0
            elif self.dx < 0:
                self.dx += self.deceleration / fps
                if self.dx > 0:
                    self.dx = 0

        if keyboard.is_pressed("space") and self.is_on_ground:
            self.jump(fps)
        else:
            self.apply_gravity(fps)

    def jump(self, fps):
        self.dy += 1000 / fps
        winsound.PlaySound("jump.wav", winsound.SND_ASYNC)
        self.is_on_ground = False

    def apply_gravity(self, fps):
        self.dy -= 100 / fps

    def put_on_ground(self, level):
        self.sety(level.boundary_y_range[0] + 20)
        self.dy = 0
        self.is_on_ground = True

    def check_is_in_any_hitbox(self, level):
        player_top = self.ycor() + 20
        player_bottom = self.ycor() - 20
        player_left = self.xcor() - 10
        player_right = self.xcor() + 10
        i = 0
        for hitbox in level.hitboxes:
            if (hitbox.y_range[0] <= player_top <= hitbox.y_range[1]
                    or hitbox.y_range[0] <= player_bottom <= hitbox.y_range[1]
                    or player_top > hitbox.y_range[1] and player_bottom < hitbox.y_range[0]):
                if (hitbox.x_range[0] <= player_right <= hitbox.x_range[1]
                        or hitbox.x_range[0] <= player_left <= hitbox.x_range[1]):
                    self.is_in_hitbox = True
                    return hitbox.x_range, hitbox.y_range
            i += 1

        else:
            self.is_in_hitbox = False

    def collide_with_hitbox(self, hitbox, side):
        if side == constants.Sides.LEFT:
            self.setx(hitbox.x_range[0] - 11)
            self.dx = 0
            self.is_in_hitbox = False

        if side == constants.Sides.RIGHT:
            self.setx(hitbox.x_range[1] + 11)
            self.dx = 0
            self.is_in_hitbox = False

        if side == constants.Sides.TOP:
            self.sety(hitbox.y_range[1] + 21)
            self.is_on_ground = True
            self.is_in_hitbox = False
            self.dy = 0

        if side == constants.Sides.BOTTOM:
            self.sety(hitbox.y_range[0] - 21)
            self.is_in_hitbox = False
            self.dy = 0

