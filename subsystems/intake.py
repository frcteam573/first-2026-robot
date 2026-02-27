import commands2
import config
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance

import subsystems
import subsystems.climber

# from subsystems.climber import Climber

class Intake(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        self.m_intakeMotor = hardware.TalonFX(53)
        self.m_intakeExtension = hardware.TalonFX(56)

        # Intake Example Section

        # Elvator Magic Motion and talon definition
        self.motion_magic = controls.MotionMagicVoltage(0)
        
        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_intakeExtension.configurator.apply(config.Intake.cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

    def setIntakePosition(self, position:float):
        #print("Set Intake Position")
        if config.Climber.Deployed == False:
            if self.m_intakeExtension.get_position().value_as_double > config.Intake.deploy_threshold:
                config.Intake.Deployed = True
            else:
                config.Intake.Deployed = False
            self.m_intakeExtension.set_control(self.motion_magic.with_position(position).with_slot(0))
            
    def stopIntakeExtension(self):
        self.m_intakeExtension.set(0)    

    def intakeMotorOut(self):
        self.m_intakeMotor.set(1)
        #print("intake out")

    def intakeMotorIn(self):
        self.m_intakeMotor.set(-1)  
        #print("intake in")     

    def intakeMotorOff(self):
        self.m_intakeMotor.set(0)        

    def getIntakeInfo(self):
        '''Gets intake info.

        Output:
            A list consisting of intake motor value and intake extension position.

        # Make sure we start at 0
        self.m_intakeExtension.set_position(0)  #### intake extension???
        

        '''
        intakeWheelSpeed = self.m_intakeMotor.get_velocity().value_as_double
        intakeExtension = self.m_intakeExtension.get_position().value_as_double
        intakeExtensionSetpoint = self.motion_magic.position
        SmartDashboard.putNumber("Intake / Actual Intake Motor Value", intakeWheelSpeed)
        SmartDashboard.putNumber("Intake / Actual Intake Extension Position", intakeExtension)
        SmartDashboard.putNumber("Intake / Commanded Intake Extension Position", intakeExtensionSetpoint)
        SmartDashboard.putBoolean("Deploy State / Intake Deployed", config.Intake.Deployed)

    def getMotors(self):
        return [self.m_intakeExtension, self.m_intakeMotor]
