import typing
import commands2
import wpilib

from oi.keymap import Keymap

# from commands.wrist import Wrist

from subsystems.climber import Climber 

class setClimberPosition(commands2.Command):
      def __init__(
        # This defines what subsystem this command is for, so it can be used in the command scheduler.
        self, 
        app: Climber,
        position: 0,
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
        self.position = position

      def execute(self):
        self.app.setClimberPosition(self.position)

      def isFinished(self):
         if abs(Climber.getClimberPosition(self.app) - self.position) < .5:
            return True
        
      def end(self, interrupted=False) -> None:
        #This is run when the command is finished.
        #Stops climber motors when the command is finished.
        self.app.stopClimber()

class extendclimber(commands2.Command):
      def __init__(
        # This defines what subsystem this command is for, so it can be used in the command scheduler.
        self, 
        app: Climber,
        #position: 0,
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
       # self.position = position

      def execute(self):
        self.app.extendClimber()
        
    #  def isFinished(self):
          
        
      def end(self, interrupted=False) -> None:
        #This is run when the command is finished.
        #Stops climber motors when the command is finished.
        self.app.stopClimber()

class retractclimber(commands2.Command):
      def __init__(
        # This defines what subsystem this command is for, so it can be used in the command scheduler.
        self, 
        app: Climber,
        # position: 0,
    ) -> None:
        super().__init__()
        
        self.app = app
        self.addRequirements(app)
    #    self.position = position

      def execute(self):
        self.app.retractClimber()
        
     # def isFinished(self):
           
        
      def end(self, interrupted=False) -> None:
        #This is run when the command is finished.
        #Stops climber motors when the command is finished.
        self.app.stopClimber()