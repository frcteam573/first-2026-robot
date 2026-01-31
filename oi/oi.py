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
import commands.elevator
import commands.drivetrain
import commands.shooter
import commands.intake
# import commands.climber

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
	
#Keymap.Elevator.setLevel3.whileTrue(commands.elevator.setPosition(Robot.elevator,position=10))
#Keymap.Elevator.setLevel1.whileTrue(commands.elevator.setPosition(Robot.elevator,position=0))

Keymap.Shooter.setupShooter.whileTrue(commands.shooter.Shoot(Robot.shooter))
Keymap.Intake.intakeIn.whileTrue(commands.intake.IntakeIn(Robot.intake))
Keymap.Intake.intakeOut.whileTrue(commands.intake.IntakeOut(Robot.intake))
Keymap.Intake.intakeRetract.whileTrue(commands.intake.IntakeRetract(Robot.intake))
