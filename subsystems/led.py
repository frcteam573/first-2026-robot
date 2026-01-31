import math
import commands2
import wpilib
import wpilib.drive
import rev
import config

###################### copied from 2025 code -tyler ###########################

class LED(commands2.SubsystemBase):
  
  def __init__(self) -> None:
    super().__init__()
    
    self.blinkin = wpilib.Spark(9) #### change!!!!!!!!!!
    
  # // COLOR FUNCTION LIST \\ #
  
  '''Value list: https://www.revrobotics.com/content/docs/REV-11-1105-UM.pdf'''
  
  def setBlueLed(self): ### alignment with the hub - teleop only
    self.blinkin.set(0.87)
    #print('Blue')

  def setOrangleBlinkLed(self): ### diagnostic flag - When a diagnostic is flagged, lights flash alternating between error light and other necessary color
    self.blinkin.set(0.05)
   # print('OrangeBlink')

  def setGreenLed(self): ### robot lined up with ladder - Teleop only, Overrides the game piece lights
    self.blinkin.set(0.77)
    #print('Green')

  def setPartyLed(self): ### robot done climbing - Lights not in use during low power mode, Overrides other lights except diagnostic
    self.blinkin.set(-0.97)
   # print('Party')

  def setBlack(self): ### low power mode - Drivetrain and reaction bar are only subsystems running, Flashing red on dashboard, Prioritize no lights when in low power mode
    self.blinkin.set(0.99)
   # print('Black') ############ LEDs off

 ### copied from setWhiteLed, not sure if Blink is a diff number or not
  def setWhiteBlinkLed(self): ### full hopper - Teleop only (only when in middle)
    self.blinkin.set(0.93)
   # print('WhiteBlink')



  def ModeManager(self):
    Motor_Error = not wpilib.SmartDashboard.getBoolean("Any Motor Error",False)
    Gyro_Error = wpilib.SmartDashboard.getBoolean("Gyro Error",False)
    Hood_At_Position = wpilib.SmartDashboard.getBoolean("Shooter / Hood at Position",False)
    Wheel_At_Speed = wpilib.SmartDashboard.getBoolean("Shooter / Wheel at Speed",False)
    
    # Algae_Released = wpilib.SmartDashboard.getBoolean("Algae Released",False)
    # Alligned_Reef_Level = wpilib.SmartDashboard.getBoolean("Alligned Reef Level",False)
    # Done_Climbing = wpilib.SmartDashboard.getBoolean("Done Climbing",False)
    # TargetSeen = wpilib.SmartDashboard.getBoolean("Target Seen",False)
    # HPTargetSeen = wpilib.SmartDashboard.getBoolean("HP Target Seen",False)
    
    error = False
    if Motor_Error or Gyro_Error:
      if config.LedCounter < 10:
        error = True
      elif config.LedCounter < 20:
        error = False
      else:
        config.LedCounter = 0
      config.LedCounter = config.LedCounter + 1
    else:
      error = False

    if error == True: 
        self.setOrangleBlinkLed() 
        #print ("orange")
    elif Alligned_Reef_Level:
      self.setGreenLed()
    elif config.cachedShooterMode ==True and Coral_In:
      if TargetSeen:
        self.setWhiteLed()
      else: 
        self.setRedLed()
    elif config.cachedShooterMode == False and TargetSeen:
      self.setWhiteLed()
    elif Done_Climbing:
      self.setPartyLed()
    elif HPTargetSeen:
      self.setYellowLed()
    else: 
      self.setBlack()
      #print ("no color")