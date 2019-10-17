import requests

league_id = 84769
year = 2019
url = "https://fantasy.espn.com/apis/v3/games/ffl/seasons/"+str(year)+"/segments/0/leagues/"+str(league_id)

k= """AEC3xjxm32Q0YdBpUeclFR5%2F6MKZZMBLIEATbjTIwi7A%2BdeocninX5iWmdp0p8jx%2FCpUo%2FZQ1MP5bEp63bR345MSTUElnk3I6R78D1AXBnnbwVlo5DMzoQr7kyRSTZns1bUxlP1woSvD6Mdty%2F2bPiYCmjr5f%2FT8XnV87qYg8DJOFdIUfDm74w6wHebyxyZZ%2BvWX56WyGSGPUMJ1xfuQaSFhwdKKrV%2BbPcKC%2B3FodydAEPbzzqll%2BuGCmX4S%2BVCt%2Frj6iHMJxJkoMwKsXeBKvdAn"""
cookies = {"swid": "98AFE6A0-F85D-4212-9FB4-17271326192A","espn_s2": k}

r = requests.get(url,cookies=cookies )
d = r.json()