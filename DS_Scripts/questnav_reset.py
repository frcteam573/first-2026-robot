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

def trigger_adb_command():
    """Execute the adb command to start the app"""
    cmd = 'adb.exe shell am start -n gg.QuestNav.QuestNav/com.unity3d.player.UnityPlayerGameActivity'
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("ADB command executed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ADB command: {e}")

def main():

    """Monitor SmartDashboard for Occulus DTap Reset"""
    print("Monitoring SmartDashboard for 'Occulus DTap Reset'...")
    previous_state = False

    topics = table.getTopics()
    for topic in topics:
        print(topic.getName())
    
    while True:
        try:
            reset_value = Sub.get()

            # Trigger only on transition from False to True
            if reset_value and not previous_state:
                print("Occulus DTap Reset triggered!")
                trigger_adb_command()
            
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