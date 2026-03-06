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







class intakegeneral(commands2.Command):
    def __init__(
        self, 
        app: Intake,
        intakeIn: int = 1,
        autolower: bool = False
    ) -> None:
        super().__init__()

        self.app = app
        self.addRequirements(app)
        self.intakeIn = intakeIn
        self.autolower = autolower
        
    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        if self.intakeIn == 1:
            self.app.intakeMotorIn()
        elif self.intakeIn == 0:
            self.app.intakeMotorOut()
        else:
            self.app.intakeMotorOff()

        if Keymap.Intake.testextin.getAsBoolean():
            self.app.intakeExtIn()
        elif Keymap.Intake.testextout.getAsBoolean() or self.autolower:
            self.app.intakeExtOut()
        else:
            self.app.stopIntakeExtension()
                
    def end(self, interrupted=False) -> None:
        self.app.intakeMotorOff()
        self.app.stopIntakeExtension()

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

class testIntakeRollerRev(commands2.Command):
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