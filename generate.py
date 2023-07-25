import requests
import json
import datetime

ENDPOINT = "https://www.speedrun.com/api/v1/"
URL = ENDPOINT + "leaderboards/m1mxxw46/category/9kv98382?embed=players"


def main():
    return_list = []

    r = requests.get(URL)

    runs = json.loads(r.text)["data"]

    info = json.load(open("info.json"))

    list_of_checked = []

    for x in info["times"]:
        run_obj = {
            "place": x["place"],
            "time": x["time"]
        }

        run = {}

        for y in runs["runs"]:
            if y["run"]["id"] == x["id"]:
                run = y["run"]
                break

        moon_count = "000"
        milliseconds = str(run["times"]["primary_t"]).split(".")
        if len(milliseconds) > 1:
            moon_count = milliseconds[1]
            while len(moon_count) < 3:
                moon_count += "0"

        run_obj["moons"] = str(int(moon_count)).zfill(3)
        run_obj["video"] = run["weblink"]
        run_obj["date"] = run["date"]

        for y in runs["players"]["data"]:
            if y["id"] == run["players"][0]["id"]:
                run_obj["player_name"] = y["names"]["international"]
                break

        version = run["values"]["onv6y608"]

        for y in info["variables"]:
            if y["id"] == version:
                run_obj["version"] = y["value"]
                break

        return_list.append(run_obj)
        list_of_checked.append(x["id"])

    for x in runs["runs"]:
        if x["run"]["id"] in list_of_checked:
            continue
        
        run_obj = {
            "place": x["place"],
            "video": x["run"]["weblink"],
            "date": x["run"]["date"]
        }

        moon_count = "000"
        milliseconds = str(x["run"]["times"]["primary_t"]).split(".")
        if len(milliseconds) > 1:
            moon_count = milliseconds[1]
            while len(moon_count) < 3:
                moon_count += "0"

        run_obj["moons"] = str(int(moon_count)).zfill(3)

        for y in runs["players"]["data"]:
            if y["id"] == x["run"]["players"][0]["id"]:
                run_obj["player_name"] = y["names"]["international"]
                break


        found = False
        for y in info["times"]:
            if y["id"] == x["run"]["id"]:
                run_obj["time"] = y["time"]
                found = True
                break

        if not found:
            run_obj["time"] = "-"

        version = x["run"]["values"]["onv6y608"]

        for y in info["variables"]:
            if y["id"] == version:
                run_obj["version"] = y["value"]
                break

        return_list.append(run_obj)
    
    return return_list