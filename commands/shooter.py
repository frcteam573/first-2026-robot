import typing
import commands2
import wpilib
import utils.utils
from oi.keymap import Keymap
import config
from wpilib import SmartDashboard

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
        SmartDashboard.putBoolean("Shooter / Hood at Position", self.app.setHoodAngle(hoodAngle))
        SmartDashboard.putBoolean("Shooter / Wheel at Speed", self.app.setShooterSpeed(wheelSpeed))
        if Keymap.Shooter.shoot.getAsBoolean() or self.shootOut:
            if wpilib.SmartDashboard.getBoolean("Aligned", False):
                self.app.hopperMotorOff()
                print('Aligned And Shot')
            else:
                print('Not Aligned')
                self.app.hopperMotorOn()
        else:
            self.app.hopperMotorOff()    
        
    def end(self, interrupted=False) -> None:
        self.app.shooterMotorOff()
        self.app.hoodMotorOff()
        self.app.hopperMotorOff() 
        SmartDashboard.putBoolean("Shooter / Hood at Position", False)
        SmartDashboard.putBoolean("Shooter / Wheel at Speed", False)