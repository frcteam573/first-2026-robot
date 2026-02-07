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
import commands.shooter
import commands.intake





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
	

# set pos code
commands2.button.Trigger(lambda: Keymap.Climber.climbUp.value > 0.5).whileTrue(commands.climber.setClimberPosition(Robot.climber, position = config.Climber.climberSetPos))
commands2.button.Trigger(lambda: Keymap.Climber.climbDown.value > 0.5).whileTrue(commands.climber.setClimberPosition(Robot.climber, 0))
# manual code
#commands2.button.Trigger(lambda: Keymap.Climber.extendclimber.value > .05).whileTrue(commands.extendclimber(Robot.climber))
#commands2.button.Trigger(lambda: Keymap.Climber.retractclimber.value > .05).whileTrue(commands.retractclimber(Robot.climber))


Keymap.Shooter.setupShooter.whileTrue(commands.shooter.Shoot(Robot.shooter))
Keymap.Intake.intakeIn.whileTrue(commands.intake.IntakeIn(Robot.intake))
Keymap.Intake.intakeOut.whileTrue(commands.intake.IntakeOut(Robot.intake))
Keymap.Intake.intakeRetract.whileTrue(commands.intake.IntakeRetract(Robot.intake))
