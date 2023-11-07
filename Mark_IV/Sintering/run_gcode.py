# from yMoveCoord import yMoveCoord
# from xMoveCoord import xMoveCoord
# from xyMoveCoord import xyMoveCoord
# from zMoveCoord import zMoveCoord
# from axisReset import axis_reset
import matplotlib.pyplot as plt
import numpy as np
# from time import sleep

def read_gcode():
    xy_fast = 0.7
    xy_slow = 0.4
    z_speed_mod = 0.3
    pause = 1
    count = 0

    x_coords = []
    y_coords = []
    z_coords = []

    file_name = "practice.gcode"
    pause_file_name = "pause.txt"

    with open(pause_file_name, "w") as f:
        f.write("1")
    with open(file_name, "r") as f:
        for line in f:
            # if "G28" in line:
            #     if "Home" in line:
            #         print("Home")
            #         axis_reset().xy_reset()
            #         axis_reset().z_axis_reset()
            #     if "X" in line and "Y" in line:
            #         print("XY Reset")
            #         axis_reset().xy_reset()
            if "G0" in line:
                xy_speed_mod = xy_fast
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
                    # zMoveCoord(z, z_speed_mod)
                    # while(pause != "0"):
                    #     with open(pause_file_name, "r") as f:
                    #         pause = f.readline()
                    # with open(pause_file_name, "w") as f:
                    #     pause = "1"
                    #     f.write("1")
                    z_coords.append(z)
                else:
                    z_coords.append(z_coords[count - 1])
                if x != -1 and y != -1:
                    print("X " + str(x) + "\t Y " + str(y))
                    # xyMoveCoord(x, y, xy_speed_mod, pause=True)
                    x_coords.append(x)
                    y_coords.append(y)
                elif x != -1 and y == -1:
                    print("X " + str(x))
                    # xMoveCoord(x, xy_speed_mod, pause=True)
                    x_coords.append(x)
                    y_coords.append(y_coords[count - 1])
                elif x == -1 and y != -1:
                    print("Y " + str(y))
                    # yMoveCoord(y, xy_speed_mod, pause=True)
                    x_coords.append(x_coords[count - 1])
                    y_coords.append(y)
                else:
                    x_coords.append(0)
                    y_coords.append(0)
                count += 1

    x_coords = np.array(x_coords[2:(len(x_coords)-1)])
    y_coords = np.array(y_coords[2:(len(y_coords)-1)])
    z_coords = np.array(z_coords[2:(len(z_coords)-1)])
    # x_coords = np.array(x_coords[2:400])
    # y_coords = np.array(y_coords[2:400])
    # z_coords = np.array(z_coords[2:400])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect([max(x_coords) - min(x_coords), max(y_coords) - min(y_coords), max(z_coords) - min(z_coords)])
    ax.plot_wireframe(x_coords,y_coords,z_coords.reshape(-1, 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
            
def main():
    read_gcode()

if __name__ == "__main__":
    main()