import commands2
import config
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance

class Intake(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()