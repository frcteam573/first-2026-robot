""" This creates buttons map for the controllers"""
import commands2
import wpilib
import config
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
    
    class Drivetrain:
        followPath = commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.A)
        
    class Climber:
        # set pos code
        climbUp =  JoystickAxis(Controllers.DRIVER, controllerDRIVER.LT)
        climbDown = JoystickAxis(Controllers.DRIVER, controllerDRIVER.RT)
        # manual code
        # extendclimber = JoystickAxis(Controllers.DRIVER, controllerDRIVER.LT)
        # retractclimber = JoystickAxis(Controllers.DRIVER, controllerDRIVER.RT)
      
         

####################################    Joel rules      #############################
###     oi oi baka baka
## this is our code


#####     #####
#####     #####
       ##
###         ###
  ###     ###
    ### ###
             

