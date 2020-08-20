from easyapplybot import EasyApplyBot
import loginGUI

"""
define if ou want to use the GUI or not (True or False)

"""
useGUI = False


"""
If GUI is False enter your credentials and preferences manually
"""

if useGUI == False :

    username = 'XXX@gmail.com'
    password = 'XXX'
    language = 'en'
    position = 'python'
    location = 'remote'
    resumeloctn = open(r'C:\Users\Debora Oliveira...')


"""
If GUI is True, just run the script
"""

if useGUI == True :

    app = loginGUI.LoginGUI()
    app.mainloop()

    # get user info info
    username=app.frames["StartPage"].username
    password=app.frames["StartPage"].password
    language=app.frames["PageOne"].language
    position=app.frames["PageTwo"].position
    location_code=app.frames["PageThree"].location_code
    if location_code == 1:
        location=app.frames["PageThree"].location
    else:
        location = app.frames["PageFour"].location
    resumeloctn=app.frames["PageFive"].resumeloctn

    print(username,password, language, position, location_code, location, resumeloctn)


#start bot
bot = EasyApplyBot(username,password, language, position, location, resumeloctn)
bot.start_apply()
