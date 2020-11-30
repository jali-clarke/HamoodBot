from bs4 import BeautifulSoup as BS
import requests
import re
import random
import json

# from instaloader import Instaloader, Profile, Hashtag

# L = Instaloader()


# def insta_profile(username):
#     url = f"https://instagram.com/{username}/"
#     response = requests.get(url)

#     if response.status_code != 404:
#         profile = Profile.from_username(L.context, username)

#         data = {
#             "url": url,
#             "pfp": profile.profile_pic_url,
#             "posts": profile.mediacount,
#             "followers": profile.followers,
#             "following": profile.followees,
#             "name": profile.full_name,
#             "bio": profile.biography,
#             "link": profile.external_url,
#         }

#         return True, data
#     else:
#         False, None


def covid_info(country):
    url = "https://www.worldometers.info/coronavirus/"
    if country == None:
        url = url
    else:
        url = "https://www.worldometers.info/coronavirus/country/" + str(country) + "/"

    try:
        data = requests.get(url)
        soup = BS(data.text, "html.parser")
        total = soup.find("div", class_="maincounter-number").text
        total = total[1 : len(total) - 2]
        other = soup.find_all("span", class_="number-table")
        try:
            recovered = other[2].text
            deaths = other[3].text
            deaths = deaths[1:]
        except IndexError:
            recovered = "N/A"
            deaths = "N/A"
        info = {
            "Total Cases": total,
            "Recovered Cases": recovered,
            "Total Deaths": deaths,
        }
    except Exception:
        info = {
            "Total Cases": "ERROR",
            "Recovered Cases": "ERROR",
            "Total Deaths": "ERROR",
        }

    return url, info


# def insta_scrapes(username):
#     url = f"https://www.instagram.com/{username}/"

#     r = requests.get(url)

#     if r.status_code != 404:
#         # profile = Profile.from_username(L.context, username)
#         json_m = re.search(r"window\._sharedData = (.*);</script>", r.text)
#         profile = json.loads(json_m.group(1))["entry_data"]["ProfilePage"][0][
#             "graphql"
#         ]["user"]

#         data = {
#             "url": url,
#             "pfp": profile["profile_pic_url_hd"],
#             "posts": profile["edge_owner_to_timeline_media"]["count"],
#             "followers": profile["edge_followed_by"]["count"],
#             "following": profile["edge_follow"]["count"],
#             "name": profile["full_name"],
#             "bio": profile["biography"],
#             "link": profile["external_url"],
#         }
#         return True, data
#     else:
#         return False, None


def scrape(imgURL, saveDir):
    img_data = requests.get(imgURL).content
    with open(saveDir, "wb") as handler:
        handler.write(img_data)

