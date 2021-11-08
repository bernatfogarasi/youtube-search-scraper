import requests
from bs4 import BeautifulSoup
import json
import yaml

def print_json(data):
    print(json.dumps(data, indent=4))

def search(text):
    words = "+".join(text.split())
    response = requests.get(f"https://www.youtube.com/results?search_query={words}&sp=EgIQAQ%253D%253D")
    return response.text

def read(name):
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

def get_json(html):
    START_TEXT = "var ytInitialData = "
    END_TEXT = "</script>"
    start_index = html.find(START_TEXT)
    reduced_html = html[start_index + len(START_TEXT):]
    end_index = reduced_html.find(END_TEXT)
    json_text = reduced_html[:end_index].strip()[:-1]
    return yaml.load(json_text, Loader=yaml.FullLoader)

def get_videos(data):
    data = data["contents"]["twoColumnSearchResultsRenderer"]
    data = data["primaryContents"]["sectionListRenderer"]["contents"]
    return data[0]["itemSectionRenderer"]["contents"]

def get_video(data):
    data = data["videoRenderer"]
    return {
        "id": data["videoId"],
        "title": data["title"]["runs"][0]["text"],
        "thumbnail": data["thumbnail"]["thumbnails"][-1]["url"],
        "channel": {
            "title": data["ownerText"]["runs"][0]["text"],
            "id": data["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            "thumbnail": data["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
        }

    }

def main():
    html = search("hear me now")
    data = get_json(html)
    videos = get_videos(data)
    print(len(videos))
    results = []
    for video in videos:
        video = get_video(video)
        results.append(video)
    print_json(results)
    return results

if __name__ == "__main__":
    main()