""" This creates links between buttons and commands for the controllers"""
import math
import commands2
import wpilib
from commands2 import (
	InstantCommand,
	ParallelCommandGroup,
	SequentialCommandGroup,
	WaitCommand,
	FunctionalCommand,
)
import commands.climber
import commands.elevator
import commands.drivetrain




import commands
import config
from oi.keymap import Controllers, Keymap

import constants
from robotcontainer import Robot
import robotcontainer



class OI:
  
	@staticmethod
	def init() -> None:
		pass

	@staticmethod
	def map_controls():
		pass

# Below is the mapping used to call commands based on user joystick input.

# #======================== drivetrain ========================#
    #This can be empty as SwerveDriveCustome command is set to run by default in teleopinit.
	
# Keymap.Elevator.setLevel3.whileTrue(commands.elevator.setPosition(Robot.elevator,position=10))
# Keymap.Elevator.setLevel1.whileTrue(commands.elevator.setPosition(Robot.elevator,position=0))

Keymap.Climber.climbUp.whileTrue(commands.climber.setPosition(Robot.climber,position=10))
Keymap.Climber.climbDown.whileTrue(commands.climber.setPosition(Robot.climber,position=0))

