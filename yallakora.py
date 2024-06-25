#Import libraries.
import requests
import csv
from bs4 import BeautifulSoup
import json

#Get input from user
date = input("Enter a date in this format(MM/DD/Year)\n")

#Make a connection with the website.
page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

#Checke The connection
if page:
    print("✔Page connected✔")

#This is the main function.
def main(page):
    #Create match_details list
    match_details = []
    #Get the content.
    src = page.content

    #Parse the content
    soup = BeautifulSoup(src, "lxml")
    championships = soup.find_all("div", {"class": "matchCard"})
    
    #Get the data and store it in variables and then in lists.
    def info(championships):
        championship_title = championships.contents[1].find("a", {"class": "tourTitle"}).find("h2").text.strip()
        all_matches_finished= championships.contents[3].find_all("div", {"class": "item finish liItem"})
        all_matches_now= championships.contents[3].find_all("div", {"class": "item now liItem"})
        all_matches_future= championships.contents[3].find_all("div", {"class": "item future liItem"})
        
        all_matches = []
        if all_matches_finished != []:
            for i in range(len(all_matches_finished)):
                all_matches.append(all_matches_finished[i])
        if all_matches_now != []:
            for i in range(len(all_matches_now)):
                all_matches.append(all_matches_now[i])
        if all_matches_future != []:
            for i in range(len(all_matches_future)):
                all_matches.append(all_matches_future[i])

        num_matches = len(all_matches)
        for x in range(num_matches):
            teamA = all_matches[x].find("div", {"class": "teamA"}).text.strip()
            teamB = all_matches[x].find("div", {"class": "teamB"}).text.strip()

            match_result = all_matches[x].find("div", {"class": "MResult"}).find_all("span", {"class", "score"})
            score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
            
            match_time = all_matches[x].find("div", {"class": "MResult"}).find("span", {"class": "time"}).text.strip()

            match_details.append({"نوع البطولة": championship_title, "الفريق الأول": teamA, "الفريق الثاني": teamB, "موعد المباراة": match_time, "نتيجة المباراة": score})

    for x in range(len(championships)):
        info(championships[x])

    keys = match_details[0].keys()
    #Create CSV file.
    with open("C:\\Users\\Abdallah Medhat\\PycharmProjects\\Webscrabing Trainings\\Yalla.csv", "w", newline="", encoding='utf-8') as file:
        dict_w = csv.DictWriter(file, keys)
        dict_w.writeheader()
        dict_w.writerows(match_details)
        print("✔ CSV file created ✔")

    #Create JSON file.
    with open("Yalla.json", "w", encoding="utf-8") as jfile:
        json.dump(match_details[0], jfile, indent=4, ensure_ascii = False)
        print("✔ Json file created ✔")
    
main(page)
#Done.😊