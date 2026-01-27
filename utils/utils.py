import math
from wpilib import DriverStation
import constants
from wpimath.geometry import Pose2d

def inches_to_meters(input:float) -> float:
    """ Input in inches returns meters """
    return input*0.0254

def remap(value: float, threshold: float) -> float:
    if abs(value) > threshold:
        value = value / abs(value) * threshold
    return value

def deadband(value: float, threshold: float) -> float:
    if abs(value) < threshold:
        value = 0
    return value

def max_min_check(value, goal, tolerance) -> bool:
    if abs(goal - value) < tolerance:
        return True
    else:
        return False

def getTargetPose(pose: Pose2d) -> Pose2d:
        '''changes hood angle when not in alliance's zone
        
        Args:
            pose: pose of the robot

        Output:
            True if in alliance zone, False if out

        '''
        
        if DriverStation.getAlliance() == DriverStation.Alliance.kBlue:
            if pose.X() > constants.blueAllianceZoneThreshold: ## not in zone, passing mode
                return pose.nearest(constants.BluePassingPos)
            else: ## in zone, shooting mode
                return constants.HubPositions.BlueHubPos
        else: ##red alliance
            if pose.X() < constants.redAllianceZoneThreshold: ## not in zone, passing mode
                return pose.nearest(constants.RedPassingPos)
            else: ## in zone, shooting mode
                return constants.HubPositions.RedHubPos
            


