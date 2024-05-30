import turtle, pathlib
import keyboard
import time
import editor_level as lvl

print('''
Controls:
wasd for movement,
arrow keys for shape resizing,
shift to slow down movement/resizing,
space to stamp a platform/obstacle,
r to delete an existing platform/obstacle
ctrl+s to save the level
''')

hitboxes = []
stamp_info = []
x_stretch = 1
y_stretch = 1

window = turtle.Screen()
window.title("Oli's Level Editor")
window.bgcolor("black")
window.setup(width=700, height=500)
window.tracer(0)
lvl.draw_boundary()
lvl.print_StartAndEndZone()

stamp = turtle.Turtle()
stamp.shape("square")
stamp.color("white")
stamp.penup()
stamp.id_list = []

message = turtle.Turtle()
message.speed(0)
message.color("white")
message.penup()
message.hideturtle()
message.goto(0, 0)
message.write("Actions Required In Console", align="center", font=("Courier", 24, "normal"))

# ----- load a pre-existing level -----
while True:
    user_input = input("do you want to load an existing level? (y/n) ")
    if user_input == "y":
        while True:
            level_name = input("type the name of the level you want to load: ")
            try:
                level = lvl.EditorLevel(f"..\levels\{level_name}.txt")
                message.clear()
                break
            except FileNotFoundError:
                if level_name == "e":
                    quit()
                print(f"'{level_name}.txt' not found in the levels folder."
                      f" try again, or type 'e' to exit")
        i = 0
        for coord in level.stamp_coords:
            stamp.shapesize(stretch_len=level.stamp_xstretches[i], stretch_wid=level.stamp_ystretches[i])
            stamp.goto(coord[0], coord[1])
            new_hitbox = lvl.generate_hitbox(coord[0], coord[1], level.stamp_xstretches[i], level.stamp_ystretches[i])
            stamp.id_list.append(stamp.stamp())
            hitboxes.append(new_hitbox)
            stamp_info.append((coord[0], coord[1], level.stamp_xstretches[i], level.stamp_ystretches[i]))
            i += 1
        print("you can now edit the existing level in the editor window")
        message.clear()
        break
    elif user_input == "n":
        print("navigate to the level editor window to begin creating a level")
        message.clear()
        break
    elif user_input == "e":
        quit()
    else:
        print("input not recognised, type 'y' or 'n', or type 'e' to exit")

    

# ----- create a 'levels' folder -----
path = pathlib.Path("..\levels")
pathlib.Path.mkdir(path, exist_ok=True)
level_count = len(list(path.glob("*.txt")))

# ----- main program loop -----
while True:
    # ----- save the level as a text file -----
    if keyboard.is_pressed("ctrl") and keyboard.is_pressed("s"):
        with open(f"..\levels\level{level_count + 1}.txt", "w") as level:
            i = 0
            level.write("xrange_bot,xrange_top,yrange_bot,yrange_top,stamp_xcor,stamp_ycor,x_stretch,y_stretch\n")
            for hitbox in hitboxes:
                data_to_write = str(hitbox)
                data_to_write = data_to_write.replace("[", "")
                data_to_write = data_to_write.replace("]", "")
                data_to_write = data_to_write.replace("(", "")
                data_to_write = data_to_write.replace(")", "")
                data_to_write = data_to_write.replace(" ", "")
                hitbox_stamp_info = str(stamp_info[i])
                hitbox_stamp_info = hitbox_stamp_info.replace("(", "")
                hitbox_stamp_info = hitbox_stamp_info.replace(")", "")
                hitbox_stamp_info = hitbox_stamp_info.replace(" ", "")
                level.write(data_to_write + "," + hitbox_stamp_info + "\n")
                i += 1
        print(f"level saved as 'level{level_count + 1}.txt'")
        print("you can rename the text file to whatever you'd like (renaming prevents accidental overwriting of level)")
        break

    # -----movement controls-----
    if keyboard.is_pressed("shift"):
        movement_rate = 1
    else:
        movement_rate = 10
    x = stamp.xcor()
    y = stamp.ycor()
    if keyboard.is_pressed("w"):
        stamp.sety(y + movement_rate)
    if keyboard.is_pressed("a"):
        stamp.setx(x - movement_rate)
    if keyboard.is_pressed("s"):
        stamp.sety(y - movement_rate)
    if keyboard.is_pressed("d"):
        stamp.setx(x + movement_rate)

    # -----resize controls-----
    if keyboard.is_pressed("shift"):
        stretch_factor = 0.1
    else:
        stretch_factor = 1

    if keyboard.is_pressed("up"):
        y_stretch += stretch_factor
    if keyboard.is_pressed("down") and y_stretch > 1:
        y_stretch -= stretch_factor
    if keyboard.is_pressed("right"):
        x_stretch += stretch_factor
    if keyboard.is_pressed("left") and x_stretch > 1:
        x_stretch -= stretch_factor

    stamp.shapesize(stretch_len=x_stretch, stretch_wid=y_stretch)

    # -----stamp shapes & create hitboxes-----
    if keyboard.is_pressed("space"):
        new_hitbox = lvl.generate_hitbox(stamp.xcor(), stamp.ycor(), x_stretch, y_stretch)
        if lvl.hitbox_overlaps(hitbox_to_check=new_hitbox, hitbox_list=hitboxes):
            pass
        else:
            stamp.id_list.append(stamp.stamp())
            hitboxes.append(new_hitbox)
            stamp_info.append((round(stamp.xcor()), round(stamp.ycor()), x_stretch, y_stretch))
    # ----- delete existing hitboxes -----
    elif keyboard.is_pressed("r"):
        new_hitbox = lvl.generate_hitbox(stamp.xcor(), stamp.ycor(), x_stretch, y_stretch)
        if lvl.hitbox_overlaps(hitbox_to_check=new_hitbox, hitbox_list=hitboxes):
            overlap_index = lvl.hitbox_overlaps(hitbox_to_check=new_hitbox, hitbox_list=hitboxes, return_overlap_index=True)
            stamp.clearstamp(stamp.id_list[overlap_index])
            stamp.id_list.pop(overlap_index)
            hitboxes.pop(overlap_index)

    window.update()
    time.sleep(0.016667)
