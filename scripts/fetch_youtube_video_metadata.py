import requests
import re
import json
from time import sleep
from argparse import ArgumentParser

# function to extract video title and description using regex
def get_youtube_video_info(video_url):
    response = requests.get(video_url)
    if response.status_code == 200:
        html = response.text

        # extract the title using a regular expression
        title_search = re.search(r'"title":"(.*?)"', html)
        title = title_search.group(1) if title_search else "No title found"

        # extract the description using a regular expression
        description_search = re.search(r'"shortDescription":"(.*?)"', html)
        description = description_search.group(1).replace('\\n', '\n') if description_search else "No description found"
        # cleanup the description
        description = re.sub('\\n', ' ', description)

        # extract author using a regular expression
        author_search = re.search(r'"ownerChannelName":"(.*?)"', html)
        author = author_search.group(1) if author_search else "No author found"

        # prepare the JSON structure
        video_info = {
            "path": video_url,
            "embed": f"https://www.youtube.com/embed/{video_url.split('=')[1]}",
            "name": title,
            "author": author,
            "description": description
        }

        return json.dumps(video_info, indent=4)
    else:
        return f"Failed to retrieve video info, status code: {response.status_code}"

parser = ArgumentParser()
parser.add_argument("url", nargs="+", help="YouTube video URL(s)")
args = parser.parse_args()

# process each URL passed in the arguments
for video_url in args.url:
    # call the function with the provided URL
    video_json = get_youtube_video_info(video_url)
    print("{},".format(video_json))
    sleep(1) # sleep for 1 second to avoid being blocked by YouTube