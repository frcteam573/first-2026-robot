#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import commands2
import commands2.cmd
from commands2.button import CommandXboxController, Trigger
from commands2.sysid import SysIdRoutine

from generated.tuner_constants import TunerConstants
# from telemetry import Telemetry

from pathplannerlib.auto import AutoBuilder, NamedCommands, RobotConfig, PathConstraints
from pathplannerlib.events import EventTrigger
from phoenix6 import swerve
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from wpimath.geometry import Rotation2d, Pose2d
from wpimath.units import rotationsToRadians
from phoenix6 import hardware, controls, configs, StatusCode

import config
from ntcore import NetworkTableInstance
import subsystems
import commands.climber
import commands.drivetrain
import commands.shooter
import commands.intake
## import commands.climber
import constants
import subsystems.command_swerve_drivetrain
import utils.utils as utilities
from oi.keymap import Controllers, Keymap


class Robot:
    # Defines all subsystems used in the robot, these are used to access the subsystems in commands and other files.
    # elevator = subsystems.Elevator()
    # climber = subsystems.Climber()
    # shooter = subsystems.Shooter()
    # # # MotorStatus = subsystems.MotorStatus()
    # intake = subsystems.Intake()
    pass

class RobotContainer:
    """
    This class is where the bulk of the robot should be declared. Since Command-based is a
    "declarative" paradigm, very little robot logic should actually be handled in the :class:`.Robot`
    periodic methods (other than the scheduler calls). Instead, the structure of the robot (including
    subsystems, commands, and button mappings) should be declared here.
    """

    def __init__(self) -> None:
        self._max_speed = (
            1.0 * TunerConstants.speed_at_12_volts
        )  # speed_at_12_volts desired top speed
        self._max_angular_rate = rotationsToRadians(
            0.75
        )  # 3/4 of a rotation per second max angular velocity

        # Setting up bindings for necessary control of the swerve drive platform
        self._drive = (
            swerve.requests.FieldCentric()
            .with_deadband(self._max_speed * 0.1)
            .with_rotational_deadband(
                self._max_angular_rate * 0.1
            )  # Add a 10% deadband
            .with_drive_request_type(
                swerve.SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            )  # Use open-loop control for drive motors
        )
        self._brake = swerve.requests.SwerveDriveBrake()
        self._point = swerve.requests.PointWheelsAt()

        # self._logger = Telemetry(self._max_speed)

        self._joystick = CommandXboxController(0)

        self.drivetrain = TunerConstants.create_drivetrain()
        # self._elevator = subsystems.Elevator()
        # self.climber = subsystems.Climber()
        self.shooter = subsystems.Shooter()
        self.intake = subsystems.Intake()
        
        #Name Commands for Autos these must be done before building the autobuilder

        # NamedCommands.registerCommand("Intake In", commands.intake.IntakeIn(Robot.intake))
        # NamedCommands.registerCommand("Intake Out", commands.intake.IntakeOut(Robot.intake))
        # NamedCommands.registerCommand("Intake Retract", commands.intake.IntakeRetract(Robot.intake))
        # NamedCommands.registerCommand("Shoot Prep", commands.shooter.Shoot(Robot.shooter))
        # NamedCommands.registerCommand("Shoot Out", commands.shooter.Shoot(Robot.shooter, shootOut=True))

        
        
        # # NamedCommands.registerCommand("Climber Extend", commands.climber.extendClimber(Robot.climber))
        # NamedCommands.registerCommand("climbUp", commands.elevator.setPosition(self._elevator,position=10))
        # NamedCommands.registerCommand("climbDown", commands.elevator.setPosition(self._elevator,position=0))

        # Auto builder
        try:
            self._auto_chooser = AutoBuilder.buildAutoChooser("test auton")
            SmartDashboard.putData("Choreo", self._auto_chooser)
        except Exception as e:
            print(f"Error building auto chooser: {e}")

        self._vision_est = config.Cameras.vision_controller

        # Configure the button bindings
        self.configureButtonBindings()

    def configureButtonBindings(self) -> None:
        """
        Use this method to define your button->command mappings. Buttons can be created by
        instantiating a :GenericHID or one of its subclasses (Joystick or XboxController),
        and then passing it to a JoystickButton.
        """

        # Note that X is defined as forward according to WPILib convention,
        # and Y is defined as to the left according to WPILib convention.
        self.drivetrain.setDefaultCommand(
            # Drivetrain will execute this command periodically
            self.drivetrain.apply_request(
                lambda: (
                    self._drive.with_velocity_x(
                        -self._joystick.getLeftY() * self._max_speed * .3
                    )  # Drive forward with negative Y (forward)
                    .with_velocity_y(
                        -self._joystick.getLeftX() * self._max_speed * .3
                    )  # Drive left with negative X (left)
                    .with_rotational_rate(
                        -self._joystick.getRightX() * self._max_angular_rate 
                    )  # Drive counterclockwise with negative X (left)
                )
            )
        )

        # Idle while the robot is disabled. This ensures the configured
        # neutral mode is applied to the drive motors while disabled.
        idle = swerve.requests.Idle()
        Trigger(DriverStation.isDisabled).whileTrue(
            self.drivetrain.apply_request(lambda: idle).ignoringDisable(True)
        )
        self._joystick.y().whileTrue(self.drivetrain.apply_request(
                lambda: (
                    self._drive.with_velocity_x(
                        -self._joystick.getLeftY() * self._max_speed * .3
                    )  # Drive forward with negative Y (forward)
                    .with_velocity_y(
                        -self._joystick.getLeftX() * self._max_speed *.3
                    )  # Drive left with negative X (left)
                    .with_rotational_rate(
                        subsystems.CommandSwerveDrivetrain.calculate_relative_angle(self=self.drivetrain, robotPose=config.RobotPoseConfig.pose, targetPose=utilities.getTargetPose(config.RobotPoseConfig.pose)) * self._max_angular_rate 
                    )  # Drive counterclockwise with negative X (left)
                )
            )) 
        self._joystick.x().whileTrue(self.drivetrain.apply_request(
                lambda: (
                    self._drive.with_velocity_x(
                        -self._joystick.getLeftY() * self._max_speed
                    )  # Drive forward with negative Y (forward)
                    .with_velocity_y(
                        -self._joystick.getLeftX() * self._max_speed
                    )  # Drive left with negative X (left)
                    .with_rotational_rate(
                        -self._joystick.getRightX() * self._max_angular_rate
                    )  # Drive counterclockwise with negative X (left)
                )
            )) 
        # self._joystick.x().whileTrue(commands.drive_to_nearest_reef_pos(self.drivetrain, left=True))
        # self._joystick.b().whileTrue(commands.drive_to_nearest_reef_pos(self.drivetrain, left=False))

        # self._joystick.pov(0).whileTrue(
        #     self.drivetrain.apply_request(
        #         lambda: self._forward_straight.with_velocity_x(0.5).with_velocity_y(0)
        #     )
        # )
        # self._joystick.pov(180).whileTrue(
        #     self.drivetrain.apply_request(
        #         lambda: self._forward_straight.with_velocity_x(-0.5).with_velocity_y(0)
        #     )
        # )

        # Run SysId routines when holding back/start and X/Y.
        # Note that each routine should be run exactly once in a single log.
        (self._joystick.back() & self._joystick.y()).whileTrue(
            self.drivetrain.sys_id_dynamic(SysIdRoutine.Direction.kForward)
        )
        (self._joystick.back() & self._joystick.x()).whileTrue(
            self.drivetrain.sys_id_dynamic(SysIdRoutine.Direction.kReverse)
        )
        (self._joystick.start() & self._joystick.y()).whileTrue(
            self.drivetrain.sys_id_quasistatic(SysIdRoutine.Direction.kForward)
        )
        (self._joystick.start() & self._joystick.x()).whileTrue(
            self.drivetrain.sys_id_quasistatic(SysIdRoutine.Direction.kReverse)
        )

        # reset the field-centric heading on left bumper press
        #self._joystick.leftBumper().onTrue(
        #    self.drivetrain.runOnce(lambda: self.drivetrain.seed_field_centric())
        #)

        # self.drivetrain.register_telemetry(
        #     lambda state: self._logger.telemeterize(state)
        # )

        #Appendage Controls
        Keymap.Shooter.setupShooter.whileTrue(commands.shooter.testComponents(self.shooter))
        # Keymap.Shooter.setupShooter.whileTrue(commands.shooter.Shoot(self.shooter))
        # Keymap.Shooter.hopperMotorReverse.whileTrue(commands.shooter.testHopper(self.shooter))
        # Keymap.Intake.intakeIn.whileTrue(commands.intake.IntakeIn(self.intake))
        # Keymap.Intake.intakeOut.whileTrue(commands.intake.IntakeOut(self.intake))
        # Keymap.Intake.intakeRetract.whileTrue(commands.intake.IntakeRetract(self.intake))

        Keymap.Intake.testextout.whileTrue(commands.intake.testIntakeExtensionOut(self.intake))
        Keymap.Intake.testextin.whileTrue(commands.intake.testIntakeExtensionIn(self.intake))
        Keymap.Intake.testroller.whileTrue(commands.intake.testIntakeRoller(self.intake))

        # commands2.button.Trigger(lambda: Keymap.Climber.climbUp.value > 0.5).whileTrue(commands.climber.extendclimber(self.climber))
        # commands2.button.Trigger(lambda: Keymap.Climber.climbDown.value > 0.5).whileTrue(commands.climber.retractclimber(self.climber))

        # commands2.button.Trigger(lambda: Keymap.Climber.climbUp.value > 0.5).whileTrue(commands.climber.setClimberPosition(Robot.climber, position = config.Climber.climberSetPos))
        # commands2.button.Trigger(lambda: Keymap.Climber.climbDown.value > 0.5).whileTrue(commands.climber.setClimberPosition(Robot.climber, 0))

    def getAutonomousCommand(self) -> commands2.Command:
        """Use this to pass the autonomous command to the main {@link Robot} class.

        :returns: the command to run in autonomous
        """
        return self._auto_chooser.getSelected()
