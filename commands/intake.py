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
        self.app.setIntakePosition(config.Intake.MaxRot)  
        # print('intake ran in')
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()

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
        self.app.setIntakePosition(config.Intake.MaxRot)  
        # print('intake ran out')
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()

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
        self.app.setIntakePosition(config.Intake.MinRot)  
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()

class testIntakeRoller(commands2.Command):
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
        
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()

class testIntakeExtensionOut(commands2.Command):
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
        self.app.intakeExtOut()
        
    def end(self, interrupted=False) -> None:
        self.app.stopIntakeExtension()

class testIntakeExtensionIn(commands2.Command):
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
        self.app.intakeExtIn()
        
    def end(self, interrupted=False) -> None:
        self.app.stopIntakeExtension()