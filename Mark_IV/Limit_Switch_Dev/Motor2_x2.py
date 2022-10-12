from Limit_Switches import limitSwitches


while(1):

    if limitSwitches.motorx2() is True:
        print("Pressed")
    else:
        pass
