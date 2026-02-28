from re import S

import commands2
from numpy import double
import config
import utils.utils as Tyler
from phoenix6 import hardware, controls, configs, StatusCode, signals
from wpilib import AnalogInput, DriverStation, Servo, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance
from wpimath.geometry import Rotation2d, Pose2d
import constants

class Shooter(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
    
        # self.m_shooter = rev.SparkMax(58, rev.SparkMax.MotorType.kBrushless)
        self.m_shooter1 = hardware.TalonFX(60)
        self.m_shooter2 = hardware.TalonFX(61)  
        self.m_hoodMotor1 = hardware.TalonFX(55)

        self.s_hoodServo1 = Servo(0) #change to match id of servo
        self.s_hoodServo2 = Servo(1) #change to match id of servo
        self.s_hoodSensor1 = AnalogInput(0)
        self.s_hoodSensor2 = AnalogInput(1)

        self.m_hopperMotor = hardware.TalonFX(58)
        self.m_shooterFeedMotor = hardware.TalonFX(59)
        
        # # Be able to switch which control request to use based on a button press
        # # Start at velocity 0, use slot 0
        self.velocity_voltage = controls.VelocityVoltage(0).with_slot(0)
        # Start at velocity 0, use slot 1
        self.velocity_torque = controls.VelocityTorqueCurrentFOC(0).with_slot(1)
        # Keep a neutral out so we can disable the motor
        self.brake = controls.NeutralOut()

        cfg = configs.TalonFXConfiguration()
        
        # Voltage-based velocity requires a velocity feed forward to account for the back-emf of the motor
        cfg.slot0.k_s = 0.1 # To account for friction, add 0.1 V of static feedforward
        cfg.slot0.k_v = 0.12 # Kraken X60 is a 500 kV motor, 500 rpm per V = 8.333 rps per V, 1/8.33 = 0.12 volts / rotation per second
        cfg.slot0.k_p = 0.11 # An error of 1 rotation per second results in 2V output
        cfg.slot0.k_i = 0 # No output for integrated error
        cfg.slot0.k_d = 0 # No output for error derivative
        # Peak output of 8 volts
        cfg.voltage.peak_forward_voltage = 8
        cfg.voltage.peak_reverse_voltage = -8

        # Torque-based velocity does not require a velocity feed forward, as torque will accelerate the rotor up to the desired velocity by itself
        cfg.slot1.k_s = 2.5 # To account for friction, add 2.5 A of static feedforward
        cfg.slot1.k_p = 5 # An error of 1 rotation per second results in 5 A output
        cfg.slot1.k_i = 0 # No output for integrated error
        cfg.slot1.k_d = 0 # No output for error derivative
        # Peak output of 40 A
        cfg.torque_current.peak_forward_torque_current = 40
        cfg.torque_current.peak_reverse_torque_current = -40

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_shooter1.configurator.apply(cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        self.m_shooter2.set_control(controls.Follower(self.m_shooter1.device_id,signals.MotorAlignmentValue.OPPOSED))

        #self.talonfx = hardware.TalonFX(0, self.canbus)
    # self.talonfx_foll

    ##################

        # Be able to switch which control request to use based on a button press
        # Start at position 0, use slot 0
        self.position_voltage = controls.PositionVoltage(0).with_slot(0)
        # Start at position 0, use slot 1
        self.position_torque = controls.PositionTorqueCurrentFOC(0).with_slot(1)
        # Keep a brake request so we can disable the motor
        self.brake = controls.NeutralOut()

        cfg = configs.TalonFXConfiguration()
        cfg.slot0.k_p = 2.4; # An error of 1 rotation results in 2.4 V output
        cfg.slot0.k_i = 0; # No output for integrated error
        cfg.slot0.k_d = 0.1; # A velocity of 1 rps results in 0.1 V output
        # Peak output of 8 V
        cfg.voltage.peak_forward_voltage = 8
        cfg.voltage.peak_reverse_voltage = -8

        cfg.slot1.k_p = 60; # An error of 1 rotation results in 60 A output
        cfg.slot1.k_i = 0; # No output for integrated error
        cfg.slot1.k_d = 6; # A velocity of 1 rps results in 6 A output
        # Peak output of 120 A
        cfg.torque_current.peak_forward_torque_current = 120
        cfg.torque_current.peak_reverse_torque_current = -120

        # # Retry config apply up to 5 times, report if failure
        # status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        # for _ in range(0, 5):
        #     status = self.m_hoodMotor1.configurator.apply(cfg)
        #     if status.is_ok():
        #         break
        # if not status.is_ok():
        #     print(f"Could not apply configs, error code: {status.name}")

        # Make sure we start at 0
        self.s_hoodServo1.setPosition(0)
        self.s_hoodServo2.setPosition(0)

    def setShooterSpeed(self, speed: float) -> bool:
        '''Sets the speed of the shooter motors based on supplied speed.
        
        Args:
            speed: The desired speed of the wheels in RPS.
        '''
        
        self.m_shooter1.set_control(self.velocity_voltage.with_velocity(speed))
        SmartDashboard.putNumber("Shooter / Shooter Wheel Speed Command", speed)
        print("Shooter out Speed:", speed)
        return Tyler.max_min_check(self.m_shooter1.get_velocity().value_as_double, speed, config.Shooter.wheelSpeedShooterTolerance)
        
    def setShooterBasic(self, speed: float):
        self.m_shooter1.set(speed)

    def shooterMotorOff(self):
        self.m_shooter1.set(0)
        SmartDashboard.putNumber("Shooter / Shooter Wheel Speed Command", 0)

    def hoodVoltageToAngle(self, voltage) -> float:
        '''Converts voltage from hood sensor to angle in degrees.'''
        return 10*voltage - 40 # NEED TO BE CHANGED

    def setHoodAngle(self, angle: float) -> bool:
        '''Sets the angle of hood.
        
        Args:
            angle: The desired angle of the hood in degrees.
        '''
        #This sets the angle value
        self.s_hoodServo1.setAngle(angle * config.Shooter.hoodRotationsToAngle)
        self.s_hoodServo2.setAngle(angle * config.Shooter.hoodRotationsToAngle)

        #This checks if the hood is at the desired angle within a certain tolerance, and returns true if it is, false if it isnt

        angle1 = self.hoodVoltageToAngle(self.s_hoodSensor1.getVoltage())
        angle2 = self.hoodVoltageToAngle(self.s_hoodSensor2.getVoltage())

        if abs(angle1 - angle) < config.Shooter.hoodAngleTolerance and abs(angle2 - angle) < config.Shooter.hoodAngleTolerance:
           return True
        else:
           return False

        # return True

        # return Tyler.max_min_check(float(self.s_hoodServ.getPosition()) / config.Shooter.hoodRotationsToAngle, angle, config.Shooter.hoodAngleTolerance)




    def inScoringZone(pose: Pose2d) -> bool:
        '''changes hood angle when not in alliance's zone
        
        Args:
            pose: pose of the robot

        Output:
            True if in alliance zone, False if out

        '''
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            if pose.X() > constants.blueAllianceZoneThreshold: ## not in zone, passing mode
                return False
            else: ## in zone, shooting mode
                return True
        else: ##red alliance
            if pose.X() < constants.redAllianceZoneThreshold: ## not in zone, passing mode
                return False
            else: ## in zone, shooting mode
                return True

    def calcTarget(self, pose:Pose2d, goalPose:Pose2d):
        '''Calculates target based on pose and goal pose, returns wheel speed and hood angle.
    
        Args:
            pose: pose of the robot.
            goalPose: pose of the target.

        Output:
            a list consisting of wheel speed in RPS and angle in degrees.

        '''
        # wheel speed, hood angle, 
        IntermediatePose = pose.relativeTo(goalPose)
        Distance = (IntermediatePose.X()**2 + IntermediatePose.Y()**2)**.5  #pythagoream theorum
        SmartDashboard.putNumber("Shooter / Calculated Shooter Distance", Distance)
        shooterWheelSpeed = 1 * Distance ### FIX
        Angle = 1 * Distance ### FIX
        SmartDashboard.putNumber("Shooter / Calculated Wheel Speed", shooterWheelSpeed)
        SmartDashboard.putNumber("Shooter / Calculated Angle", Angle)
        return shooterWheelSpeed, Angle

    def hopperMotorOff(self):
        self.m_hopperMotor.set(0)
        self.m_shooterFeedMotor.set(0)

    def hopperMotorOn(self):
        self.m_hopperMotor.set(-1) 
        self.m_shooterFeedMotor.set(-1) 

    def hopperMotorReverse(self):
        # print("hopper motor reverse")
        self.m_hopperMotor.set(1)
        self.m_shooterFeedMotor.set(1)
        
    def getMotors(self):
        motors = (self.m_shooter1, self.m_shooter2, self.m_hopperMotor)
        self.motorTemps = []
        for motor in motors:
            signal = motor.get_device_temp().value_as_double
            self.motorTemps.append(signal)
            # get the device temperature as a failsafe, this is a status that is always being refreshed and posted.
        # Because it is always being posted, we can remove any chance of an error occuring since we cant get the status of a dead motor.
        # print(self.motorTemps)
        

    def getShooterInfo(self):
        '''Gets shooter info.

        Output:
            A list consisting of shooter wheel speed in RPS and hood angle in degrees.

        '''
        try:
            shooterWheelSpeed = self.m_shooter1.get_velocity().value_as_double
            shooterWheelSpeed2 = self.m_shooter2.get_velocity().value_as_double
            hood1Angle = self.hoodVoltageToAngle(self.s_hoodSensor1.getVoltage())
            hood2Angle = self.hoodVoltageToAngle(self.s_hoodSensor2.getVoltage())
            # hoodAngle = self.m_hoodMotor1.get_position().value_as_double/config.Shooter.hoodRotationsToAngle
            hopperSpeed = self.m_hopperMotor.get_velocity().value_as_double

            SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed", shooterWheelSpeed)
            SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed 2", shooterWheelSpeed2)

            SmartDashboard.putNumber("Shooter / Commanded Hood Angle 1", self.s_hoodServo1.getAngle())
            SmartDashboard.putNumber("Shooter / Actual Hood Angle 1", hood1Angle)
            
            SmartDashboard.putNumber("Shooter / Commanded Hood Angle 2", self.s_hoodServo2.getAngle())
            SmartDashboard.putNumber("Shooter / Actual Hood Angle 2", hood2Angle)
            SmartDashboard.putNumber("Shooter / Actual Hopper Speed", hopperSpeed)
            SmartDashboard.putNumber("Shooter / Hopper Motor Command", self.m_hopperMotor.get())
        except:
            pass