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
    class Shooter:
        setupShooter = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerOPERATOR.RB)
        shoot = commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerOPERATOR.Y)

    class Drivetrain:
        followPath = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.A)

    #class Intake:
         
   # class Climber:        



       # **in code*
       # Y- shoot
       # A- setup shooter
       # B- intake
       # X- climb




####################################    Joel rules      #############################
###     oi oi baka baka
## this is our code


#####     #####
#####     #####
       ##
###         ###
  ###     ###
    ### ###
             

