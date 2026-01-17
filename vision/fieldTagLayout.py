from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
from vision.singleton import Singleton
import os


class FieldTagLayout(metaclass=Singleton):
    def __init__(self):
        #Field tags
        self.fieldTags = AprilTagFieldLayout.loadField(AprilTagField.k2026RebuiltWelded)
        # deploy_dir = "C:\\Users\\savag\\OneDrive\\Documents\\GitHub\\Team573CTRESwervewithSIM\\"
        # json_path = os.path.join(deploy_dir, "vision\\2026-rebuilt-welded.json")
        # self.fieldTags = AprilTagFieldLayout(json_path)
        #Shop tags
        #self.fieldTags = constants.Shop_AprilTagLayout

    def lookup(self, tagId):
        return self.fieldTags.getTagPose(tagId)