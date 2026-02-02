#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
import commands2
import typing
import wpiutil
import time

from robotcontainer import RobotContainer, Robot
from vision import vision_sim
from vision.vision_estimator import VisionEstimator
from telemetry import Telemetry

from config import Cameras, Elevator
from wpimath.geometry import Pose2d, Rotation2d, Pose3d

import oi.oi
import subsystems
import config, constants
import ntcore
from questnav.questnav import QuestNav

from wpilib import DataLogManager, DriverStation



from utils.oi import (
    JoystickAxis,
    XBoxController,
)


controllerDRIVER = XBoxController
controllerOPERATOR = XBoxController
class Controllers:
    DRIVER = 0
    OPERATOR = 1

    DRIVER_CONTROLLER = wpilib.Joystick(0)
    OPERATOR_CONTROLLER = wpilib.Joystick(1)

class MyRobot(commands2.TimedCommandRobot):
    """
    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """
    autonomousCommand: typing.Optional[commands2.Command] = None

    photonVisionMethod = config.PhotonVisionSetting.REAL_CAMERA

    localizationMethod = config.PrimaryLocalization.VISION

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()

        #Setting default pose
        self.container.drivetrain.reset_pose(Pose2d(2,2,Rotation2d(0)))

        self.questnav = QuestNav()  #Initialize QuestNav

        #Initialize the items to send vision and questnav pose to dashboard
        self.questnav_field = wpilib.Field2d()
        self.photonvision_field = wpilib.Field2d()
        wpilib.SmartDashboard.putData('QuestNavField',self.questnav_field)
        wpilib.SmartDashboard.putData('PhotonVisionField',self.photonvision_field)

        oi.oi.OI.map_controls() #Map controls
        self.time_start = time.time()
        self.wpilogger = DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        if wpilib.RobotBase.isSimulation(): #Only run is in SIM
            self.simulationInit()

    def robotPeriodic(self) -> None:
        """This function is called every 20 ms, no matter the mode. Use this for items like diagnostics
        that you want ran during disabled, autonomous, teleoperated and test.

        This runs after the mode specific periodic functions, but before LiveWindow and
        SmartDashboard integrated updating."""

        # Runs the Scheduler.  This is responsible for polling buttons, adding newly-scheduled
        # commands, running already-scheduled commands, removing finished or interrupted commands,
        # and running subsystem periodic() methods.  This must be called from the robot's periodic
        # block in order for anything in the Command-based framework to work.

        #Run camera update and questNav update every loop
        self.vision_est = self.container._vision_est.get_estimated_robot_pose()
        if self.vision_est:
            self.photonvision_field.setRobotPose(self.vision_est[0])
        else:
            self.photonvision_pose = None

        #Run QuestNav command every loop
        self.questnav.command_periodic()

        #Only run during SIM
        if wpilib.RobotBase.isSimulation():
            
            self.simulationPeriodic()

        #Add measurements to localization based on primary source
        if self.localizationMethod == config.PrimaryLocalization.VISION:
            self.add_vision_to_pose_esitmate()
        elif self.localizationMethod == config.PrimaryLocalization.QUESTNAV:
            self.add_questnav_to_pose_estimate()
        else:
            pass

        config.RobotPoseConfig.pose = self.container.drivetrain.get_state().pose
        
        subsystems.Elevator.getElevatorDSOutput(Robot.elevator)
        subsystems.Shooter.getMotors(self=Robot.shooter)
        subsystems.Shooter.getShooterInfo(Robot.shooter)
        subsystems.Intake.getIntakeInfo(Robot.intake)
        commands2.CommandScheduler.getInstance().run()
        subsystems.Climber.getClimberDSOutput(Robot.climber)
    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        self.resetPoseBasedOnVision() # Resets pose of QuestNav and robot based on Vision Only

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.alliance = wpilib.DriverStation.getAlliance() #Get Alliance color from DS
        config.Alliance.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance #Set a config value to this color used in automous selection 
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""


        pass

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        self.alliance = wpilib.DriverStation.getAlliance() #Get Alliance color from DS
        config.Alliance.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance #Set a config value to this color used in automous selection
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""
        if commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.START) and commands2.button.JoystickButton(Controllers.OPERATOR_CONTROLLER, controllerDRIVER.SELECT):
         config.Climber.climberMode = True
         print("TEST")
                 
        pass

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
    
    def simulationInit(self) -> None:
        if self.photonVisionMethod == config.PhotonVisionSetting.SIM:
            self.visionSim = vision_sim.photonvision_sim_setup() #Setup sim vision system
    
    def simulationPeriodic(self) -> None:
        try:
            self.visionSim.update(self.container.drivetrain.get_state().pose)
            
        except:
            pass
            
    def add_vision_to_pose_esitmate(self):
        if self.vision_est is not None:
            self.container.drivetrain.add_vision_measurement(self.vision_est[0],self.vision_est[1])

    def add_questnav_to_pose_estimate(self):
        # get new pose frames
        frames = self.questnav.get_all_unread_pose_frames()
        for frame in frames:
            if self.questnav.is_connected(): #and self.questnav.is_tracking():
                # Add to pose estimator
                #print("QN Pose:",frame.quest_pose_3d.toPose2d())
                
                #print("Timestamp:", frame.data_timestamp - self.time_start)
                self.questnav_field.setRobotPose(frame.quest_pose_3d.toPose2d())
                self.container.drivetrain.add_vision_measurement(
                    frame.quest_pose_3d.toPose2d(),
                    frame.data_timestamp- self.time_start) # Standard deviations

        # current_pose = self.container.drivetrain.get_state().pose
        # vision_ests = self.container._vision_est.get_estimated_robot_pose(current_pose)
        # if vision_ests is not None:
        #     for vision_est in vision_ests:
        #         esti_pose = vision_est[0]
        #         if esti_pose is not None:
        #             relative = esti_pose.relativeTo(current_pose)
        #             dist = (relative.X()**2 + relative.Y()**2)**(1/2)
        #             if  dist < 0.5:
        #                 self.container.drivetrain.add_vision_measurement(vision_est[0],vision_est[1],vision_est[2])
        #                 #print(vision_est[2])
        #                 #print("Odo Pose: ", self.container.drivetrain.get_state().pose, "Vision Est Pose", vision_est[0])
        
    def resetPoseBasedOnVision(self):
        vision_est = self.container._vision_est.get_estimated_robot_pose()
        if vision_est is not None:
            self.container.drivetrain.reset_pose(vision_est[0])
            self.questnav.set_pose(Pose3d(vision_est[0]))



