import typing
import commands2
import wpilib

from oi.keymap import Keymap

# from commands.wrist import Wrist

from subsystems.intake import Intake 
import config

class IntakeIn(commands2.Command):
    #This command used to run shooter motor
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.app.intakeMotorIn()  
        self.app.setIntakePosition(config.Intake.MaxLength)  
        self.app.getIntakeDSOutput()
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()
        self.app.getIntakeDSOutput()

class IntakeOut(commands2.Command):
    #This command used to run shooter motor
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.app.intakeMotorOut()  
        self.app.setIntakePosition(config.Intake.MaxLength)  
        self.app.getIntakeDSOutput()
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()
        self.app.getIntakeDSOutput()



class IntakeRetract(commands2.Command):
    #This command used to run shooter motor
    def __init__(
        self, 
        app: Intake,
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        
    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.app.intakeMotorOff()  
        self.app.setIntakePosition(config.Intake.MinLength)  
        self.app.getIntakeDSOutput()
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()        
        self.app.getIntakeDSOutput()