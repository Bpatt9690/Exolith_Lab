from Limit_Switches import limitSwitches

ls = limitSwitches()

while 1:

    if ls.motory1() is True:
        print("Pressed")
    else:
        pass
