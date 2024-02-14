from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
import progressbar

class Bot:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

    def login(self, username, password) -> None:
        self.browser.find_element(By.NAME, "username").send_keys(username)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.browser.find_element(By.XPATH, "//button[@type='submit']").click()
        sleep(2)
        self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div").click()
        self.browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]").click()
        print("\nSuccessfully logged in to Instagram...")
        
    def send_messages(self, namelist=None, message="This is a test message.") -> None:
        """
        Sends messages to a list of Instagram usernames.

        Args:
            namelist (list): List of Instagram usernames to send messages to. Defaults to an empty list.
            message (str): The message to send. Defaults to "This is a test message."

        Returns:
            None
        """
        if namelist is None:
            namelist = []
        message = message.splitlines()

        print("\n")
        bar = progressbar.ProgressBar(maxval=20 if len(namelist) > 20 else len(namelist), widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
        bar.start()
        num = 0
        bar_value = 0
        updates = list(range(0, len(namelist), len(namelist)//20 if len(namelist) > 20 else 1))
        updates.append(len(namelist))
        for name in namelist:
            self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/div/div/span/div/a/div").click()
            self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div").click()
            ActionChains(self.browser)\
            .pause(1)\
            .send_keys("@" + name)\
            .send_keys(Keys.RETURN)\
            .perform()
            element = self.browser.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div")
            sleep(2)
            elements = element.find_elements(By.TAG_NAME, "div")
            elements_text = [text.split("\n")[1] for text in [element.text for element in elements][::15]]
            # 'bria black🌷\nbriacblack', 'bria black🌷\nbriacblack', 'bria black🌷\nbriacblack', 'bria black🌷\nbriacblack', '', '', 'bria black🌷\nbriacblack', 'bria black🌷\nbriacblack', 'bria black🌷\nbriacblack', 'bria black🌷', '', '', '', '', '', 'BRIA BLACK\nbriablack'
            element = None
            for (i, e) in enumerate(elements_text):
                if e == name:
                    element = elements[i*15]
                    break
            assert element is not None, 'Invalid username in list of usernames'
            element.click()
            self.browser.find_element(By.XPATH, "/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]").click()
            for mes in message:
                if mes == "/NEWMESSAGE":
                    ActionChains(self.browser)\
                    .pause(1)\
                    .send_keys(Keys.RETURN)\
                    .perform()
                else:
                    ActionChains(self.browser)\
                    .pause(1)\
                    .send_keys(mes)\
                    .key_down(Keys.SHIFT)\
                    .send_keys(Keys.RETURN)\
                    .key_up(Keys.SHIFT)\
                    .perform()
            ActionChains(self.browser)\
                    .pause(1)\
                    .send_keys(Keys.RETURN)\
                    .perform()
                
            num += 1
            if num in updates:
                bar_value += 1
                bar.update(bar_value)
            if num == len(namelist):
                sleep(2)
                print(f"\n\nFinished.\n{len(namelist)} messages sent.\n")
                exit()
            sleep(10)
            self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/div/span/div/a/div").click()
            sleep(10 + random.randint(0,20))
            if num % 10 == 0:
                sleep(2 * 3600)