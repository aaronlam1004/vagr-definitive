import os, json, sys

# makes a .[vmname].json copy of Vagr.json
def vagrJsonCopy(vmname, vData):
	if getattr(sys, 'frozen', False):
		tmpFile = os.path.join(os.path.dirname(sys.executable), "tmp", "." + vmname + ".json")
	else:
		tmpFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp", "." + vmname + ".json")
	json.dump(vData, open(tmpFile, "w"))

# writes information into the Vagr.json
def writeVagrJson(section, info):
	if os.path.exists("Vagr.json"):
		jsonFile = open("Vagr.json", "r")
		vagrFile = json.load(jsonFile)
	else:
		vagrFile = {}
	vagrFile[section] = info
	json.dump(vagrFile, open("Vagr.json", "w"))
	vagrJsonCopy(vagrFile["machine"], vagrFile)

# reads information from Vagr.json file
def readVagrJson(section):
	jsonFile = open("Vagr.json", "r")
	vagrFile = json.load(jsonFile)
	jsonFile.close()
	return vagrFile[section]

# locates differences between Vagr.json and .[vmname].json files and returns those differences as a dict
def findDifferences():
	if not os.path.exists("Vagr.json"):
		printErrorMessage("Vagr.json missing\nNo vagr machine set up")
		return
	vagrFile = json.load(open("Vagr.json", "r"))

	if getattr(sys, 'frozen', False):
		tmp = os.path.join(os.path.dirname(sys.executable), "tmp", "." + vagrFile['machine'] + ".json")
	else:
		tmp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tmp", "." + vagrFile['machine'] + ".json")

	if not os.path.exists(tmp):
		vagrJsonCopy(vagrFile["machine"], vagrFile)
	tmpFile = json.load(open(tmp, "r"))

	changes = {"add": [], "delete": []}

	for port in vagrFile["ports"]:
		if port not in tmpFile["ports"]:
			changes["add"].append(port)
	for port in tmpFile["ports"]:
		if port not in vagrFile["ports"]:
			changes["delete"].append(port)

	tmpFile["ports"] = vagrFile["ports"]
	json.dump(tmpFile, open(tmp, "w"))

	return changes
