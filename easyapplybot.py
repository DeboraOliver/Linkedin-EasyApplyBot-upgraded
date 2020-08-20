import time, random, os, csv, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
#import bs4
import pandas as pd
import pyautogui
from tkinter import filedialog, Tk
import tkinter.messagebox as tm
from urllib.request import urlopen
import loginGUI

# pyinstaller --onefile --windowed --icon=app.ico easyapplybot.py

class EasyApplyBot:

    MAX_APPLICATIONS = 500

    def __init__(self,username,password, language, position, location, resumeloctn, appliedJobIDs, filename):

        print("\nBem-vinda ao Easy Apply Bot\n")
        dirpath = os.getcwd()
        print("current directory is : " + dirpath)
        chromepath = dirpath + '/assets/chromedriver.exe'

        self.language = language
        self.appliedJobIDs = appliedJobIDs
        self.filename = filename
        self.options = self.browser_options()
        self.browser = webdriver.Chrome(chrome_options=self.options, executable_path = chromepath)
        self.wait = WebDriverWait(self.browser, 30)
        self.start_linkedin(username,password)


    def browser_options(self):
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        return options

    def start_linkedin(self,username,password):
        print("\nLogging in.....\n \nPor favor espere :) \n ")
        self.browser.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
        try:
            user_field = self.browser.find_element_by_id("username")
            pw_field = self.browser.find_element_by_id("password")
            login_button = self.browser.find_element_by_css_selector(".btn__primary--large")
            user_field.send_keys(username)
            user_field.send_keys(Keys.TAB)
            time.sleep(1)
            pw_field.send_keys(password)
            time.sleep(1)
            login_button.click()
        except TimeoutException:
            print("TimeoutException! Username/password field or login button not found")

    def wait_for_login(self):
        if language == "en":
             title = "Sign In to LinkedIn"
        elif language == "es":
             title = "Inicia sesión"
        elif language == "pt":
             title = "Entrar no LinkedIn"

        time.sleep(random.uniform(3,1.5))

        while True:
            if self.browser.title != title:
                print("\nIniciando o LinkedIn bot\n")
                break
            else:
                time.sleep(1)
                print("\nPor favor faça o login novamente\n")

    def fill_data(self):
        self.browser.set_window_size(0, 0)
        self.browser.set_window_position(2000, 2000)
        os.system("reset")

        self.position = position
        self.location = "&location=" + location
        self.resumeloctn = resumeloctn
        print(self.resumeloctn)

    def start_apply(self):
        self.fill_data()
        self.applications_loop()

    def applications_loop(self):

        count_application = 0
        count_job = 0
        jobs_per_page = 0

        os.system("reset")

        self.browser.set_window_position(0, 0)
        self.browser.maximize_window()
        self.browser, _ = self.next_jobs_page(jobs_per_page)
        print("\nProcurando vagas.. Aguarde..\n")

        while count_application < self.MAX_APPLICATIONS:

            # sleep to make sure everything loads, add random to make us look human.
            time.sleep(random.uniform(2.5, 3.5))
            self.load_page(sleep=1)

            # get job links
            links = self.browser.find_elements_by_xpath(
                    '//div[@data-job-id]'
                    )

            # get job ID of each job link
            IDs = []
            for link in links :
                temp = link.get_attribute("data-job-id")
                jobID = temp.split(":")[-1]
                IDs.append(int(jobID))
            IDs = set(IDs)

            #UNIO Q JÁ TEM NNO ARQUIVO CSV COM ESSES NOVOS VER APEND
            # df = pd.read_csv("joblist.csv", usecols = [1])
            # last_applied = df.dropna()
            # last_id = last_applied.tolist()
            #
            # for j in last_id:
            #     self.appliedJobIDs.append(int(j))
            # print(self.appliedJobIDs)


            # remove already applied jobs
            jobIDs = [x for x in IDs if x not in self.appliedJobIDs]

            if len(jobIDs) == 0:
                jobs_per_page = jobs_per_page + 25 #0 + 25
                count_job = 0
                self.avoid_lock()
                self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)

            # loop over IDs to apply
            for jobID in jobIDs:
                #count_job += 1
                self.get_job_page(jobID)

                # get easy apply button
                button = self.get_easy_apply_button ()
                if button is not False:
                    string_easy = "* Tem Easy Apply "
                    button.click()
                    self.send_resume()
                    count_application += 1
                    count_job += 1 #eu coloquei aqui senão ele conta até os que não aplicou

                #let's register only jobs we applied for
                    position_number = str(count_job + jobs_per_page)
                    print("\nPosition {position_number}:\n {self.browser.title} \n {string_easy} \n")


                    # append applied job ID to csv file
                    timestamp = datetime.datetime.now()
                    # gerar um link
                    toWrite = [timestamp, jobID]
                    with open(self.filename, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow(toWrite)

                else:
                    string_easy = "* Não tem Easy Apply "

                # sleep every 20 applications
                if count_application % 20 == 0:
                    sleepTime = random.randint(500, 900)
                    print('\n\n****************************************\n\n')
                    print('Descansando - volto: ' + str(sleepTime/60) + 'min..')
                    print('\n\n****************************************\n\n')

                    #time.sleep (sleepTime)

                # go to new page if all jobs are done
                if count_job == len(jobIDs):
                    jobs_per_page = jobs_per_page + 25
                    count_job = 0
                    print('\n\n****************************************\n\n')
                    print('Indo para a próxima página, YEAAAHHH!!')
                    print('\n\n****************************************\n\n')
                    self.avoid_lock()
                    self.browser, jobs_per_page = self.next_jobs_page(jobs_per_page)
                    #QUANDO NÃO HA PROXIMA PAGINA, O QUE FAZER?
                #else len(jobIDs) < 25:
                 #   print('Há menos de 25 vagas!!!')
                  #  self.finish_apply()


        self.finish_apply() #SAI DO  WHILE caso ele atinja o numero máximo de aplicações

    def get_job_links(self, page):
        links = []
        for link in page.find_all('a'):
            url = link.get('href')
            if url:
                if '/jobs/view' in url:
                    links.append(url)
        return set(links)

    def get_job_page(self, jobID):
        #root = 'www.linkedin.com'
        #if root not in job:
        job = 'https://www.linkedin.com/jobs/view/'+ str(jobID)
        self.browser.get(job)
        self.job_page = self.load_page(sleep=0.5)
        return self.job_page

# o web scrapping deveria ser aqui

    def got_easy_apply(self, page):
        #button = page.find("button", class_="jobs-apply-button artdeco-button jobs-apply-button--top-card artdeco-button--3 ember-view")

        button = self.browser.find_elements_by_xpath(
                    '//button[contains(@class, "jobs-apply")]/span[1]'
                    )
        EasyApplyButton = button [0]
        if EasyApplyButton.text in "Easy Apply" :
            return EasyApplyButton
        else :
            return False
        #return len(str(button)) > 4

    def get_easy_apply_button(self):
        try :
            button = self.browser.find_elements_by_xpath(
                        '//button[contains(@class, "jobs-apply")]/span[1]'
                        )
            #if button[0].text in "Easy Apply" :
            EasyApplyButton = button [0]
        except :
            EasyApplyButton = False

        return EasyApplyButton

    def easy_apply_xpath(self):
        button = self.get_easy_apply_button()
        button_inner_html = str(button)
        list_of_words = button_inner_html.split()
        next_word = [word for word in list_of_words if "ember" in word and "id" in word]
        ember = next_word[0][:-1]
        xpath = '//*[@'+ember+']/button'
        return xpath

    def click_button(self, xpath):
        triggerDropDown = self.browser.find_element_by_xpath(xpath)
        time.sleep(random.uniform(1.5, 2.5))
        triggerDropDown.click()
        time.sleep(random.uniform(3, 2))

    # def send_resume(self):
    #     try:
    #         #self.browser.find_element_by_xpath('//*[@id="file-browse-input"]').send_keys(self.resumeloctn)
    #         submit_button = None
    #         time.sleep(5)
    #         while not submit_button:
    #         #while not submit_button:
    #             if language == "en":
    #                 submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']")))
    #                 #submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]")
    #             elif language == "es":
    #                 submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Enviar solicitud']")))
    #                 #submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Enviar solicitud')]")
    #             elif language == "pt":
    #                 submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Enviar candidatura']")))
    #                 #submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Enviar candidatura')]")
    #         submit_button.click()
    #
    #         time.sleep(random.uniform(2.5, 3.5))
    #
    #         #After submiting the application, a dialog shows up, we need to close this dialog
    #         #close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']")))
    #         time.sleep(5)
    #         #close_button.click()
    #
    #     except :
    #         print("Não deu certo")
    def send_resume(self):
        try:
            #self.browser.find_element_by_xpath('//*[@id="file-browse-input"]').send_keys(self.resumeloctn)
            #submit_button = None
            submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Submit application']")))
            #submit_button = self.browser.find_element_by_xpath("//*[contains(text(), 'Submit application')]")
            time.sleep(random.uniform(1.5, 3))

            submit_button.click()
            print("Curriculo enviado!!!! Yeahhh")

            #aquisim ele deveria escrever no arquivo

            time.sleep(random.uniform(2.5, 3.5))

            #After submiting the application, a dialog shows up, we need to close this dialog
            #close_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Dismiss']")))
            #time.sleep(5)
            #close_button.click()

        except :


            print("Não tem como enviar a candidatura")


    def load_page(self, sleep=1):
        scroll_page = 0
        while scroll_page < 4000:
            self.browser.execute_script("window.scrollTo(0,"+str(scroll_page)+" );")
            scroll_page += 200
            time.sleep(sleep)

        if sleep != 1:
            self.browser.execute_script("window.scrollTo(0,0);")
            time.sleep(sleep * 3)

        page = BeautifulSoup(self.browser.page_source, "lxml")
        return page

    def avoid_lock(self):
        x, _ = pyautogui.position()
        pyautogui.moveTo(x+200, None, duration=1.0)
        pyautogui.moveTo(x, None, duration=0.5)
        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(0.5)
        pyautogui.press('esc')

    def next_jobs_page(self, jobs_per_page):
        self.browser.get(
            "https://www.linkedin.com/jobs/search/?f_LF=f_AL&keywords=" +
            self.position + self.location + "&start="+str(jobs_per_page))
        self.avoid_lock()
        self.load_page()
        return (self.browser, jobs_per_page)

    def finish_apply(self):
        self.browser.close()

if __name__ == '__main__':

    # set use of gui (T/F)

    #useGUI = True
    useGUI = False

    # use gui
    if useGUI == True:

        app = loginGUI.LoginGUI()
        app.mainloop()

        #get user info info
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

    # no gui
    if useGUI == False:

        username = 'XXX@gmail.com'
        password = 'XXX'
        language = 'en'
        position = 'python'
        location = 'Campinas, São Paulo, Brazil'
        resumeloctn = open(r'C:\Users\Debora Oliveira...')

    # print input
    print("\nThese is your input:")

    print(
        "\nUsername:  "+ username,
        "\nPassword:  "+ password,
        "\nLanguage:  "+ language,
        "\nPosition:  "+ position,
        "\nLocation:  "+ location
        )

    print("\nVamos procurar emprego!\n")

    # get list of already applied jobs
    filename = 'joblist.csv'
    headers = "Data,ID\n"
    try:
        df = pd.read_csv(filename, header=headers)
        appliedJobIDs = list (df.iloc[:,1])
    except:
        appliedJobIDs = []

    # start bot
    bot = EasyApplyBot(username, password, language, position, location, resumeloctn, appliedJobIDs, filename)
    bot.start_apply()


 #References
 #The original code: https://github.com/nicolomantini/LinkedIn-Easy-Apply-Bot
