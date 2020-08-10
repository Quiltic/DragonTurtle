import os, subprocess

#get home and where to clone to
cwd = "/home/pi/DragonTurtle"#os.getcwd()
print(cwd) # location

#Clone to location
os.chdir(cwd) # move to home
os.system("sudo git pull https://github.com/Quiltic/DragonTurtle.git") # update turtle
print("cloned") # Tell me you did it

# go home
os.chdir(cwd)
#os.system("sudo chmod ugo+rwx ActiveUsing.xml") # this is a failsafe
#os.system("mv /home/pi/DragonTurtle/Tools/player.py /home/pi/DragonTurtle/Tools/Player.py") # For some reason its saved as a lowercase p when installed with git

#reopen turtle
call_freind = "python3 " + cwd + "/DragonTurtle.py &" # Launch the Dragon Command
os.system("ls") # Make sure that we achualy have the proper location
print(call_freind) # Show the command
os.system(call_freind) # AWAKIN THE DRAGON!

print("Updated!\nTurning off") # Just what we needed

