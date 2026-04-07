from re import S
from signal import Signals

import commands2
from numpy import double
import wpilib
# from commands import shooter
import config
import utils.utils as Tyler
from phoenix6 import CANBus, hardware, controls, configs, StatusCode, signals
from wpilib import AnalogInput, DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance
from wpimath.geometry import Rotation2d, Pose2d
import constants

class Shooter(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
    
        # self.m_shooter = rev.SparkMax(58, rev.SparkMax.MotorType.kBrushless)
        self.m_shooter1 = hardware.TalonFX(60,CANBus("573CANivore"))
        self.m_shooter2 = hardware.TalonFX(61,CANBus("573CANivore"))  
        self.m_hoodMotor1 = hardware.TalonFX(55,CANBus("573CANivore"))

        #Set soft limits for hood motor
        hoodcfg = configs.SoftwareLimitSwitchConfigs()
        hoodcfg.forward_soft_limit_threshold = config.Shooter.hoodmaxRot
        hoodcfg.reverse_soft_limit_threshold = config.Shooter.hoodminRot
        hoodcfg.forward_soft_limit_enable = True
        hoodcfg.reverse_soft_limit_enable = True
        
        
        print("Applying hood configs...")
        print("Hood Config Set Code:", self.m_hoodMotor1.configurator.apply(hoodcfg))

        # self.s_hoodServo1 = wpilib.Servo(6) #change to match id of servo
        # self.s_hoodServo2 = wpilib.Servo(7) #change to match id of servo
        # self.s_hoodSensor1 = AnalogInput(2)
        # self.s_hoodSensor2 = AnalogInput(3)

        self.m_hopperMotor = hardware.TalonFX(58,CANBus("573CANivore"))
        self.m_shooterFeedMotor = hardware.TalonFX(59,CANBus("573CANivore"))
        
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
        cfg.slot0.k_p = 0.15 # An error of 1 rotation per second results in 2V output
        cfg.slot0.k_i = 0 # No output for integrated error
        cfg.slot0.k_d = 0.02 # No output for error derivative
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
        # self.m_hoodMotor1.setNeutralMode(neutralMode=signals.NeutralModeValue.BRAKE)
       
        # Keep a brake request so we can disable the motor
        self.brake = controls.StaticBrake()

        cfg1 = configs.TalonFXConfiguration()
        cfg1.motor_output.inverted = signals.InvertedValue.CLOCKWISE_POSITIVE
        cfg1.motor_output.neutral_mode = signals.NeutralModeValue.BRAKE
        
        cfg1.slot0.k_p = 5; # An error of 1 rotation results in 2.4 V output
        cfg1.slot0.k_i = 0; # No output for integrated error
        cfg1.slot0.k_d = 0; # A velocity of 1 rps results in 0.1 V output
        cfg1.slot0.k_s = 0.00
        cfg1.slot0.k_v = 0.0
        # Peak output of 8 V
        cfg1.voltage.peak_forward_voltage = 8
        cfg1.voltage.peak_reverse_voltage = -8
        

        cfg1.slot1.k_p = 60; # An error of 1 rotation results in 60 A output
        cfg1.slot1.k_i = 0; # No output for integrated error
        cfg1.slot1.k_d = 6; # A velocity of 1 rps results in 6 A output
        # Peak output of 120 A
        cfg1.torque_current.peak_forward_torque_current = 40
        cfg1.torque_current.peak_reverse_torque_current = -40

        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_hoodMotor1.configurator.apply(cfg1)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")
        
        self.m_hoodMotor1.set(0)
        #self.s_hoodServo1.setPosition(0)
        #self.s_hoodServo2.setPosition(0)

    def setShooterSpeed(self, speed: float) -> bool:
        '''Sets the speed of the shooter motors based on supplied speed.
        
        Args:
            speed: The desired speed of the wheels in RPS.
        '''
        
        self.m_shooter1.set_control(self.velocity_voltage.with_velocity(speed))
        SmartDashboard.putNumber("Shooter / Shooter Wheel Speed Command", speed)
        # print("Shooter out Speed:", speed)
        return Tyler.max_min_check(self.m_shooter1.get_velocity().value_as_double, speed, config.Shooter.wheelSpeedShooterTolerance)
        
    def setShooterBasic(self, speed: float):
        self.m_shooter1.set(speed)

    def shooterMotorOff(self):
        self.m_shooter1.set(0)
        SmartDashboard.putNumber("Shooter / Shooter Wheel Speed Command", 0)

    def hoodOff(self):
        self.m_hoodMotor1.set(0)

    def hoodUp(self):
        self.m_hoodMotor1.set(.15)

    def hoodDown(self):
        self.m_hoodMotor1.set(-.15)

    def hoodreset(self):
        self.m_hoodMotor1.set_control(self.position_voltage.with_position(0))
        SmartDashboard.putNumber("Shooter / Shooter Hood Angle Command", 0)

    def setHoodAngle(self, angleIn: float) -> bool:
        # print("Setting Hood to:", angleIn)
        self.m_hoodMotor1.set_control(self.position_voltage.with_position(angleIn))
        SmartDashboard.putNumber("Shooter / Hood Output", self.m_hoodMotor1.get())
        SmartDashboard.putNumber("Shooter / Shooter Hood Angle Command", angleIn)
        



        # print("Shooter out Speed:", angleIn)
        return Tyler.max_min_check(self.m_hoodMotor1.get_position().value_as_double, angleIn, config.Shooter.hoodAngleTolerance)
        

    def inScoringZone(self,pose: Pose2d) -> bool:
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
        
        Distance = (Distance/.0254) # convert to inches
        Distance = Distance + (config.Shooter.trim * 12)
        # Distance = SmartDashboard.getNumber("Shooter / TEST Distance", 0)
        SmartDashboard.putNumber("Shooter / Calculated Shooter Distance", Distance)

        shooterHoodAngle = 0 # Needs to be updated with actual formula, this is just a placeholder
        if SmartDashboard.getBoolean("Occulus Disconnected", False):
            shooterHoodAngle = 0  # Hardcode hood angle and wheel speed if oculus is disconnected, this is just a failsafe and should be tuned to something that works well for most of the field
            shooterWheelSpeed = 0 #UPDATED THESE
        elif config.inZone:
            shooterHoodAngle = 0 # needs to be updated with actual formula, this is just a placeholder
            shooterWheelSpeed = 0

            if Distance < 51:
                shooterHoodAngle = 4.7
                shooterWheelSpeed = 47
            elif Distance < 161:
                shooterWheelSpeed = -0.00129*(Distance**2) + 0.40431*Distance + 32.52545
                shooterHoodAngle = 0.00000958*(Distance**2) + 0.04021995*Distance + 2.68452440
            elif Distance < 207:
                Distance = Distance 
                shooterWheelSpeed = 0.2391*Distance + 25.5000
                shooterHoodAngle = 0.0428*Distance + 2.6050
            else:
                shooterWheelSpeed = 75
                shooterHoodAngle = 11.5
            
            # if Distance < 78.5:
            #     shooterWheelSpeed = 47
            #     shooterHoodAngle = (0.141818182 * Distance) - 4.652727273
            # elif Distance < 119:
            #     shooterWheelSpeed = (0.44444444 * Distance) + 12.111111
            #     shooterHoodAngle = (0.02617284 * Distance) + 4.425432099
            # elif Distance < 180.5:
            #     Distance = Distance - 24
            #     shooterWheelSpeed = (0.162602 * Distance) + 45.65041
            #     shooterHoodAngle = (0.036097561 * Distance) + 3.244390244
            # elif Distance < 207:
            #     Distance = Distance - 24
            #     shooterWheelSpeed = 75
            #     shooterHoodAngle = (0.064528302 * Distance) - 1.887358491
            # else:
            #     shooterWheelSpeed = 75
            #     shooterHoodAngle = 11.5

        else:
            if Distance < 238:
                shooterWheelSpeed = 55
                shooterHoodAngle = 10.7
            elif Distance < 267:
                shooterWheelSpeed = 55
                shooterHoodAngle = (0.087586 * Distance) - 10.1455
            elif Distance < 319:
                shooterWheelSpeed = (0.384615 * Distance) - 47
                shooterHoodAngle = 13.24
            else:
                shooterWheelSpeed = 75
                shooterHoodAngle = 13.24
                

        
        if shooterWheelSpeed < 0:
            shooterWheelSpeed = 0
        if shooterHoodAngle < 0:
            shooterHoodAngle = 0
        if shooterHoodAngle > 13.5:
            shooterHoodAngle = 13.5
        if shooterWheelSpeed > 75:
            shooterWheelSpeed = 75

        SmartDashboard.putNumber("Shooter / Calculated Wheel Speed", shooterWheelSpeed)
        SmartDashboard.putNumber("Shooter / Calculated Angle", shooterHoodAngle)
        return shooterWheelSpeed, shooterHoodAngle

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
            # shooterWheelSpeed2 = self.m_shooter2.get_velocity().value_as_double
            hoodAngle = self.m_hoodMotor1.get_position().value_as_double
            # hoodAngle = self.m_hoodMotor1.get_position().value_as_double/config.Shooter.hoodRotationsToAngle
            # hopperSpeed = self.m_hopperMotor.get_velocity().value_as_double

            SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed", shooterWheelSpeed)
            # SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed 2", shooterWheelSpeed2)

            # SmartDashboard.putNumber("Shooter / Commanded Hood Angle", self.m_hoodMotor1.get_position().value_as_double)
            SmartDashboard.putNumber("Shooter / Actual Hood Angle", hoodAngle)
            
        except:
            pass

    def resetHoodZero(self):
        self.m_hoodMotor1.set_position(0)