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
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        self.finished = False

    def execute(self) -> None:
        self.finished = False
        shooterSettings = self.app.calcTarget(config.RobotPose.pose, utils.utils.getTargetPose(config.RobotPose.pose))
        self.app.setHoodAngle(shooterSettings[1])
        self.app.setShooterSpeed(shooterSettings[0])
        if Keymap.Shooter.shoot.getAsBoolean():
            self.app.hopperMotorOn()
        else:
            self.app.hopperMotorOff()    
        
    def end(self, interrupted=False) -> None:
        self.app.shooterMotorOff()
        self.app.hoodMotorOff()
        self.app.hopperMotorOff() 



