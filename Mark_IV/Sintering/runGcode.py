from yMoveCoord import yMoveCoord
from xMoveCoord import xMoveCoord
from xyMoveCoord import xyMoveCoord
from zMoveCoord import zMoveCoord
from axisReset import axis_reset

def read_gcode():
    xy_fast = 0.7
    xy_slow = 0.4
    z_speed_mod = 0.3
    pause = 1
    count = 0

    file_name = "practice.gcode"
    pause_file_name = "pause.txt"

    with open(pause_file_name, "w") as f:
        f.write("1")
    with open(file_name, "r") as f:
        for line in f:
            light_pause = True
            if "G28" in line:
                if "Home" in line:
                    print("Home")
                    axis_reset().xy_reset()
                    axis_reset().z_axis_reset()
                if "X" in line and "Y" in line:
                    print("XY Reset")
                    axis_reset().xy_reset()
            if "G0" in line:
                xy_speed_mod = xy_fast
                light_pause = False
            if "G1" in line:
                xy_speed_mod = xy_slow
            if "G0" in line or "G1" in line:
                x = -1
                y = -1
                z = -1
                line_segs = line.split(' ')
                for seg in line_segs:
                    if seg[0] == "X":
                        x = float(seg[1:]) / 10
                        
                    elif seg[0] == "Y":
                        y = float(seg[1:]) / 10
                        
                    elif seg[0] == "Z":
                        z = float(seg[1:]) / 10
                        
                if z != -1:
                    print("Z " + str(z))
                    zMoveCoord(z, z_speed_mod)
                    while(pause != "0"):
                        with open(pause_file_name, "r") as f:
                            pause = f.readline()
                    with open(pause_file_name, "w") as f:
                        pause = "1"
                        f.write("1")
                if x != -1 and y != -1:
                    print("X " + str(x) + "\t Y " + str(y))
                    xyMoveCoord(x, y, xy_speed_mod, pause=light_pause)
                elif x != -1 and y == -1:
                    print("X " + str(x))
                    xMoveCoord(x, xy_speed_mod, pause=light_pause)
                elif x == -1 and y != -1:
                    print("Y " + str(y))
                    yMoveCoord(y, xy_speed_mod, pause=light_pause)
                count += 1
            
def main():
    read_gcode()

if __name__ == "__main__":
    main()