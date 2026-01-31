import typing
import commands2
import wpilib
import utils.utils
from oi.keymap import Keymap
import config

# from commands.wrist import Wrist

from subsystems.shooter import Shooter 

class Shoot(commands2.Command):
    #This command used to run shooter motor
    def __init__(
        self, 
        app: Shooter, 
        shootOut: bool = False,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        self.shootOut = shootOut
        
    def initialize(self) -> None:
        pass


    def execute(self) -> None:
        wheelSpeed, hoodAngle = self.app.calcTarget(config.RobotPoseConfig.pose, utils.utils.getTargetPose(config.RobotPoseConfig.pose))
        self.app.setHoodAngle(hoodAngle)
        self.app.setShooterSpeed(wheelSpeed)
        if Keymap.Shooter.shoot.getAsBoolean() or self.shootOut:
            self.app.hopperMotorOn()
        else:
            self.app.hopperMotorOff()    
        
        
    def end(self, interrupted=False) -> None:
        self.app.shooterMotorOff()
        self.app.hoodMotorOff()
        self.app.hopperMotorOff() 



