from math import ceil
import math
import os
import sys
from xMoveCoord import xMoveCoord
from yMoveCoord import yMoveCoord
from xyMoveCoord import xyMoveCoord

def xyCircleFill(radius=3, speed_mod=0.6, flip=False):
    # Initialize variables
    x_file_name = "x_coord.txt"
    y_file_name = "y_coord.txt"
    os.chdir("/home/pi/Exolith_Lab/Mark_IV/Sintering")
    x_coord = 0
    y_coord = 0
    focal_diameter = 0.7

    with open(x_file_name, "r") as f:
        x_coord = float(f.readline())
    with open(y_file_name, "r") as f:
        y_coord = float(f.readline())

    # Radius of circle that curve being drawn is a part of
    radius = radius - 0.5 * focal_diameter
    num_lines = ceil(2 * radius / focal_diameter) - 1
    diff = float(2 * radius / (num_lines + 1))
    print(num_lines)
    print(diff)

    line_dir = 1
    if not(flip):
        y_coord += 0.5 * focal_diameter
        yMoveCoord(y_coord, speed_mod=speed_mod, pause=True)
        x_center = x_coord
        y_center = y_coord - radius
        for i in range(num_lines):
            y_coord -= diff
            x_coord = line_dir * math.cos(math.asin((y_coord - y_center) / radius)) * radius + x_center
            line_dir *= -1
            xyMoveCoord(x_coord, y_coord + (i + 1) * focal_diameter * 2, speed_mod=speed_mod, pause=True)
            x_coord = -2 * (x_coord - x_center) + x_coord
            xMoveCoord(x_coord, speed_mod=speed_mod, pause=True)
    else:
        x_coord += 0.5 * focal_diameter
        xMoveCoord(x_coord, speed_mod=speed_mod, pause=True)
        x_center = x_coord - radius
        y_center = y_coord
        for i in range(num_lines):
            x_coord -= diff
            y_coord = line_dir * math.sin(math.acos((x_coord - x_center) / radius)) * radius + y_center
            line_dir *= -1
            xyMoveCoord(x_coord + (i + 1) * focal_diameter * 2, y_coord, speed_mod=speed_mod, pause=True)
            y_coord = -2 * (y_coord - y_center) + y_coord
            yMoveCoord(y_coord, speed_mod=speed_mod, pause=True)

def main():
    if len(sys.argv) == 4:
        xyCircleFill(float(sys.argv[1]), float(sys.argv[2]), bool(int(sys.argv[3])))
    else:
        xyCircleFill()

if __name__ == "__main__":
    main()