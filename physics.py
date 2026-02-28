import wpilib.simulation as sim
from wpilib import RobotController, DriverStation

from wpimath.system.plant import DCMotor, LinearSystemId
from wpimath.units import radiansToRotations
from phoenix6 import hardware

from pyfrc.physics.core import PhysicsInterface
from phoenix6 import unmanaged

import typing

if typing.TYPE_CHECKING:
    from robot import MyRobot

import subsystems.climber
import subsystems.climber

class PhysicsEngine:

    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        self.physics_controller = physics_controller

        # Climber SIM
        gearbox = DCMotor.krakenX60FOC(1)
        gearratio = 100
        self.motor_sim = sim.DCMotorSim(LinearSystemId.DCMotorSystem(gearbox, 0.01, gearratio), gearbox)
        # Keep a reference to the motor sim state so we can update it
        self.talon_sim = robot.container.climber.m_climber.sim_state

        # #Intake extension SIM
        # gearbox_intake_extension = DCMotor.krakenX44(1)
        # gearratio_intake_extension = 9*9*3
        # self.motor_sim_intake = sim.DCMotorSim(LinearSystemId.DCMotorSystem(gearbox_intake_extension, 0.01, gearratio_intake_extension), gearbox_intake_extension)
        # # Keep a reference to the motor sim state so we can update it
        # self.talon_sim_intake = robot.container.intake.m_intakeExtension.sim_state
        
        # #Intake motor SIM
        # gearbox_intake_motor = DCMotor.krakenX60(1)
        # gearratio_intake_motor = 1
        # self.motor_sim_intake_motor = sim.DCMotorSim(LinearSystemId.DCMotorSystem(gearbox_intake_motor, 0.01, gearratio_intake_motor), gearbox_intake_motor)
        # # Keep a reference to the motor sim state so we can update it
        # self.talon_sim_intake_motor = robot.container.intake.m_intakeMotor.sim_state

        # #Shooter motor Sim
        # gearbox_shooter = DCMotor.krakenX60(2)
        # gearratio_shooter = 1
        # self.motor_sim_shooter = sim.DCMotorSim(LinearSystemId.DCMotorSystem(gearbox_shooter, 0.01, gearratio_shooter), gearbox_shooter)
        # # Keep a reference to the motor sim state so we can update it
        # self.talon_sim_shooter = robot.container.shooter.m_shooter1.sim_state

    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """
        # If the driver station is enabled, then feed enable for phoenix devices
        if DriverStation.isEnabled():
            unmanaged.feed_enable(100)

        self.talon_sim.set_supply_voltage(RobotController.getBatteryVoltage())
        self.motor_sim.setInputVoltage(self.talon_sim.motor_voltage)
        self.motor_sim.update(tm_diff)
        self.talon_sim.set_raw_rotor_position(radiansToRotations(self.motor_sim.getAngularPosition()))
        self.talon_sim.set_rotor_velocity(radiansToRotations(self.motor_sim.getAngularVelocity()))

        # self.talon_sim_intake.set_supply_voltage(RobotController.getBatteryVoltage())
        # self.motor_sim_intake.setInputVoltage(self.talon_sim_intake.motor_voltage)
        # self.motor_sim_intake.update(tm_diff)
        # self.talon_sim_intake.set_raw_rotor_position(radiansToRotations(self.motor_sim_intake.getAngularPosition()))
        # self.talon_sim_intake.set_rotor_velocity(radiansToRotations(self.motor_sim_intake.getAngularVelocity()))

        # self.talon_sim_intake_motor.set_supply_voltage(RobotController.getBatteryVoltage())
        # self.motor_sim_intake_motor.setInputVoltage(self.talon_sim_intake_motor.motor_voltage)
        # self.motor_sim_intake_motor.update(tm_diff) 
        # self.talon_sim_intake_motor.set_raw_rotor_position(radiansToRotations(self.motor_sim_intake_motor.getAngularPosition()))
        # self.talon_sim_intake_motor.set_rotor_velocity(radiansToRotations(self.motor_sim_intake_motor.getAngularVelocity()))

        # self.talon_sim_shooter.set_supply_voltage(RobotController.getBatteryVoltage())
        # self.motor_sim_shooter.setInputVoltage(self.talon_sim_shooter.motor_voltage)
        # self.motor_sim_shooter.update(tm_diff)
        # self.talon_sim_shooter.set_raw_rotor_position(radiansToRotations(self.motor_sim_shooter.getAngularPosition()))
        # self.talon_sim_shooter.set_rotor_velocity(radiansToRotations(self.motor_sim_shooter.getAngularVelocity()))
