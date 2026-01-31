""" This creates buttons map for the controllers"""
import commands2
import wpilib
from utils.oi import (
    JoystickAxis,
    XBoxController,
)

# -- Create controllers --
controllerDRIVER = XBoxController
controllerOPERATOR = XBoxController

class Controllers:
    DRIVER = 0
    OPERATOR = 1

    DRIVER_CONTROLLER = wpilib.Joystick(0)
    OPERATOR_CONTROLLER = wpilib.Joystick(1)
#-- Create keymap class --
class Keymap:
    #class Elevator:
       # setLevel3 = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RB)
       # setLevel1 = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.LB)

    class Drivetrain:
        followPath = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.A)
        
    class Climber:
        climbUp =  commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.RB)
        climbDown = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.LB)

####################################    Joel rules      #############################
###     oi oi baka baka
## this is our code


#####     #####
#####     #####
       ##
###         ###
  ###     ###
    ### ###
             

