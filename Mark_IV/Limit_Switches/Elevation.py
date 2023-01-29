from Limit_Switches import limitSwitches

ls = limitSwitches()

while 1:

    if ls.elevation() is True:
        print("Pressed")
    else:
        pass
