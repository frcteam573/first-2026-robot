import math
from unittest import signals
import commands2
import wpilib
import wpilib.drive
import config
import enum #### from enum import Enum ????

from enum import Enum
from phoenix6 import CANBus, configs, controls, hardware, signals
import math
### joel##################################################################
import commands2
import wpilib
import wpilib.drive
import rev
import config

class LED(commands2.SubsystemBase):
  
  def __init__(self) -> None:
    super().__init__()
    
    self.blinkin = wpilib.Spark(9)
    
  # // COLOR FUNCTION LIST \\ #
  
  '''Value list: https://www.revrobotics.com/content/docs/REV-11-1105-UM.pdf'''
  
  def setBlueLed(self):
    self.blinkin.set(0.87)
    #print('Blue')

  def setRedLed(self): 
    self.blinkin.set(0.61)
    #print('Red')

  def setOrangleBlinkLed(self): 
    self.blinkin.set(0.05)
   # print('OrangeBlink')

  def setGreenLed(self):
    self.blinkin.set(0.77)
    #print('Green')

  def setPartyLed(self):
    self.blinkin.set(-0.97)
   # print('Party')

  def setBlack(self):
    self.blinkin.set(0.99)
   # print('Black')

  def setWhiteLed(self):
    self.blinkin.set(0.93)
   # print('White')

  def setYellowLed(self):
    self.blinkin.set(0.69)
   # print('Yellow')


  def ModeManager(self):
    #Motor_Error = not wpilib.SmartDashboard.getBoolean("Any Motor Error", False)
    #Gyro_Error = wpilib.SmartDashboard.getBoolean("Gyro Error", False)
    Hood_At_Position = wpilib.SmartDashboard.getBoolean("Shooter / Hood at Position", False)
    Wheel_At_Speed = wpilib.SmartDashboard.getBoolean("Shooter / Wheel at Speed", False)
    oculusDisconnected = wpilib.SmartDashboard.getBoolean("Oculus Disconnected", False)
    Aligned = wpilib.SmartDashboard.getBoolean("Aligned", False)
    #Done_Climbing = wpilib.SmartDashboard.putBoolean("Done Climbing",False)
    #TargetSeen = wpilib.SmartDashboard.putBoolean("Target Seen",False)
  # these 3 above i put as putboolean as I don't know if we already have a check for these... feel free to add more.
  
    if oculusDisconnected and Hood_At_Position and Wheel_At_Speed:
      if self.animationTimer < 10:
        self.setBlueLed() 
      elif self.animationTimer < 20:
        self.setGreenLed()
      else:
        self.animationTimer = 0
      self.animationTimer += 1
    elif oculusDisconnected:
        self.setBlueLed() ## change later
    elif Aligned and Hood_At_Position and Wheel_At_Speed: #add more checks as needed
      self.setGreenLed()
    elif Aligned or Hood_At_Position or Wheel_At_Speed: #add a check
      self.setWhiteLed()
    else:
        self.setOrangleBlinkLed()
        self.animationTimer = 0