import commands2
import config
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance

class Shooter(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()
        
        self.m_shooter = rev.SparkMax(58, rev.SparkMax.MotorType.kBrushless)
              
    def setShooterOutSpeed(self, speed: float) -> bool:
        '''Sets the speed of the intake motors.
        
        Args:
            speed: The speed to set the motors to, -1 to 1.
        '''
        
        self.m_shooter.set(speed)
        #print("Shooter out Speed:", speed)

    def setShooterOutSpeed(self, speed: float) -> bool:
        #print("Shooter Out Speed:", speed)
        self.m_shooter.set(speed)
    
    def TeleopSetShooterOutSpeed(self, speed: float) -> bool:
        #print("Shooter Out Speed:", speed)
        if config.current_ele_pos > -2:
            self.m_shooter.set(speed * 0.5)
        else:
            self.m_shooter.set(speed)        