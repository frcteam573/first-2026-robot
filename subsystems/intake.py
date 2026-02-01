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

################ lines 17-53 (and the rest) copied from shooter code, made some changes -tyler ######################################################

        # # Be able to switch which control request to use based on a button press
        # # Start at velocity 0, use slot 0
        self.velocity_voltage = controls.VelocityVoltage(0).with_slot(0)
        # Start at velocity 0, use slot 1
        self.velocity_torque = controls.VelocityTorqueCurrentFOC(0).with_slot(1)
        # Keep a neutral out so we can disable the motor
        self.brake = controls.NeutralOut()

        cfg = configs.TalonFXConfiguration()
        
        # Voltage-based velocity requires a velocity feed forward to account for the back-emf of the motor
        cfg.slot0.k_s = 0.1 # To account for friction, add 0.1 V of static feedforward
        cfg.slot0.k_v = 0.12 # Kraken X60 is a 500 kV motor, 500 rpm per V = 8.333 rps per V, 1/8.33 = 0.12 volts / rotation per second
        cfg.slot0.k_p = 0.11 # An error of 1 rotation per second results in 2V output
        cfg.slot0.k_i = 0 # No output for integrated error
        cfg.slot0.k_d = 0 # No output for error derivative
        # Peak output of 8 volts
        cfg.voltage.peak_forward_voltage = 8
        cfg.voltage.peak_reverse_voltage = -8

        # Torque-based velocity does not require a velocity feed forward, as torque will accelerate the rotor up to the desired velocity by itself
        cfg.slot1.k_s = 2.5 # To account for friction, add 2.5 A of static feedforward
        cfg.slot1.k_p = 5 # An error of 1 rotation per second results in 5 A output
        cfg.slot1.k_i = 0 # No output for integrated error
        cfg.slot1.k_d = 0 # No output for error derivative
        # Peak output of 40 A
        cfg.torque_current.peak_forward_torque_current = 40
        cfg.torque_current.peak_reverse_torque_current = -40

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_intakeMotor.configurator.apply(cfg) 
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        ################### add self.m_intakeExtension to above #############################

        #self.talonfx = hardware.TalonFX(0, self.canbus)
       # self.talonfx_foll

       #################### remove???? below is only hood motor stuff i think ####################################

        # Be able to switch which control request to use based on a button press
        # Start at position 0, use slot 0
        self.position_voltage = controls.PositionVoltage(0).with_slot(0)
        # Start at position 0, use slot 1
        self.position_torque = controls.PositionTorqueCurrentFOC(0).with_slot(1)
        # Keep a brake request so we can disable the motor
        self.brake = controls.NeutralOut()

        cfg = configs.TalonFXConfiguration()
        cfg.slot0.k_p = 2.4; # An error of 1 rotation results in 2.4 V output
        cfg.slot0.k_i = 0; # No output for integrated error
        cfg.slot0.k_d = 0.1; # A velocity of 1 rps results in 0.1 V output
        # Peak output of 8 V
        cfg.voltage.peak_forward_voltage = 8
        cfg.voltage.peak_reverse_voltage = -8

        cfg.slot1.k_p = 60; # An error of 1 rotation results in 60 A output
        cfg.slot1.k_i = 0; # No output for integrated error
        cfg.slot1.k_d = 6; # A velocity of 1 rps results in 6 A output
        # Peak output of 120 A
        cfg.torque_current.peak_forward_torque_current = 120
        cfg.torque_current.peak_reverse_torque_current = -120

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.m_hoodMotor1.configurator.apply(cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

        # Make sure we start at 0
        self.m_intakeExtension.set_position(0)  #### intake extension???
        
    def getMotors(self):
        return [self.m_intakeExtension, self.m_intakeMotor]