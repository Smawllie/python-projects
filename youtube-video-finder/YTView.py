'''
Usage: YTView.py [title] [views] (need to edit)

This file takes in a Youtube search input and # views and returns a
list of Youtube videos with over that # of views

Example: (need to edit)
  YTView.py 4 Hour Instrumental --views 5000000
'''

# argparse is for command line input parsing
# build is for obtaining the YouTube Resource object
# HTTPError is for an error that I'm not sure is for yet
import argparse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Developer key is my own personal key, will need to change it later
DEVELOPER_KEY = '<API_KEY>'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def search(search_input):
  ''' (argparse.Namespace) --> dict {string, dict{string, string}}
  Given an argparse object containing search title and view count return a dictionary that maps video ids to a data dictionary, which maps the name of the data type to the value
  i.e.. search returns multiple <id> : {"title": <title>} in a dict
  e.g. {9bZkp7q19f0 : {"title": PSY - GANGNAM STYLE(강남스타일) M/V}}
  '''
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  
  # search_response is a dictionary. Details found here: https://developers.google.com/youtube/v3/docs/search/list#usage
  # Use the API explorer as well
  search_response = youtube.search().list(
    q=search_input.query,
    part='snippet',
    maxResults=25
  ).execute()

  id_to_data = dict()
  

  # If items key isn't found return []
  # Additionally make sure to only look at videos, not channels or playlists
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        dataType_to_value = dict()
        video_id = search_result["id"]["videoId"]
        video_title = search_result["snippet"]["title"]
        dataType_to_value["title"] = video_title
        id_to_data[video_id] = dataType_to_value
  return id_to_data

def addViewCount(id_to_data, minView=0):
  ''' (dict {string, dict {string, string}}, int) --> dict {string, dict {string, string}}
  Given a dictionary containing video elements, add the viewCount element only if it's greater than the minimum views (default is to add all viewcount). If it's less, delete the element
  i.e. 
  addViewCount(<id> : {"title": <title>})
  <id> : {"viewCount": <viewCount>, "title": <title>}
  e.g. with no viewCount of PSY's video before, the function returns
  9bZkp7q19f0 : {"title": PSY - GANGNAM STYLE(강남스타일) M/V, "viewCount": 3276910244}
  '''
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
  # Read docstring and developers.google if this doesn't make sense
  # Use list(id_to_data.keys()) instead of id_to_data because RuntimeError when deleting elements from a dictionary but not a list!
  for ID in list(id_to_data.keys()):
    video_data = youtube.videos().list(
      # statistics is the part that contains the viewCount
      # more info at https://developers.google.com/youtube/v3/docs/videos/list
      part="statistics",
      id=ID
    ).execute()
    viewCount = video_data["items"][0]["statistics"]["viewCount"]
    if int(viewCount) > minView:
      id_to_data[ID]["viewCount"] = viewCount
    else:
      del id_to_data[ID]
  return id_to_data

def addCommas(n):
  ''' (int) -> str
  Given a number return the number with commas added to make it more readable
  '''
  r = []
  # i is the index and n is the number
  # we flip the string so that we can add a comma every 3 numbers
  # enumerate is essentially a list of pairs (index, character)
  for i, n in enumerate(reversed(str(n))):
    # every 3rd character we add a comma
    if i and (not (i % 3)):
        r.insert(0, ',')
    r.insert(0, n)
  return ''.join(r)  


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--query', help='Search term', default='Gangnam')
  parser.add_argument('--views', help='Minimum views', default=100000000)
  args = parser.parse_args()

  try:
    id_to_data = addViewCount(search(args), args.views)
    for ID in id_to_data:
      output = id_to_data[ID]["title"] + "\n"
      output += "https://www.youtube.com/watch?v=" + ID + "\n"
      output += "Views: " + addCommas(int(id_to_data[ID]["viewCount"])) + "\n"
      print(output)

  except HttpError as e:
    print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
