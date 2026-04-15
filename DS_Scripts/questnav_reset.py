
import time
import subprocess
import ntcore

# NEEDS TO BE RUN ON THE SAME COMPUTER AS THE DRIVER STATION, DURING MATCHES

# Initialize NetworkTables
inst = ntcore.NetworkTableInstance.getDefault()
inst.startClient4("python-client")
# inst.setServer("127.0.0.1")
inst.setServerTeam(573) 

print(inst.getTopics())

def setup_QN():

    #Look for QN
    for i in range(200,209):
        cmd2 = "adb connect 10.5.73."+str(i)+':5802'
        # cmd = "adb shell ping 10.5.73."+str(i)
        try:
            subprocess.run(cmd2, shell=True, check=True)
            print("Found QN at 10.5.73."+str(i))
            # subprocess.run(cmd2, shell=True, check=True)
            return i
        except subprocess.CalledProcessError as e:
            print(f"Error executing ADB command: {e}")
            continue
    
    return 0

def trigger_adb_command(port):
    """Execute the adb command to start the app"""
    cmd = 'adb.exe -s 10.5.73.'+str(port)+':5802 shell am start -n gg.QuestNav.QuestNav/com.unity3d.player.UnityPlayerGameActivity'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("ADB command executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

def main():

    """Monitor SmartDashboard for Occulus DTap Reset"""
   
    previous_state = False
    setup = 0
    #Ensure QN is setup
    while setup == 0:
        setup = setup_QN()
        time.sleep(.5)


    print("Monitoring SmartDashboard for 'Occulus DTap Reset'...")
    
    while True:
        try:
            reset_value = Sub.get()

            # Trigger only on transition from False to True
            if reset_value and not previous_state:
                print("Occulus DTap Reset triggered!")
                trigger_adb_command(setup)
            
            previous_state = reset_value
            time.sleep(0.1)  # Check every 100ms
            
        except Exception as e:
            print(f"Error reading SmartDashboard: {e}")
            time.sleep(1)

if __name__ == "__main__":

    inst = ntcore.NetworkTableInstance.getDefault()
    table = inst.getTable("SmartDashboard")
    Sub = table.getBooleanTopic("Occulus DTap Reset").subscribe(False)
    inst.startClient4("example client")
    # inst.setServer("127.0.0.1") # or use
    inst.setServerTeam(573) # where TEAM=190, 294, etc, or use inst.setServer("hostname") or similar
    inst.startDSClient() # recommended if running on DS computer; this gets the robot IP from the DS

    # subprocess.run("adb.exe tcpip 5801", shell=True, check=True)
    main()