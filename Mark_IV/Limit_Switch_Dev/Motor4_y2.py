from Limit_Switches import limitSwitches

while(1):

    if limitSwitches.motory2() is True:
        print("Pressed")
    else:
        pass
