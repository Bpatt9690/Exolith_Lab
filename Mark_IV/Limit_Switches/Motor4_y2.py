from Limit_Switches import limitSwitches

ls = limitSwitches()

while 1:

    if ls.motory2() is True:
        print("Pressed")
    else:
        pass
