from facebook_scraper import get_posts
from dotenv import load_dotenv, find_dotenv
import json, datetime, requests, os, sys

load_dotenv(find_dotenv())
PAGE_NAME = os.getenv("PAGE_NAME")
PAGE_PROFILE_URL = os.getenv("PAGE_PROFILE_URL")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

def write_json(new_data):
    with open("log.json",'r+') as file:
        file_data = json.load(file)
        file_data["posts"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def discordsend(user, data):
    ilog = open("log.json", "r")
    ilogged = json.loads(ilog.read())
    oldmedcode = ilogged["posts"]
    newmedcode = data["post_id"]
    if newmedcode not in oldmedcode:
        postid = data["post_id"]
        if postid == None:
            postid = "NotFound"

        profileurl = PAGE_PROFILE_URL
        if PAGE_PROFILE_URL == None:
            profileurl = "https://cdn.discordapp.com/attachments/839327846773162014/999566573339676703/eFacebook.png"
        medurl = data["w3_fb_url"]

        if medurl == None:
            medurl = "https://facebook.com/" + data['post_id']
            if medurl == None:
                medurl = " "

        medcaption = data["text"]
        if medcaption == None:
            medcaption = " "

        posttime_ist = (data['time']).timestamp() - 19800
        medtime = datetime.datetime.fromtimestamp(posttime_ist).strftime("%Y-%m-%dT%H:%M:00.000Z")

        if data['image'] != None:
            medpreview = data['image']
            medname = "Image"
        elif data['video'] != None:
            medpreview = data['video_thumbnail']
            medname = "Video"  

        #Template of Discord Webhooks from Python - https://gist.github.com/Bilka2/5dd2ca2b6e9f3573e0c2defe5d3031b2
        data = {
            "content" : "",
            "username" : "Social Media",
            "avatar_url" : "https://media.discordapp.net/attachments/839327846773162014/964543848200159302/ThisIsBusiness.png"
        }
        data["embeds"] = [
            {
                "author" : {
                    "name" :  user,
                    "url" : "https://www.facebook.com/"+ user,
                    "icon_url" : profileurl
                },
                "color" : "4351922",
                "url" : medurl,
                "timestamp" : medtime,
                "image" : {
                    "url" : medpreview
                },
                "fields": [
                    {
                      "name": user + " uploaded a " + medname + ": " + medurl,
                      "value": medcaption
                    }
                ],
                "footer" : {
                    "text" : "Facebook",
                    "icon_url" : "https://cdn.discordapp.com/attachments/839327846773162014/999566573339676703/eFacebook.png"
                }

            }
        ]

        result = requests.post(DISCORD_WEBHOOK, json = data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload for "+ user +" was delivered successfully, with code {}.".format(result.status_code))
            return postid
    else:
        print("No new Media from " + user)
        return None

def main():
    print(" "*5 + "Facebook to Discord" + " "*5)
    print("Getting Info for "+ PAGE_NAME)

    try:
        i = 0
        for post in get_posts(PAGE_NAME, pages=3, cookies="cookiefile.txt"):
            if i > 0:
                break
            else:
                thepost = post
                i += 1
        if (DISCORD_WEBHOOK==None) or (PAGE_NAME==None):
            print("Correct Environment Variables not provided!")
        else:
            
            retcode = discordsend(PAGE_NAME, thepost)
            if retcode != None:
                print("The Post with ID " + retcode + " has been logged.")
                write_json(retcode)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        pass

main()