# By Sam Ehlers

import os
from absl import app
from absl import flags
from selenium import webdriver
from pages import Bot

FLAGS = flags.FLAGS
flags.DEFINE_string("username", None, "Username")
flags.DEFINE_string("password", None, "Password")
flags.DEFINE_string("users_file", "usernames.txt", "Users in a .txt file")
flags.DEFINE_string("message_file", "message.txt", "Message in a .txt file")

flags.mark_flag_as_required("username")
flags.mark_flag_as_required("password")

def main(argv):
    del argv

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(5)

    usr =  FLAGS.username
    passwd =  FLAGS.password

    with open(os.path.join(FLAGS.users_file), 'r', encoding='UTF-8') as f:
        users = f.read().splitlines()

    with open(os.path.join(FLAGS.message_file), 'r', encoding='UTF-8') as f:
        message = f.read()

    bot = Bot(browser)
    bot.login(usr, passwd)
    bot.send_messages(users, message)

if __name__ == '__main__':
    app.run(main)