from wpimath.geometry import Pose2d, Quaternion, Rotation2d, Translation2d
from wpilib import RobotController
from ntcore import NetworkTableInstance

class QuestNav:
    def __init__(self):
        # Configure Network Tables topics (questnav/...) to communicate with the Quest HMD
        nt4_instance = NetworkTableInstance.getDefault()
        nt4_table = nt4_instance.getTable("questnav")
        self.quest_miso = nt4_table.getIntegerTopic("miso").subscribe(0)
        self.quest_mosi = nt4_table.getIntegerTopic("mosi").publish()

        # Subscribe to the Network Tables questnav data topics
        self.quest_timestamp = nt4_table.getDoubleTopic("timestamp").subscribe(0.0)
        self.quest_position = nt4_table.getFloatArrayTopic("position").subscribe([0.0, 0.0, 0.0])
        self.quest_quaternion = nt4_table.getFloatArrayTopic("quaternion").subscribe([0.0, 0.0, 0.0, 0.0])
        self.quest_euler_angles = nt4_table.getFloatArrayTopic("eulerAngles").subscribe([0.0, 0.0, 0.0])
        self.quest_battery_percent = nt4_table.getDoubleTopic("batteryPercent").subscribe(0.0)

        # Local heading helper variables
        self.yaw_offset = 0.0
        self.reset_position = Pose2d()

    def get_pose(self) -> Pose2d:

        return Pose2d(self.get_questnav_pose().relativeTo(self.reset_position).translation(), Rotation2d.fromDegrees(self.get_oculus_yaw()))

    def get_battery_percent(self) -> float:
        return self.quest_battery_percent.get()

    def connected(self) -> bool:
        return ((RobotController.getFPGATime() - self.quest_battery_percent.getLastChange()) / 1000) < 250

    def get_quaternion(self) -> Quaternion:
        qq_floats = self.quest_quaternion.get()
        return Quaternion(qq_floats[0], qq_floats[1], qq_floats[2], qq_floats[3])

    def timestamp(self) -> float:
        return self.quest_timestamp.get()

    def zero_heading(self) -> None:
        euler_angles = self.quest_euler_angles.get()
        self.yaw_offset = euler_angles[1]

    def zero_position(self) -> None:
        self.reset_position = self.get_pose()
        if self.quest_miso.get() != 99:
            self.quest_mosi.set(1)

    def cleanup_questnav_messages(self) -> None:
        if self.quest_miso.get() == 99:
            self.quest_mosi.set(0)

    def get_oculus_yaw(self) -> float:
        euler_angles = self.quest_euler_angles.get()
        ret = euler_angles[1] - self.yaw_offset
        ret %= 360
        if ret < 0:
            ret += 360
        return ret

    def get_questnav_translation(self) -> Translation2d:
        questnav_position = self.quest_position.get()
        return Translation2d(questnav_position[2], -questnav_position[0])

    def get_questnav_pose(self) -> Pose2d:
        oculus_position_compensated = self.get_questnav_translation() - Translation2d(0, 0.1651)
        return Pose2d(oculus_position_compensated, Rotation2d.fromDegrees(self.get_oculus_yaw()))