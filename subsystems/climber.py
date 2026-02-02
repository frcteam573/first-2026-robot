import commands2
import config
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
        self.talonfx = self.getTalon()
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

    def setClimberPosition(self,position:float):
        if config.Climber.climberMode:
            print("Set climber Position")
            self.talonfx.set_control(self.motion_magic.with_position(position).with_slot(0))


    def stopClimber(self):
        self.talonfx.set(0)

    def extendClimber(self):
        
        if config.Climber.climberMode:
         self.talonfx.set(1.0)

    def retractClimber(self):
        
        if config.Climber.climberMode:
         self.talonfx.set(-1.0)
    

    def getClimberPosition(self):
        return self.talonfx.get_position().value_as_double

    def getTalon(self) -> hardware.TalonFX:
        self.talonfx = hardware.TalonFX(10, "canivore")
        return self.talonfx
    
    def getClimberDSOutput(self):
        current_rot = self.talonfx.get_position().value_as_double
        self._field1_pub.set(current_rot)
        self._field2_pub.set(self.motion_magic.position)
        self.Climber.setLength(config.Climber.MinLength + (current_rot * config.Climber.Rot_to_Dist))
