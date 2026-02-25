from math import fabs

import commands2
from commands import intake
import config
import phoenix6
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance

from subsystems.intake import Intake

class Climber(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        # climber Example Section
        #Creat 2d Mechanism for visualization of simulation
        self.mech = Mechanism2d(3,3)
        self.root = self.mech.getRoot("Climber",1.5,0)
        self.Climber = self.root.appendLigament("Climber", config.Climber.MinLength,90)
        SmartDashboard.putData("Mech2d", self.mech)

        # climber Magic Motion and talon definition
        # self.talonfx = self.getTalon()
        self.talonfx = hardware.TalonFX(64)
        self.motion_magic = controls.MotionMagicVoltage(0)
        
        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.talonfx.configurator.apply(config.Climber.cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        #Output for logging
        self._inst = NetworkTableInstance.getDefault()
        self._table = self._inst.getTable("Climber")
        self._field1_pub = self._table.getDoubleTopic("Current Position").publish()
        self._field2_pub = self._table.getDoubleTopic("Current Setpoint").publish()

    def setClimberPosition(self, position:float):
        if config.Climber.climberMode and config.Intake.Deployed == False:
            print("Set climber Position")
            config.Climber.Deployed = True
            self.talonfx.set_control(self.motion_magic.with_position(position).with_slot(0))
            SmartDashboard.putBoolean("Intake Deployed", config.Intake.Deployed)
            SmartDashboard.putBoolean("Climber Deployed", config.Climber.Deployed)
            SmartDashboard.putNumber("Climber / Actual Set Climber Position", position)
        elif config.Intake.Deployed == True:
            pass
            # print("UNDEPLOY INTAKE")
            # Intake.setIntakePosition(config.Intake.MinLength)
            # config.Intake.Deployed = False
            # self.talonfx.set_control(self.motion_magic.with_position(position).with_slot(0))
            # config.Climber.Deployed = True
            # SmartDashboard.putNumber("Climber / Actual Set Climber Position", position)
            # SmartDashboard.putBoolean("Intake Deployed", config.Intake.Deployed)
            # SmartDashboard.putBoolean("Climber Deployed", config.Climber.Deployed)


    def stopClimber(self):
        self.talonfx.set(0)

    def extendClimber(self):
        
        if config.Climber.climberMode and config.Climber.Deployed == False:
         self.talonfx.set(1.0)

    def retractClimber(self):
        
        if config.Climber.climberMode:
         self.talonfx.set(-1.0)

    def retractClimberToCertainPos(self, position: float):
        if config.Climber.climberMode:
            self.talonfx.set(position)
    

    def getClimberPosition(self):
        print(self.talonfx)
        return self.talonfx.get_position().value_as_double

    def getTalon(self) -> hardware.TalonFX:
        self.talonfx = hardware.TalonFX(64)
        return self.talonfx
    
    def getClimberDSOutput(self):
        current_rot = self.talonfx.get_position().value_as_double
        self._field1_pub.set(current_rot)
        self._field2_pub.set(self.motion_magic.position)
        self.Climber.setLength(config.Climber.MinLength + (current_rot * config.Climber.Rot_to_Dist))
        
    def getMotorOutputStatus(self):
        climberPosition = self.talonfx.get_position().value_as_double
        SmartDashboard.putNumber("Climber / Actual climber Position", climberPosition)
        return self.talonfx.get_motor_output_status(True)
       
        
       # current_rot = self.talonfx.get_position().value_as_double
       # self._field1_pub.set(current_rot)
       # self._field2_pub.set(self.motion_magic.position)
       # self.Climber.setLength(config.Climber.MinLength + (current_rot * config.Climber.Rot_to_Dist))

       # shooterWheelSpeed = self.m_shooter1.get_velocity().value_as_double
       # shooterWheelSpeed2 = self.m_shooter2.get_velocity().value_as_double
       # hoodAngle = self.m_hoodMotor1.get_position().value_as_double/config.Shooter.hoodRotationsToAngle
       # hopperSpeed = self.m_hopperMotor.get_velocity().value_as_double
       # SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed", shooterWheelSpeed)
       # SmartDashboard.putNumber("Shooter / Actual Shooter Wheel Speed 2", shooterWheelSpeed2)
       # SmartDashboard.putNumber("Shooter / Actual Hood Angle", hoodAngle)
       # SmartDashboard.putNumber("Shooter / Actual Hopper Speed", hopperSpeed)
       # SmartDashboard.putNumber("Shooter / Hopper Motor Command", self.m_hopperMotor.get())
