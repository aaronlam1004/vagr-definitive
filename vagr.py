import os, sys, subprocess, time, random
from VagrJSON import *

# path to Oracle's VirtualBox directory
vbox = os.path.abspath("C:/Program Files/Oracle/VirtualBox")

# runs a VBoxManage command
def runVBoxCommand(commands):
		cwd = os.getcwd()
		os.chdir(vbox)
		commands.insert(0, "VBoxManage")
		subprocess.run(commands)
		os.chdir(cwd)

# checks to see if Vagr machine is running
def running():
		cwd = os.getcwd()
		os.chdir(vbox)
		out = subprocess.check_output(["VBoxManage", "list", "runningvms"])
		runningvms = [machine.split(" ")[0].translate({ord('\"'): None}) for machine in out.decode("utf-8").split("\n")]
		os.chdir(cwd)
		if readVagrJson("machine") in runningvms:
				return True
		return False

# hads program wait based on input time
def wait(givenTime):
		frame = random.randint(0, 5)
		animationFrames = [
		 "UwU",
		 "OwO",
		 ">w<",
		 "✧w✧",
		 "☆w☆",
		 "♥w♥"
		]
		t = 0
		while t != givenTime:
				print(animationFrames[frame % len(animationFrames)], end = "\r")
				time.sleep(1)
				frame += 1
				t += 1

# prints the error message when user inputs wrong information
def printErrorMessage(eMessage):
		print(eMessage)
		print("Usage: vagr [command]")
		print("Commands:")
		print(" ovas")
		print(" init [vagr machine ova] [vmname]")
		print(" up")
		print(" down")
		print(" reload")
		print(" rename [vmname]")
		print(" destroy")
		print(" status")

# prints the information of the machine
def printMachineInfo():
		print(readVagrJson('machine') + ": " + str(running()))
		for port in readVagrJson('ports'):
				guestip = "localhost"
				portNum = 22
				if port[2] != "":
						guestip = port[2]
				if port[3] != 22:
						portNum = port[3]
				print(" " + port[0] + ": " + guestip + ":" + str(portNum))
		for shared in readVagrJson('shared'):
				print(" " + shared[0] + ": " + shared[1] + " -> " + shared[2])

# creates a port inside Vagr VM (VBoxManage)
def createPort(portInfo):
		portString = ""
		for info in portInfo[0:-1]:
				portString += info + ", "
		portString = portString + portInfo[-1]
		if not running():
				runVBoxCommand(['modifyvm', readVagrJson("machine"), '--natpf1' , portString])
		else:
				runVBoxCommand(['controlvm', readVagrJson("machine"), 'natpf1' , portString])

# deletes a port inside Vagr VM (VBoxManage)
def deletePort(portInfo):
		if not running():
				runVBoxCommand(['modifyvm', readVagrJson('machine'), '--natpf1', 'delete', portInfo[0]])
		else:
				runVBoxCommand(['controlvm', readVagrJson('machine'), 'natpf1', 'delete', portInfo[0]])

# adds a shared folder inside Vagr VM (VBoxManage)
def addShared(sfInfo):
		runVBoxCommand(['sharedfolder', 'add', readVagrJson('machine'), '--name', sfInfo[0], '--hostpath', os.path.abspath(sfInfo[1]), '--transient'])

# runs commands that makes a folder based on share folder and then mounts that folder into Vagr VM
def initShared(sfInfo):
		runVBoxCommand(['guestcontrol', readVagrJson('machine'), 'run', '--exe', '/bin/sh', '--username', 'root', '--password', 'vagr', '--quiet', '--', 'sh/arg0', '-c', 'mkdir ' + sfInfo[1] + ' 2>null'])
		runVBoxCommand(['guestcontrol', readVagrJson('machine'), 'run', '--exe', '/sbin/mount.vboxsf', '--username', 'root', '--password', 'vagr', '--quiet', '--', 'mount.vboxsf/arg0', sfInfo[0], sfInfo[1]])

# adds and inits all the shared folders inside the Vagr VM based on the Vagr.json file
def sharedInit():
		for shared in readVagrJson("shared"):
				if len(shared) != 3:
						print("Insufficient formatting of shared directory.")
				elif shared[0] == "":
						print("No name for share folder specified.")
				elif shared[1] == "" or not os.path.exists(shared[1]):
						print(shared[1] + " is not a valid directory. Unable to add shared folder.")
				elif shared[2] == "":
						print("Share folder directory on Vagr machine not specified.")
				else:
						addShared((shared[0], shared[1]))
						initShared((shared[0], shared[2]))

# does changes based on modification in the Vagr.json file
def doChanges():
		changes = findDifferences()
		if changes["delete"] != []:
				for change in changes["delete"]:
						deletePort(change)
		if changes["add"] != []:
				for change in changes["add"]:
						createPort(change)

def runCommand(cmd):
		if getattr(sys, 'frozen', False):
				filepath = os.path.dirname(sys.executable)
		else:
				filepath = os.path.dirname(__file__)
		# vagr init [vagr machine] [vmname]
		if cmd == "init":
				if len(sys.argv) != 4:
						printErrorMessage("Insufficient amount of arguments required to run [" + cmd + "]")
				elif not os.path.exists(os.path.join(filepath, "ovas", sys.argv[2] + ".ova")):
						printErrorMessage("No vagr machine specified")
				else:
						runVBoxCommand(['import', os.path.join(filepath, 'ovas', sys.argv[2] + ".ova"), '--vsys', '0', '--vmname', sys.argv[3]])
						writeVagrJson("machine", sys.argv[3])
						createPort(["ssh", "tcp", "127.0.0.1", "2222", "", "22"])
						writeVagrJson("ports", [["ssh", "tcp", "127.0.0.1", "2222", "", "22"]])
						writeVagrJson("shared", [["vagr", os.path.abspath(os.getcwd()), "/home/vagr_home"]])
		# vagr up
		elif cmd == "up" and not running():
				doChanges()
				print("Starting up Vagr machine: " + readVagrJson('machine'))
				runVBoxCommand(['startvm', readVagrJson('machine'), '--type', 'headless'])
				wait(50)
				printMachineInfo()
				sharedInit()
		# vagr down
		elif cmd == "down" and running():
				print("Shutting down Vagr machine: " + readVagrJson('machine'))
				runVBoxCommand(['controlvm', readVagrJson('machine'), "poweroff"])
		# vagr reload
		elif cmd == "reload" and running():
				doChanges()
				print("Reloading Vagr machine: " + readVagrJson('machine'))
				runVBoxCommand(['controlvm', readVagrJson('machine'), 'reset'])
				wait(50)
				printMachineInfo()
				sharedInit()
		# vagr rename [vmname]
		elif cmd == "rename" and not running():
				if len(sys.argv) == 3:
						print("Renaming Vagr machine: " + readVagrJson('machine') + "->" + sys.argv[2])
						runVBoxCommand(["modifyvm", readVagrJson('machine'), "--name", sys.argv[2]])
						tmpFile = os.path.join(filepath, "tmp", "." + readVagrJson('machine') + ".json")
						os.remove(tmpFile)
						writeVagrJson("machine", sys.argv[2])
				else:
						printErrorMessage("Insufficient amount of arguments required to run [" + cmd + "]")
		# vagr destroy
		elif cmd == "destroy" and not running():
				print("Removing Vagr machine: " + readVagrJson('machine'))
				runVBoxCommand(['unregistervm', readVagrJson('machine'), '--delete'])
				tmpFile = os.path.join(filepath, "tmp", "." + readVagrJson('machine') + ".json")
				os.remove(tmpFile)
				os.remove('Vagr.json')
		# vagr status
		elif cmd == "status":
				printMachineInfo()
		# vagr ovas
		elif cmd == "ovas":
				ovasDirectory = os.path.join(filepath, "ovas")
				for file in os.listdir(ovasDirectory):
						print(file[0:-4])
		else:
				eMessage = "Could not run command: vagr [" + cmd + "]\n"
				if cmd in ["down", "reload", "ssh"]:
						eMessage += " Make sure the machine is running before starting this command...\n"
				elif cmd == "up":
						eMessage += " Make sure the machine is NOT running before starting this command...\n"
				else:
						eMessage += " Make sure that the command is valid.\n"
				printErrorMessage(eMessage)

if __name__ == '__main__':
		validCmds = ["init", "ovas", "up", "down", "reload", "rename", "destroy", "status"]
		if len(sys.argv) == 1 or sys.argv[1] not in validCmds:
				printErrorMessage("No command specified")
		elif sys.argv[1] in validCmds[2:] and not os.path.exists(os.path.join(os.getcwd(), "Vagr.json")):
				printErrorMessage("No Vagr.json file")
		else:
				runCommand(sys.argv[1])
