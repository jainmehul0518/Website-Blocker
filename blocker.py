#TODO::allow user to specify working hours
# Script for blocking websites included in websites.txt during working hours of 8 am to 4 pm
from datetime import datetime
import webbrowser

is_blocked = False
firefox_path = "open -a /Applications/Firefox.app %s"

def main():
    global is_blocked
    global firefox_path
    website_names = []
    # create list of websites to block
    with open("websites.txt",'r') as f:
        for website in f:
            website = website.strip()
            website_names.append(website)

    try:
        webbrowser.get(firefox_path).open("https://google.com")
    except:
        print("Can't access firefox browser. Please check if firefox is downloaded on your machine.")
        exit()

    cur_hour = datetime.now().hour
    if cur_hour >= 8 and cur_hour <= 15:
        is_blocked = False
    else:
        is_blocked = True

    while True:
        cur_hour = datetime.now().hour
        if not is_blocked and cur_hour >= 8 and cur_hour <= 15:
            with open("/etc/hosts",'a') as f:
                for name in website_names:
                   f.write("127.0.0.1 {}\n".format(name))
            is_blocked = True
        elif is_blocked and (cur_hour < 8 or cur_hour > 15):
            with open("/etc/hosts","r+") as f:
                old_file = f.readlines()
                f.seek(0)
                f.truncate()
                for line in old_file:
                    if not any(website in line for website in website_names) and line != '\n':
                        f.write(line)
            is_blocked = False

if __name__ == "__main__":
    main()