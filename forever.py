from subprocess import Popen

filename = r'C:\Users\User\Data_Science_Projects\luka_bot\luka_bot.py'
while True:
    print("\nStarting " + filename)
    p = Popen("python " + filename, shell=True)
    p.wait()
