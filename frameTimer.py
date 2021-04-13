import os
import json
# Import datetime twice, because why not. Python can kinda suck.
import datetime as dt
from datetime import datetime, timedelta
from time import gmtime, strftime

# Ideally I would create a class function, but since our python file gets called different times, just making them as functions
# appears to be a better way.

# Custom hash checker. This will remove redundant writing.
def make_hash(d):
    check = ''
    for key in d:
        check += str(d[key])
    return hash(check)

def createFile(outputFile, jsonName, currentFrame):
    if not outputFile.strip():
        return False #TODO -  This may need to be converted to an error.
    if not jsonName.strip():
        return False #TODO -  This may need to be converted to an error.

    # Get the folder from our paths
    outputFolder = os.path.dirname(outputFile)

    # Check if directory exists!! If not, create it!
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    # Get current time
    currentTime = strftime("%H:%M:%S", gmtime())

    # Create the jsonFile path
    jsonFile = os.path.abspath(os.path.join(outputFolder, "{}.metadata.json").format(jsonName))

    # Open our JSON
    outJson = open(jsonFile, "w")

    # Create our initial JSON data. It holds the current frame, starttime, endtime and the total time taken.
    # Again, I would normally make this as a class, but for now this appears to be the best option
    jsonData = {}
    jsonData["Meta"] = []
    jsonData["Meta"].append(
        { 
        "frame": currentFrame, 
        "startTime": currentTime, 
        "endTime" : "", 
        "timeTaken" : "" 
        })
    
    # Write out our Json file.
    json.dump(jsonData, outJson, indent=6)

    # Close the file.
    outJson.close()

# Primary workhorse
def editFile(outputFile, jsonName, currentFrame):
    if not outputFile.strip():
        return False #TODO - This may need to be converted to an error.
    if not jsonName.strip():
        return False #TODO - This may need to be converted to an error.

    # Get the folder from our paths
    outputFolder = os.path.dirname(outputFile)

    # Get current time
    currentTime = strftime("%H:%M:%S", gmtime())

    # Create the jsonFile path
    jsonFile = os.path.abspath(os.path.join(outputFolder, "{}.metadata.json").format(jsonName))

    # Open our json file as a read, and just apply it to data.
    with open(jsonFile, "r") as json_file:
        data = json.load(json_file)
    
    # Make sure we HAVE data?
    if data:
        # Create a checksum to check against later.
        checksum = make_hash(data)

        # Loop through each one of our data. See if we have a time?
        adjustingFrame = False
        for frameData in data["Meta"]:
            # Check if our frame is equal to our current frame. If not, jump to next iteration
            if(frameData["frame"] != currentFrame):
                continue

            # Apply the endtime to our frame.
            frameData["endTime"] = currentTime
            # Get previous time
            tPreviousTime = datetime.strptime(frameData["startTime"], "%H:%M:%S")
            # Get current time
            tCurrentTime = datetime.strptime(currentTime, "%H:%M:%S")
            # Get time taken
            timeTaken = (tCurrentTime - tPreviousTime)
            # Apply to our data
            frameData["timeTaken"] = str(timeTaken)
            adjustingFrame = True

        if adjustingFrame == False:
            data["Meta"].append(
                { 
                "frame": currentFrame, 
                "startTime": currentTime, 
                "endTime" : "", 
                "timeTaken" : "" 
                })

        # Write out our final!
        if checksum != make_hash(data):
            with open(jsonFile, "r+") as json_file:
                json.dump(data, json_file, indent=6)
                json_file.truncate()

def totalTime(outputFile, jsonName):
    if not outputFile.strip():
        return False #TODO - This may need to be converted to an error.
    if not jsonName.strip():
        return False #TODO - This may need to be converted to an error.

    # Get the folder from our paths
    outputFolder = os.path.dirname(outputFile)

     # Create the jsonFile path
    jsonFile = os.path.abspath(os.path.join(outputFolder, "{}.metadata.json").format(jsonName))

    # Open our json file as a read, and just apply it to data.
    with open(jsonFile, "r") as json_file:
        data = json.load(json_file)

        totalTimeTaken = dt.timedelta(hours=0, minutes=0, seconds=0)
        for frameData in data["Meta"]:
            # Stupid, hacky way of getting the total time. We first convert it from string to datetime.datetime
            timeTakenD = datetime.strptime(frameData["timeTaken"], "%H:%M:%S")
            # Then we get the hours, minutes and seconds, and convert that to timedelta.
            timeTaken = dt.timedelta(hours=timeTakenD.hour, minutes=timeTakenD.minute, seconds=timeTakenD.second)
            # Finally, we just add them all together.
            totalTimeTaken = totalTimeTaken + timeTaken

    return(str(totalTimeTaken))