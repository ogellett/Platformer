import turtle
import hitbox


class Level:
    def __init__(self, level_filepath):
        self.boundary_x_range = (-300, 300)
        self.boundary_y_range = (-200, 200)
        self.hitboxes = []
        self.hitbox_x_ranges = []
        self.hitbox_y_ranges = []
        with open(f"{level_filepath}", "r") as file:
            lines = file.readlines()[1:]
            for line in lines:
                line = line.strip()
                line = line.split(",")
                self.hitboxes.append(hitbox.Hitbox((int(line[0]), int(line[1])), (int(line[2]), int(line[3]))))

    def draw_level(self):
        self.draw_boundary()
        self.draw_hitboxes()
        self.draw_start_end_zones()

    def draw_hitboxes(self):
        pen = turtle.Turtle()
        pen.color("white")
        pen.hideturtle()
        pen.penup()
        i = 0
        for hitbox in self.hitboxes:
            pen.goto(hitbox.x_range[0], hitbox.y_range[0])
            pen.pendown()
            pen.begin_fill()
            pen.setx(hitbox.x_range[1])
            pen.sety(hitbox.y_range[1])
            pen.setx(hitbox.x_range[0])
            pen.sety(hitbox.y_range[0])
            pen.penup()
            pen.end_fill()
            i += 1

    def draw_boundary(self):
        pen = turtle.Turtle()
        pen.color("white")
        pen.hideturtle()
        pen.penup()
        pen.goto(self.boundary_x_range[0], self.boundary_y_range[0])
        pen.pendown()
        pen.goto(self.boundary_x_range[1], self.boundary_y_range[0])
        pen.goto(self.boundary_x_range[1], self.boundary_y_range[1])
        pen.goto(self.boundary_x_range[0], self.boundary_y_range[1])
        pen.goto(self.boundary_x_range[0], self.boundary_y_range[0])

    def draw_start_end_zones(self):
        stamp = turtle.Turtle()
        stamp.penup()
        stamp.shape("square")
        stamp.shapesize(stretch_len=4, stretch_wid=2.5)
        stamp.color("red")
        stamp.goto(-260, -175)
        stamp.stamp()
        stamp.color("green")
        stamp.goto(260, 175)
        stamp.stamp()
        stamp.hideturtle()