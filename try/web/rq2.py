import requests
import json


# resp = requests.get('http://d2-wallpaperv3.ticktockapps.com/res/tag/category.json?app=wallhd-10000&device=iPod5%2C1&devicesize=640x1136&ios=8.3&sort=pop&thumb=305x543&version=5.0')
# dc = json.loads(resp.content)
# print(dc)

category="""Actors
Actresses
Animals
Anime
Art
Autumn
Basketball
Birthday
Black and White
Blue
Blur
Brands
Calendars
Cars
Cartoons
Cats
Celebrities
Colors
Country
Cute
Dogs
Fashion
Flower
Food
Football
Funny
Games
Girls
Holidays
Illustrations
Landscapes
Love
Monogram
Motivational
Movies
Music
Nature
Neon
Pink
Purple
Quotes
Sea
Sky
Soccer
Space
Spiritual
Sports
Spring
Summer
Sunset
TV Shows
Textures
Tree
USA
Winter"""

ls = category.split('\n')
print(ls)

