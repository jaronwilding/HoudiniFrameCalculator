# Houdini Frame Calculator

## Table of contents
* [General info](#general-info)
* [Setup](#setup)
* [Usage](#usage)
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

Before you use the scripts though, you have to add one extra parameter to the ROP.

1) Click the cog on the ROP node in the parameters, and select `Edit Parameter Interface...`
2) Drag and drop a `String` from the `Create Parameters` to the `Existing Parameters`
3) Set the name of the new parameter to `jsonoutput`
4) Hit `Accept` and you're done!

![ROPChanges](https://user-images.githubusercontent.com/26001129/114503778-629a3980-9c60-11eb-8bce-49f58a26ad6c.JPG)


### Create File

I use this function in the Pre-Render Script section of a ROP. (You can edit the script easier by selecting and pressing "Alt+E" to bring up a script window)

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
