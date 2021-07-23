import turtle


class EditorLevel:
    def __init__(self, level_filename):
        self.stamp_coords = []
        self.stamp_xstretches = []
        self.stamp_ystretches = []
        with open(f"{level_filename}", "r") as file:
            lines = file.readlines()[1:]
            for line in lines:
                line = line.strip()
                line = line.split(",")
                self.stamp_coords.append((int(line[4]), int(line[5])))
                self.stamp_xstretches.append(float(line[6]))
                self.stamp_ystretches.append(float(line[7]))


def hitbox_overlaps(hitbox_to_check, hitbox_list, return_overlap_index=False):
    top_left = (hitbox_to_check[0][0], hitbox_to_check[1][1])
    top_right = (hitbox_to_check[0][1], hitbox_to_check[1][1])
    bot_left = (hitbox_to_check[0][0], hitbox_to_check[1][0])
    bot_right = (hitbox_to_check[0][1], hitbox_to_check[1][0])
    hitbox_corners = (top_left, top_right, bot_left, bot_right)
    for hitbox in hitbox_list:
        for corner in hitbox_corners:
            if hitbox[0][0] <= corner[0] <= hitbox[0][1]:
                if hitbox[1][0] <= corner[1] <= hitbox[1][1]:
                    if return_overlap_index:
                        return hitbox_list.index(hitbox)
                    else:
                        return True
    else:
        return False


def generate_hitbox(x_cor, y_cor, x_stretch, y_stretch):
    x_range = (round(x_cor - (10 * x_stretch)),
               round(x_cor + (10 * x_stretch)))
    y_range = (round(y_cor - (10 * y_stretch)),
               round(y_cor + (10 * y_stretch)))
    return x_range, y_range


def draw_boundary():
    boundary_x_range = (-300, 300)
    boundary_y_range = (-200, 200)
    pen = turtle.Turtle()
    pen.color("white")
    pen.hideturtle()
    pen.penup()
    pen.goto(boundary_x_range[0], boundary_y_range[0])
    pen.pendown()
    pen.goto(boundary_x_range[1], boundary_y_range[0])
    pen.goto(boundary_x_range[1], boundary_y_range[1])
    pen.goto(boundary_x_range[0], boundary_y_range[1])
    pen.goto(boundary_x_range[0], boundary_y_range[0])


def print_StartAndEndZone():
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