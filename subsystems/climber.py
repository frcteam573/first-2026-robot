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
        self.root = self.mech.getRoot("climber",1.5,0)
        self.elevator = self.root.appendLigament("climber", config.climber.MinLength,90)
        SmartDashboard.putData("Mech2d", self.mech)

        # climber Magic Motion and talon definition
        self.talonfx = self.getTalon()
        self.motion_magic = controls.MotionMagicVoltage(0)
        
        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.talonfx.configurator.apply(config.climber.cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        #Output for logging
        self._inst = NetworkTableInstance.getDefault()
        self._table = self._inst.getTable("climber")
        self._field1_pub = self._table.getDoubleTopic("Current Position").publish()
        self._field2_pub = self._table.getDoubleTopic("Current Setpoint").publish()

    def setclimberPosition(self,position:float):
        #print("Set climber Position")
        self.talonfx.set_control(self.motion_magic.with_position(position).with_slot(0))

    def stopclimber(self):
        self.talonfx.set(0)
    
    def getclimberPosition(self):
        return self.talonfx.get_position().value_as_double

    def getTalon(self) -> hardware.TalonFX:
        self.talonfx = hardware.TalonFX(10, "canivore")
        return self.talonfx
    
    def getclimberDSOutput(self):
        current_rot = self.talonfx.get_position().value_as_double
        self._field1_pub.set(current_rot)
        self._field2_pub.set(self.motion_magic.position)
        self.climber.setLength(config.Elevator.MinLength + (current_rot * config.climber.Rot_to_Dist))