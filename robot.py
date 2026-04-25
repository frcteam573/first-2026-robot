#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

from math import radians


import wpilib
import commands2
import typing
import wpiutil
import time

from oi.keymap import Keymap
from robotcontainer import RobotContainer, Robot
# from vision import vision_sim
# from vision.vision_estimator import VisionEstimator
from telemetry import Telemetry

from config import Cameras, Elevator
from wpimath.geometry import Pose2d, Rotation2d, Pose3d, Translation3d, Rotation3d,Quaternion

# import oi.oi
import subsystems
import config, constants
import ntcore
from questnav.questnav import QuestNav

from wpilib import DataLogManager, DriverStation, SmartDashboard
import utils.utils as utilities



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

    # photonVisionMethod = config.PhotonVisionSetting.REAL_CAMERA

    localizationMethod = config.PrimaryLocalization.QUESTNAV

    def robotInit(self) -> None:
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        self.container = RobotContainer()

        #Setting default pose
        self.container.drivetrain.reset_pose(Pose2d(0,0,Rotation2d(0)))

        self.questnav = QuestNav()  #Initialize QuestNav
        # SmartDashboard.putNumber("Shooter / TEST Distance", 0)

        self.questnav_missed_frame_count = 0
        self.questnav_dtap_count = 0
        self.questnav_dtap_reset_limit = 14 #Allows for 0.2 s at 50 Hz
        self.questnav_non_track_count = 0
        self.questnav_non_track_count_limit = 100
        self.questnav_dis_count = 0
        wpilib.SmartDashboard.putBoolean("Occulus DTap Reset", False)
        wpilib.SmartDashboard.putBoolean("Occulus Tracking", False)
        wpilib.SmartDashboard.putBoolean("Occulus Connected", False)
        wpilib.SmartDashboard.putBoolean("Occulus Use Default Pos", False)

        #Initialize the items to send vision and questnav pose to dashboard
        self.questnav_field = wpilib.Field2d()
        # self.photonvision_field = wpilib.Field2d()
        wpilib.SmartDashboard.putData('QuestNavField',self.questnav_field)
        # wpilib.SmartDashboard.putData('PhotonVisionField',self.photonvision_field)
        self.resetQuestNavPoseforAutoStart()
        self.container.shooter.hoodOff()
        

        # oi.oi.OI.map_controls() #Map controls
        self.time_start = time.time()
        self.wpilogger = DataLogManager.start()
        DriverStation.startDataLog(DataLogManager.getLog())
        self.container.intake.intakeMotorOff()

        #For TESTING
        SmartDashboard.putNumber("Shooter / TEST Wheel Speed", 0)
        SmartDashboard.putNumber("Shooter / TEST Hood Pos", 0)
        SmartDashboard.putNumber("Shooter / Shooter Trim Value", 0)
        SmartDashboard.putBoolean("Oculus Disconnected", False)
        self.logDelay = 0

        # if wpilib.RobotBase.isSimulation(): #Only run is in SIM
        #     self.simulationInit()

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

        utilities.calculate_alignment(robotPose=config.RobotPoseConfig.pose, targetPose=utilities.getTargetPose(config.RobotPoseConfig.pose))
        config.inZone = self.container.shooter.inScoringZone(config.RobotPoseConfig.pose)
        # #Run QuestNav command every loop
        self.questnav.command_periodic()

        self.container.led.ModeManager() #Update LED mode based on conditions
        # #Only run during SIM
        # if wpilib.RobotBase.isSimulation():
            
        #     self.simulationPeriodic()

        # Add measurements to localization based on primary source
        # if self.localizationMethod == config.PrimaryLocalization.VISION:
        #     self.add_vision_to_pose_esitmate()
        # elif self.localizationMethod == config.PrimaryLocalization.QUESTNAV:
            
        self.add_questnav_to_pose_estimate()
        # #     pass
        # # else:
        # #     pass

        config.RobotPoseConfig.pose = self.container.drivetrain.get_state().pose
        
        # # subsystems.Elevator.getElevatorDSOutput(Robot.elevator)
        # # subsystems.Shooter.getMotors(self=Robot.shooter)

        if self.logDelay == 3:
            subsystems.Shooter.getShooterInfo(self.container.shooter)
            subsystems.Intake.getIntakeInfo(self.container.intake)
            # # subsystems.Climber.getClimberInfo(self.container.climber)
            # #Deployed values
            self.logDelay = 0
            # robotToOculus = config.RobotPoseConfig.pose.relativeTo(self.questnav_field.getRobotPose())
            # oculusErrorDistance = ((robotToOculus.X()**2 + robotToOculus.Y()**2)**0.5)
            
            # SmartDashboard.putBoolean("Robot/Oculus Aligned ", oculusErrorDistance >= 1)
        else:
            self.logDelay += 1


        commands2.CommandScheduler.getInstance().run()

    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""
        pass

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""
        
        # self.vision_est = self.container._vision_est.get_estimated_robot_pose()
        # if self.vision_est:
        #     self.photonvision_field.setRobotPose(self.vision_est[0])
        # else:
        #     self.photonvision_pose = None
        # self.resetPoseBasedOnVision() # Resets pose of QuestNav and robot based on Vision Only

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.alliance = wpilib.DriverStation.getAlliance() #Get Alliance color from DS
        config.Alliance.blue_team = wpilib.DriverStation.Alliance.kBlue == self.alliance #Set a config value to this color used in automous selection 
        config.Shooter.trim = SmartDashboard.getNumber("Shooter / Shooter Trim Value", 0)
        self.autonomousCommand = self.container.getAutonomousCommand()

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

        self.container.shooter.resetHoodZero()
        self.resetQuestNavPoseforAutoStart()

    def autonomousPeriodic(self) -> None:
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
        # self.container.shooter.resetHoodZero()
        self.trimCounter = 0
        # self.resetQuestNavPoseforAutoStart() #TEMP

    def teleopPeriodic(self) -> None:
        """This function is called periodically during operator control"""

        if commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.START) and commands2.button.JoystickButton(Controllers.DRIVER_CONTROLLER, controllerDRIVER.SELECT):
            #Reset questnav pose if its really messed up, only if both start and select are pressed to avoid accidental resets
            self.resetQuestNavPoseforEmergency()
        #  print("TEST")
        
        if Keymap.Shooter.trimFar.getAsBoolean():
            if self.trimCounter == 0:
                config.Shooter.trim += 1
                SmartDashboard.putNumber("Shooter / Shooter Trim Value", config.Shooter.trim)
            self.trimCounter += 1
            if self.trimCounter > 10:
                self.trimCounter = 0
        elif Keymap.Shooter.trimClose.getAsBoolean():
            if self.trimCounter == 0:
                config.Shooter.trim -= 1
                SmartDashboard.putNumber("Shooter / Shooter Trim Value", config.Shooter.trim)
            self.trimCounter += 1
            if self.trimCounter > 10:
                self.trimCounter = 0
        else: self.trimCounter = 0

    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()
    
    # def simulationInit(self) -> None:
    #     if self.photonVisionMethod == config.PhotonVisionSetting.SIM:
    #         pass
    #     #   self.visionSim = vision_sim.photonvision_sim_setup() #Setup sim vision system
    
    # def simulationPeriodic(self) -> None:
    #     try:
    #         self.visionSim.update(self.container.drivetrain.get_state().pose)
            
    #     except:
    #         pass
            
    # def add_vision_to_pose_esitmate(self):
    #     if self.vision_est is not None:
    #         self.container.drivetrain.add_vision_measurement(self.vision_est[0],self.vision_est[1])

    def add_questnav_to_pose_estimate(self):
        # get new pose frames
        # print("QuestNav1")
        connected = self.questnav.is_connected()
        wpilib.SmartDashboard.putBoolean("Occulus Tracking", self.questnav.is_tracking())
        wpilib.SmartDashboard.putBoolean("Occulus Connected", connected)
        dis_cout_inc = False
        
        frames = self.questnav.get_all_unread_pose_frames()

        # print(frames) #See what it does when paused
        if not frames: 
            SmartDashboard.putBoolean("Oculus Disconnected", True)
            # print("No Frames")
            dis_cout_inc = True
            if not connected:
                self.questnav_dtap_count += 1

                if self.questnav_dtap_count > self.questnav_dtap_reset_limit:
                    wpilib.SmartDashboard.putBoolean("Occulus DTap Reset", True)
                    self.questnav_dtap_count = 0
                    self.questnav_missed_frame_count += 1 


        else:
            for frame in frames:
                self.questnav_dtap_count = 0
                wpilib.SmartDashboard.putBoolean("Occulus DTap Reset", False)
                # print("QuestNav2")
                if self.questnav.is_connected() and self.questnav.is_tracking():
                    # Add to pose estimator
                    self.questnav_non_track_count = 0
                    self.questnav_dis_count = 0
                    SmartDashboard.putBoolean("Oculus Disconnected", False)
                    wpilib.SmartDashboard.putBoolean("Occulus Use Default Pos", False)
                    #print("QN Pose:",frame.quest_pose_3d.toPose2d())
                    # print("QuestNav3")
                    #print("Timestamp:", frame.data_timestamp - self.time_start)
                    quest_pose = frame.quest_pose_3d.toPose2d()
                    newPose = quest_pose.transformBy((constants.Robot_To_Quest2D.inverse()))
                    self.questnav_field.setRobotPose(newPose)
                    # print("QuestNavPose", newPose)
                    custom_std_devs = tuple([0.01, 0.01, 0.02]) # TUNE SMALL NUMBERS MEAN MORE TRUST IN QuestNav
                    # print(frame.data_timestamp- self.time_start)

                    if newPose is not None:
                        # print("QN4")
                        self.container.drivetrain.reset_pose(newPose)

                    # self.container.drivetrain.add_vision_measurement(
                    #     newPose,
                    #     frame.data_timestamp- self.time_start,
                    #     custom_std_devs) # Standard deviations
                else:
                    self.questnav_non_track_count += 0
                    if self.questnav_non_track_count > self.questnav_non_track_count_limit:
                        SmartDashboard.putBoolean("Oculus Disconnected", True)
                        dis_cout_inc = True

        if dis_cout_inc:
            # print(self.questnav_dis_count)
            self.questnav_dis_count += 1
        
        if self.questnav_dis_count > 20:
            wpilib.SmartDashboard.putBoolean("Occulus Use Default Pos", True)
    # def resetPoseBasedOnVision(self):
    #     vision_est = self.container._vision_est.get_estimated_robot_pose()
    #     if vision_est is not None:
    #         self.container.drivetrain.reset_pose(vision_est[0])
    #         self.questnav.set_pose(Pose3d(vision_est[0]))
    #         self.questnav_field.setRobotPose(Pose3d(vision_est[0]).toPose2d())

    def resetQuestNavPoseforAutoStart(self):
        current_pose = self.container.drivetrain.get_state().pose

        questNavpose = current_pose.transformBy(constants.Robot_To_Quest2D)

        self.questnav.set_pose(Pose3d(questNavpose))
        self.questnav_field.setRobotPose(questNavpose)

    def resetQuestNavPoseforEmergency(self):

        #Find pose location 
        pose_to_use = Pose2d(0,0,Rotation2d(0))
        if config.Alliance.blue_team:
            pose_to_use = Pose2d(3.53,4.050,Rotation2d(0))
        else:
            pose_to_use = Pose2d(12.99,4.050,Rotation2d(radians(180)))

        current_pose = pose_to_use

        questNavpose = current_pose.transformBy(constants.Robot_To_Quest2D)

        self.questnav.set_pose(Pose3d(questNavpose))
        self.container.drivetrain.reset_pose(current_pose)
        self.questnav_field.setRobotPose(questNavpose)



