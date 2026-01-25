from wpimath.geometry import Pose3d, Pose2d
from wpilib import Timer
from photonlibpy import PhotonCamera, PhotonPoseEstimator
import constants, config
from vision.fieldTagLayout import FieldTagLayout, AprilTagFieldLayout, AprilTagField
import os


class VisionEstimator:
    """
    An estimator (e.g. limelight, photon-vision) that returns a list of robot poses relative to the field.
    """

    def __init__(self):
        # deploy_dir = "C:\\Users\\savag\\OneDrive\\Documents\\GitHub\\Team573CTRESwervewithSIM\\"
        # json_path = os.path.join(deploy_dir, "vision\\2026-rebuilt-welded.json")
        # tagLayout = AprilTagFieldLayout(json_path)
        tagLayout = AprilTagFieldLayout.loadField(AprilTagField.k2026RebuiltWelded)
        self.cam = PhotonCamera('camera1')
        self.camPoseEst = PhotonPoseEstimator(
            tagLayout,
            constants.Robot_To_Camera1,
        )

    def get_estimated_robot_pose(self) -> tuple[Pose2d, float] | None:
        """
        Returns the robot's pose relative to the field, estimated by the vision system. Override this method.
        :return: Vision system estimate of robot pose along with the associated timestamp.
        :rtype: list[Pose2d, seconds: float] | None
        """
        camEstPose = None
        for result in self.cam.getAllUnreadResults():
            camEstPose = self.camPoseEst.estimateCoprocMultiTagPose(result)
            if camEstPose is not None:
                print(camEstPose.estimatedPose.toPose2d())
            # if camEstPose is None:
                # camEstPose = self.camPoseEst.estimateLowestAmbiguityPose(result)
        if camEstPose is not None:
            return camEstPose.estimatedPose.toPose2d(), camEstPose.timestampSeconds
        else:
            return None