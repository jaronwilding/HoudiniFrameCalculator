# Houdini Frame Calculator

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Usage](#usage)
* [Acknowledgements](#acknowledgements)


## General Info
A simple python script to track render times in Houdini
 
The script can be run basically anywhere, but it was created with rendering out Geometry primarily, as you can add metadata inside of image files, saying render times and such.

Tested on Houdini 18.5 - Windows 10.

## Setup
To use inside of Houdini, install the script to this directory:
```
houdini18.5/scripts/python
```
If the directory does not exist, create it.

![Install Location](https://user-images.githubusercontent.com/26001129/114502435-5d3bef80-9c5e-11eb-9012-3f72d05eb314.JPG)


## Usage
There are three main functions inside the script. Below are the uses.

### ROP Setup

Before you use the scripts though, you have to add one extra parameter to the ROP.

1) Click the cog on the ROP node in the parameters, and select `Edit Parameter Interface...`
2) Drag and drop a `String` from the `Create Parameters` to the `Existing Parameters`
3) Set the name of the new parameter to `jsonoutput`
4) Hit `Accept` and you're done!

![ROPChanges](https://user-images.githubusercontent.com/26001129/114503778-629a3980-9c60-11eb-8bce-49f58a26ad6c.JPG)


### Create File

I use this function in the Pre-Render Script section of a ROP. (You can edit the script easier by selecting and pressing "Alt+E" to bring up a script window)

Make sure that the script type is set to `Python` and not `HScript`

I have added descriptions here, but you can remove them for ease.
```
# Import the library
import frameTimer
# We need to grab the parameters from our current node.
node = hou.pwd()

# The "sopoutput" is our "Output File" parameter
outputFile = node.parm("sopoutput").eval()
# The "jsonoutput" is a custom string parameter that you have to add yourself.
jsonName = node.parm("jsonoutput").eval()

# Creation of the file. This script will create the directory if not found.
frameTimer.createFile(outputFile, jsonName, hou.frame())
```

![CreateFile](https://user-images.githubusercontent.com/26001129/114504849-17812600-9c62-11eb-89fc-b076bef33fdc.JPG)


### Edit File

I use this function in the `Pre-Frame Script` and `Post-Frame Script` section of a ROP. (You can edit the script easier by selecting and pressing `Alt+E` to bring up a script window).
If you want to make it calculate the write speed instead of the frame speed, instead of `Post-Frame Script`, place it inside of the `Post-Write Script`

Make sure that the script type is set to `Python` and not `HScript`

I have added descriptions here, but you can remove them for ease.
```
# Import the library
import frameTimer
# We need to grab the parameters from our current node.
node = hou.pwd()

# The "sopoutput" is our "Output File" parameter
outputFile = node.parm("sopoutput").eval()
# The "jsonoutput" is a custom string parameter that you have to add yourself.
jsonName = node.parm("jsonoutput").eval()

# Editing the file. It will automatically detect if it is adding new data, and adjusting the timestamp.
frameTimer.editFile(outputFile, jsonName, hou.frame())
```

![EditFile](https://user-images.githubusercontent.com/26001129/114504876-1fd96100-9c62-11eb-98e6-497004c3940c.JPG)


### Total Time

I use this function in the `Post-Render Script` section of a ROP. (You can edit the script easier by selecting and pressing `Alt+E` to bring up a script window).

Make sure that the script type is set to `Python` and not `HScript`

I have added descriptions here, but you can remove them for ease.
```
# Import the library
import frameTimer
# We need to grab the parameters from our current node.
node = hou.pwd()

# The "sopoutput" is our "Output File" parameter
outputFile = node.parm("sopoutput").eval()
# The "jsonoutput" is a custom string parameter that you have to add yourself.
jsonName = node.parm("jsonoutput").eval()

# I am just going to print it to the console, but you can use this function elsewhere if you need to. It just needs the outputfile, and the json name.
print(frameTimer.totalTime(outputFile, jsonName))
```

![PrintFile](https://user-images.githubusercontent.com/26001129/114504910-2c5db980-9c62-11eb-91cb-aed566cc7538.JPG)


## Acknowledgements


[Jeff Lim and his small python script for getting total simulation time.](https://limjeff.wordpress.com/2017/04/27/houdini-simulation-timestamp/)
