import os, subprocess, time

time.sleep(10)
#get home and where to clone to
cwd = "/home/pi/Turtle"#os.getcwd()
#mainfile = cwd[:cwd.rfind('\\')]
print(cwd)


#Clone to location
os.system(("cd " + cwd))
os.system("git pull https://github.com/Quiltic/Turtle.git")
print("cloned")

#give it a moment or 12 then go home
#time.sleep(3)
os.system(("cd "+ cwd))

#reopen turtle
#time.sleep(10)
call_freind = "python3 " + cwd + "/Turtle.py &"
os.system("ls")
print(call_freind)
os.system(call_freind)
#subprocess.Popen(call_freind)
print("Updated!")

print("Turning off")
