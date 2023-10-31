# from yMoveCoord import yMoveCoord
# from xMoveCoord import xMoveCoord
# from axisReset import axis_reset
from time import sleep

def read_gcode():
    file_name = "practice.gcode"
    with open(file_name, "r") as f:
        for line in f:
            if "G28" in line:
                print("Reset")
                sleep(1)
                # axis_reset().xy_reset()
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
                    # zMoveCoord(z)
                if x != -1 and y != -1:
                    print("X " + str(x) + "\t Y " + str(y))
                    # xyMoveCoord(x, y)
                elif x != -1 and y == -1:
                    print("X " + str(x))
                    # xMoveCoord(x)
                elif x == -1 and y != -1:
                    print("Y " + str(y))
                    # yMoveCoord(y)
                sleep(1)
            
def main():
    read_gcode()

if __name__ == "__main__":
    main()