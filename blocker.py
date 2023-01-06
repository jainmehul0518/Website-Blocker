# NOTE::A web driver is a interface that allows you to remotely command your web browser
# Script for blocking websites included in websites.txt during working hours of startHour am to 4 pm
from datetime import datetime, timedelta
import webbrowser
import argparse
import pause
import atexit

#global variables
is_blocked = False
firefox_path = "open -a /Applications/Firefox.app %s"
website_names = []
#argument handling
parser = argparse.ArgumentParser()
parser.add_argument("-startHour", dest="startHour", help="Please specify the starting hour (0-23) of study time.")
parser.add_argument("-endHour", dest="endHour", help="Please specify the ending hour (0-23) of study time.")
args = parser.parse_args()

# validate startHour and endHour arguments
def validate_time():
    global startHour, endHour
    try:
        startHour = int(args.startHour)
        endHour = int(args.endHour)
    except:
        print("Please specify an integer for the startHour and endHour")
        exit()
    if (startHour < 0 or startHour >= 24):
        print("Please specify a valid hour from 0 to 23 for startHour")
        exit()
    if (endHour < 0 or endHour >= 24):
        print("Please specify a valid hour from 0 to 23 for endHour")
        exit()

# remove redirects from /etc/hosts file
def clean_hosts_file(website_names):
    with open("/etc/hosts","r+") as f:
        old_file = f.readlines()
        f.seek(0)
        f.truncate()
        for line in old_file:
            if not any(website in line for website in website_names) and line != '\n':
                f.write(line)

# register clean_hosts_file as atexit function, called whenever Python-handled exception occurs or main function finishes running
atexit.register(clean_hosts_file, website_names)

def main():
    global is_blocked
    global firefox_path
    global website_names
    
    validate_time()
    
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
    if cur_hour >= startHour and cur_hour <= endHour:
        is_blocked = False
    else:
        is_blocked = True

    while True:
        cur_time = datetime.now().replace(minute=0,second=0, microsecond=0) # get current time rounded to current hour
        cur_hour = cur_time.hour
        if not is_blocked and cur_hour >= startHour and cur_hour <= endHour:
            with open("/etc/hosts",'a') as f:
                for name in website_names:
                   f.write("127.0.0.1 {}\n".format(name))
            is_blocked = True
        elif is_blocked and (cur_hour < startHour or cur_hour > endHour):
            clean_hosts_file(website_names)
            is_blocked = False
        pause.until(cur_time + timedelta(hours=1))

if __name__ == "__main__":
    main()