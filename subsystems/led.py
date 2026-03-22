import math
from unittest import signals
import commands2
import wpilib
import wpilib.drive
import config
import enum #### from enum import Enum ????

from enum import Enum
from phoenix6 import CANBus, configs, controls, hardware, signals

###################### copied from 2025 code -tyler ###########################

class AnimationType(Enum):
        NONE = 0
        COLOR_FLOW = 1
        FIRE = 2
        LARSON = 3
        RAINBOW = 4
        RGB_FADE = 5
        SINGLE_FADE = 6
        STROBE = 7
        TWINKLE = 8
        TWINKLE_OFF = 9

class LED(commands2.SubsystemBase):

    def __init__(self) -> None:
        super().__init__()

        self.YELLOW = signals.RGBWColor(wpilib.Color.kYellow)
        self.GREEN = signals.RGBWColor(wpilib.Color.kGreen)
        self.WHITE = signals.RGBWColor(wpilib.Color.kWhite)
        self.ORANGE = signals.RGBWColor(wpilib.Color.kOrange)
        self.GREEN = signals.RGBWColor(wpilib.Color.kGreen)
        self.BLUE = signals.RGBWColor(wpilib.Color.kBlue)

        # Keep a reference to all the devices used
        self.candle = hardware.CANdle(45, CANBus("573CANivore"))

        # Configure CANdle
        cfg = configs.CANdleConfiguration()
        # set the LED strip type and brightness
        cfg.led.strip_type = signals.StripTypeValue.GRB
        cfg.led.brightness_scalar = 0.5  #### can be changed
        # disable status LED when being controlled
        cfg.candle_features.status_led_when_active = signals.StatusLedWhenActiveValue.DISABLED

        self.candle.configurator.apply(cfg)
                # clear all previous animations
        for i in range(0, 8):
            self.candle.set_control(controls.EmptyAnimation(i))
        # set the onboard LEDs to a solid color
        self.candle.set_control(controls.SolidColor(0, 8).with_color(self.ORANGE))

    def setBlueLed(self): ### alignment with the hub - teleop only
      self.candle.set_control(controls.SolidColor(0, 8).with_color(self.BLUE))
      #print('Blue')

    def setOrangleBlinkLed(self): ### diagnostic flag - When a diagnostic is flagged, lights flash alternating between error light and other necessary color
      self.candle.set_control(controls.SolidColor(0, 8).with_color(self.ORANGE))
    # print('OrangeBlink')

    def setGreenLed(self): ### robot lined up with ladder - Teleop only, Overrides the game piece lights
      self.candle.set_control(controls.SolidColor(0, 8).with_color(self.GREEN))
      #print('Green')

    def setBlack(self): ### low power mode - Drivetrain and reaction bar are only subsystems running, Flashing red on dashboard, Prioritize no lights when in low power mode
      self.candle.set_control(controls.SolidColor(0, 8).with_color(signals.RGBWColor(0, 0, 0, 0)))

    def setWhiteBlinkLed(self): ### full hopper - Teleop only (only when in middle)
      self.candle.set_control(controls.SolidColor(0, 8).with_color(self.WHITE))



    def ModeManager(self):
      #Motor_Error = not wpilib.SmartDashboard.getBoolean("Any Motor Error", False)
      #Gyro_Error = wpilib.SmartDashboard.getBoolean("Gyro Error", False)
      Hood_At_Position = wpilib.SmartDashboard.getBoolean("Shooter / Hood at Position", False)
      Wheel_At_Speed = wpilib.SmartDashboard.getBoolean("Shooter / Wheel at Speed", False)

      Aligned = wpilib.SmartDashboard.getBoolean("Aligned", False)
      #Done_Climbing = wpilib.SmartDashboard.putBoolean("Done Climbing",False)
      #TargetSeen = wpilib.SmartDashboard.putBoolean("Target Seen",False)
    # these 3 above i put as putboolean as I don't know if we already have a check for these... feel free to add more.

      if Aligned and Hood_At_Position and Wheel_At_Speed: #add more checks as needed
        self.setGreenLed()
      elif Aligned or Hood_At_Position or Wheel_At_Speed: #add a check
        self.setWhiteBlinkLed()
      else:
         self.setOrangleBlinkLed()