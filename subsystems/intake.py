import commands2
import config
from phoenix6 import hardware, controls, configs, StatusCode
from wpilib import DriverStation, SmartDashboard, Mechanism2d, MechanismLigament2d
from ntcore import NetworkTableInstance

class Intake(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        self.m_intakeMotor = hardware.TalonFX(63)
        self.m_intakeExtension = hardware.TalonFX(66)


        # Intake Example Section
        #Creat 2d Mechanism for visualization of simulation
        self.mech = Mechanism2d(3,3)
        self.root = self.mech.getRoot("Intake",1.5,0)
        self.intake = self.root.appendLigament("intake", config.Intake.MinLength,90)
        SmartDashboard.putData("Mech2d", self.mech)

        # Elvator Magic Motion and talon definition
        self.motion_magic = controls.MotionMagicVoltage(0)
        
        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_intakeExtension.configurator.apply(config.Intake.cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        #Output for logging
        self._inst = NetworkTableInstance.getDefault()
        self._table = self._inst.getTable("Intake")
        self._field1_pub = self._table.getDoubleTopic("Current Position").publish()
        self._field2_pub = self._table.getDoubleTopic("Current Setpoint").publish()

    def setIntakePosition(self,position:float):
        #print("Set Intake Position")
        self.m_intakeExtension.set_control(self.motion_magic.with_position(position).with_slot(0))

    def stopIntakeExtension(self):
        self.m_intakeExtension.set(0)    

    def getIntakeDSOutput(self):
        current_rot = self.m_intakeExtension.get_position().value_as_double
        self._field1_pub.set(current_rot)
        self._field2_pub.set(self.motion_magic.position)
        self.intake.setLength(config.Intake.MinLength + (current_rot * config.Intake.Rot_to_Dist))
        SmartDashboard.putNumber("Intake Motor Value", self.m_intakeMotor.get())

    def intakeMotorOut(self):
        self.m_intakeMotor.set(1)
        #print("intake out")

    def intakeMotorIn(self):
        self.m_intakeMotor.set(-1)  
        #print("intake in")     

    def intakeMotorOff(self):
        self.m_intakeMotor.set(0)        
    





