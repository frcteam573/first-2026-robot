from math import fabs

import commands2

import config
import phoenix6
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance



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
        self.m_climber = hardware.TalonFX(54)
        self.motion_magic = controls.MotionMagicVoltage(0)
        
        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_climber.configurator.apply(config.Climber.cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

    def setClimberPosition(self, position:float):
        if config.Climber.climberMode and config.Intake.Deployed == False:
            # print("Set climber Position")
            if self.m_climber.get_position().value_as_double > config.Climber.deploy_threshold:
                config.Climber.Deployed = True
            else:
                config.Climber.Deployed = False
            self.m_climber.set_control(self.motion_magic.with_position(position).with_slot(0))

    def stopClimber(self):
        self.m_climber.set(0)

    def extendClimber(self):
        
        if config.Climber.climberMode and config.Climber.Deployed == False:
         self.m_climber.set(0.5)

    def retractClimber(self):
        
        if config.Climber.climberMode:
         self.m_climber.set(-0.5)

    def retractClimberToCertainPos(self, position: float):
        if config.Climber.climberMode:
            self.m_climber.set(position)
    
    def getClimberPosition(self):
        # print(self.m_climber)
        return self.m_climber.get_position().value_as_double

    def getClimberInfo(self):
        try:

            current_rot = self.m_climber.get_position().value_as_double
            SmartDashboard.putNumber("Climber / Actual Position", current_rot)
            SmartDashboard.putNumber("Climber / Setpoint Position", self.motion_magic.position)
            SmartDashboard.putBoolean("Deploy State / Climber Deployed", config.Climber.Deployed)
            SmartDashboard.putBoolean("Climber / Climber Mode", config.Climber.climberMode)
            self.Climber.setLength(config.Climber.MinLength + (current_rot * config.Climber.Rot_to_Dist))
        except:
            pass
