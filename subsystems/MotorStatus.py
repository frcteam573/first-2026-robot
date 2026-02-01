from subsystems.shooter import Shooter
from subsystems.climber import Climber
from subsystems.command_swerve_drivetrain import CommandSwerveDrivetrain
from subsystems.elevator import Elevator
from subsystems.intake import Intake
import robot

import phoenix6, math, commands2, wpilib
from phoenix6 import SignalLogger, status_code, StatusCode

class MotorStatus(commands2.SubsystemBase):
#motorCollection = phoenix6.StatusSignalCollection()
  motorStatusCollection = [] # This is the basic table of all motor status colletion, it remains empty until the function below is called.
  motorTemps = []

  def getAllMotorStatus(self):
    def __init__(self):
        super().__init__()

        self.shooter = robot.subsystems.Shooter
        self.swerve = CommandSwerveDrivetrain()
        self.elevator = Elevator()
        self.climber = Climber()
        self.intake = Intake()

        self.motorStatusCollection = []
        self.motorTemps = []
        
        
    self.motorStatusCollection = [
        robot.subsystems.Shooter.getMotors(),
        # CommandSwerveDrivetrain.getMotors(),
        # Elevator.getTalon(),
        # Climber.getTalon(),
        # Intake.getMotors()
    ]
    for motor in self.motorStatusCollection:
        signal = motor.get_device_temp()
        self.motorTemps.append(signal)
        # get the device temperature as a failsafe, this is a status that is always being refreshed and posted.
      # Because it is always being posted, we can remove any chance of an error occuring since we cant get the status of a dead motor.
    print(self.motorTemps)
