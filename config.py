#from vision.photon_camera import WrapperedPhotonCamera, PhotonVisionController
from vision.vision_estimator import VisionEstimator, PhotonCamera
import constants
from utils.utils import inches_to_meters
from phoenix6 import configs, controls
from wpimath.geometry import Pose2d, Rotation2d, Transform2d
from enum import Enum
from wpimath.geometry import Pose2d, Rotation2d, Transform2d, Translation2d
from wpimath.controller import PIDController


class PrimaryLocalization(Enum):
    ODO_Only = 0
    VISION = 1
    QUESTNAV = 2

class PhotonVisionSetting(Enum):
    REAL_CAMERA = 0
    SIM = 1
    
class Shooter:
    hoodRotationsToAngle = 6   ## number of rotations per degree in angle of hood ## NEEDS TO BE CHANGED 
    wheelSpeedShooterTolerance = 10 ##### +- tolerance value in RPS ### change number    
    hoodAngleTolerance = 12 ## change number


# ------------ Elevator Settings -----------------
class Elevator:
    MinLength = inches_to_meters(30) # Elevator height all the way down.
    Rot_to_Dist = 5*0.0254 # Number of Rotations to go 1 m
    cfg = configs.TalonFXConfiguration()
     # Configure gear ratio
    fdb = cfg.feedback
    fdb.sensor_to_mechanism_ratio = 1 # 12.8 rotor rotations per mechanism rotation

    # Configure Motion Magic
    mm = cfg.motion_magic
    mm.motion_magic_cruise_velocity = 2 # 5 (mechanism) rotations per second cruise
    mm.motion_magic_acceleration = 5 # Take approximately 0.5 seconds to reach max vel
    # Take apprximately 0.1 seconds to reach max accel
    mm.motion_magic_jerk = 100

    slot0 = cfg.slot0
    slot0.k_s = 0.25 # Add 0.25 V output to overcome static friction
    slot0.k_v = 0.12 # A velocity target of 1 rps results in 0.12 V output
    slot0.k_a = 0.01 # An acceleration of 1 rps/s requires 0.01 V output
    slot0.k_p = 10 # A position error of 0.2 rotations results in 12 V output
    slot0.k_i = 0 # No output for integrated error
    slot0.k_d = 0.5 # A velocity error of 1 rps results in 0.5 V output


# ------------ Vision Settings --------------------

class vision_settings:
    #These are the ratio to get std dev for the vision system based on trust where 1 is the most trustworthy and 0 is the least
    #So eahc is trust_ratio * (1-trust) + trust_min
    stdXtrust_ratio = 5
    stdYtrust_ratio = 5
    stdRtrust_ratio = 5
    #This is the minumum value for the std dev based on trust trust for any vision mesaurement
    stdXtrust_min = 0.7
    stdYtrust_min = 0.7
    stdRtrust_min = 1.5

    #These are settings for trust based on distance from the target
    #The trust is a value from 0 to 1 where 1 is the most trustworthy and 0 is the least
    #The trust is calculated as -1/10*distance + 1 and is bound between 0 and 1
    tursttoDist_ratio = -1/10 #This should always be negative for example -1/10 means at 10 meters the trust is 0
    tursttoDist_offset = 1 #This should always be 1

class Cameras:
    vision_controller = VisionEstimator()

class Alliance:
    blue_team = False  # Set to True if the robot is on the blue team, False for red team

class DrivebasedAngleAlign:
    allowable_errorX = 0.1  # meters
    allowable_errorY = 0.1
    allowable_errorR = 5  # degrees
    
    p = 10
    i = 0
    d = 0
    alignmentPID = PIDController(p, i, d)
    angleTolerance = 10
    

class RobotPoseConfig:
    pose = Pose2d(0,0,Rotation2d(0))

