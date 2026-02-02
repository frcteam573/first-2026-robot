import typing
import commands2
import wpilib

from oi.keymap import Keymap
from pathplannerlib.path import PathPlannerPath, PathConstraints, GoalEndState
from wpimath.geometry import Pose2d, Rotation2d
import math
from pathplannerlib.auto import AutoBuilder, RobotConfig
import constants,config

# from commands.wrist import Wrist

from subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain    

class drive_to_nearest_HP_station(commands2.Command):
      def __init__(
        # This defines what subsystem this command is for, so it can be used in the command scheduler.
        self, 
        app: CommandSwerveDrivetrain,
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
    
      def initialize(self) -> None:
        self.nearest = self.app.get_state().pose.nearest(constants.HPStations.humanPlayersPos)
        
      def execute(self):
        AutoBuilder.pathfindToPose(self.nearest,constants.DrivetrainConstants.constraints).schedule()

      def end(self, interrupted=False) -> None:
        #This is run when the command is finished.
        #Stops elevator motors when the command is finished.
        pass
      
class drive_to_nearest_reef_pos(commands2.Command):
      def __init__(
        # This defines what subsystem this command is for, so it can be used in the command scheduler.
        self, 
        app: CommandSwerveDrivetrain,
        left: bool = True
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
        self.left = left
    
      def initialize(self) -> None:
        self.nearest = self.app.get_state().pose.nearest(constants.ReefPositions.BlueReef.BlueReefList if config.Alliance.blue_team else constants.ReefPositions.RedReef.RedReefList)

      def execute(self):
        AutoBuilder.pathfindToPose(self.nearest,constants.DrivetrainConstants.constraints).until(self.isFinished).schedule()

      def isFinished(self) -> bool:
        compare_poses = self.nearest.relativeTo(self.app.get_state().pose)
        if abs(compare_poses.X()) < config.ReefAlign.allowable_errorX and abs(compare_poses.Y()) < config.ReefAlign.allowable_errorY and abs(compare_poses.rotation().degrees()) < config.ReefAlign.allowable_errorR:
           wpilib.SmartDashboard.putBoolean("Reef Align", True)
           return True
        else:
           wpilib.SmartDashboard.putBoolean("Reef Align", False)
           return False
           
      def end(self, interrupted=False) -> None:
        #This is run when the command is finished.
        #Stops elevator motors when the command is finished.
        pass