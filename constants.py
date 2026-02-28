import math

from wpimath.geometry import Pose3d, Rotation3d, Transform3d, Pose2d, Translation2d, Rotation2d, Translation3d
from pathplannerlib.auto import PathConstraints

blueAllianceZoneThreshold = 4.75
redAllianceZoneThreshold = 11.9

inches_to_meters = 0.0254
#----------------------------- Camera Locations ---------------------------
Robot_To_Camera1 = Transform3d(
    Translation3d(
       -10*inches_to_meters, 8.625*inches_to_meters, 10.5*inches_to_meters  # X  # Y  # Z
    ),
        Rotation3d(0.0, 0.0, math.radians(90)),  # Roll  # Pitch  # Yaw
    )

Robot_To_Camera2 = Transform3d(
    Translation3d(
       11*inches_to_meters, 8.625*inches_to_meters, 10.75*inches_to_meters  # X  # Y  # Z
    ),
        Rotation3d(0.0, 0.0, math.radians(-90)),  # Roll  # Pitch  # Yaw
    )

# Robot_To_Camera3 = Transform3d(
#     Translation3d(
#        0*inches_to_meters, -7*inches_to_meters, 24*inches_to_meters  # X  # Y  # Z
#     ),
#         Rotation3d(math.radians(0), math.radians(-1*(90-56)), math.radians(180-15)),  # Roll  # Pitch  # Yaw
#     )

# ---------------------------------------------------------

#Drivetrain Constants
class DrivetrainConstants:
    MaxVelocity = 4.5 #meters per second
    MaxAcceleration = 3 #meters per second squared
    MaxAngularVelocity = math.pi #radians per second
    MaxAngularAcceleration = math.pi #radians per second squared

    constraints = PathConstraints(MaxVelocity,MaxAcceleration,MaxAngularVelocity,MaxAngularAcceleration)

class HPStations:

    #Offeset from wall at HP for robot to stop at
    HPOffset = 0.01 # in meters
    # HP Positions
    blue_right_HP = Pose2d(0.851, 0.654, Rotation2d((54 * math.pi) / 180))
    postOffset_BlueR_HP = Pose2d(blue_right_HP.X() + math.cos(blue_right_HP.rotation().radians()) * HPOffset, blue_right_HP.Y() + math.sin(blue_right_HP.rotation().radians()), blue_right_HP.rotation())
    blue_left_HP =  Pose2d(0.851, 7.404, Rotation2d((306 * math.pi) / 180))
    postOffset_BlueL_HP = Pose2d(blue_left_HP.X() + math.cos(blue_left_HP.rotation().radians()) * HPOffset, blue_left_HP.Y() + math.sin(blue_left_HP.rotation().radians()), blue_left_HP.rotation())
    red_right_HP = Pose2d(16.711, 7.404, Rotation2d((234 * math.pi) / 180))
    PostOffset_RedR_HP = Pose2d(red_right_HP.X() + math.cos(red_right_HP.rotation().radians()) * HPOffset, red_right_HP.Y() + math.sin(red_right_HP.rotation().radians()), red_right_HP.rotation())
    red_left_HP = Pose2d(16.711, 0.654, Rotation2d((126 * math.pi) / 180))
    PostOffset_RedL_HP = Pose2d(red_left_HP.X() + math.cos(red_right_HP.rotation().radians()) * HPOffset, red_left_HP.Y() + math.sin(red_left_HP.rotation().radians()), red_left_HP.rotation())

    humanPlayersPos = [
        postOffset_BlueL_HP, postOffset_BlueR_HP, PostOffset_RedR_HP, PostOffset_RedL_HP
]

class HubPositions:
    BlueHubPos = Pose2d(inches_to_meters*(182.11), inches_to_meters*(158.84), Rotation2d(math.radians(0))) #april tag 18

    RedHubPos = Pose2d(Translation2d(inches_to_meters*(469.11), inches_to_meters*(158.84)), Rotation2d(math.radians(0))) #april tag 7

##### only hub postiions are current field, all other measurements are from last year
class PassingPositions:
    BluePassingPos1 = Pose2d(2.6, 5.4, Rotation2d(math.radians(0))) #april tag 18
    BluePassingPos2 = Pose2d(2.5, 2, Rotation2d(math.radians(0))) #april tag 18
    
    BluePassingPos = [
        BluePassingPos1, BluePassingPos2
    ]

    RedPassingPos1 = Pose2d(14.2, 2.3, Rotation2d(math.radians(0))) #april tag 7
    RedPassingPos2 = Pose2d(14.2, 6, Rotation2d(math.radians(0))) #april tag 7

    #blue1: 2.6, 5.4
    #blue2: 2.5, 2
    #red1: 14.2, 2.3
    #red2: 14.2, 6

    RedPassingPos = [
        RedPassingPos1, RedPassingPos2
    ]
    

class ClimbingPositions:
   BlueClimbPos = Pose2d(inches_to_meters*(144.00), inches_to_meters*(158.50), Rotation2d(math.radians(0))) #april tag 18
        
   RedClimbPos = Pose2d(Translation2d(inches_to_meters*(546.87), inches_to_meters*(158.50)), Rotation2d(math.radians(0))) #april tag 7