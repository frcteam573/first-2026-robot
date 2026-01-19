import typing
import commands2
import wpilib

from oi.keymap import Keymap

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
        self.app.shooterOn(1) #Intake setIntakeSpeed in subsystem is function to actually set the intake speed

    def isFinished(self) -> bool:
        return self.finished
        
    def end(self, interrupted=False) -> None:

        self.app.setShooterOffSpeed(0) #Intake setIntakeSpeed in subsystem is function to actually set the intake speed
