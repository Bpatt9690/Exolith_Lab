from Limit_Switches import limitSwitches

while(1):

    if limitSwitches.motorx1() is True:
        print("Pressed")
    else:
        pass
