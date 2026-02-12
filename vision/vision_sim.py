import photonlibpy.simulation as pv_sim
from robotpy_apriltag import AprilTagField, AprilTagFieldLayout
from wpimath.geometry import Rotation2d 
from config import Cameras
import constants
from photonlibpy import PhotonCamera
import wpilib
import os

def photonvision_sim_setup():
    print("Setting up photonvision sim...")
    try:
        #setup sim vision system
        visionSim = pv_sim.VisionSystemSim("main")
        # deploy_dir = "C:\\Users\\savag\\OneDrive\\Documents\\GitHub\\Team573CTRESwervewithSIM\\"
        # json_path = os.path.join(deploy_dir, "vision\\2026-rebuilt-welded.json")
        # tagLayout = AprilTagFieldLayout(json_path)

        #Add field tags to the sim system       
        tagLayout = AprilTagFieldLayout.loadField(AprilTagField.k2026RebuiltWelded)
        visionSim.addAprilTags(tagLayout)

        #setup sim camera properties
        camera_prop = pv_sim.SimCameraProperties()
        camera_prop.setCalibrationFromFOV(640,480,Rotation2d.fromDegrees(70)) #A 640 x 480 camera with a 70 degree diagonal FOV
        camera_prop.setCalibError(0.25, 0.08) #Approximate detection noise with average and standard deviation error in pixels. These valuse from from the PhotonVision documentation
        camera_prop.setFPS(30) #Camer FPS, this will be throttled based on robot loop rate on real robot so be sure to put an tested value here.
        camera_prop.setAvgLatency(0.035) #Avg latency in seconds. This is the time it takes for the camera to process the image and send it to the robot.
        camera_prop.setLatencyStdDev(0.005) #Std dev of latency in seconds.

        #Setup all cameras in the sim system
    
        print("camera1")
        camera_sim = pv_sim.PhotonCameraSim(PhotonCamera('camera1'),camera_prop)
        #camera_sim.enableRawStream(True)
        #camera_sim.enableProcessedStream(True)
        #camera_sim.enableDrawWireframe(True)
        visionSim.addCamera(camera_sim,constants.Robot_To_Camera1)


    except Exception as e:
        print("Error setting up photonvision sim: ", e)
        return None

    return visionSim