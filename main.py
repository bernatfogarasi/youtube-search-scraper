import requests
import json
import yaml

def search(text):
    words = "+".join(text.split())
    url = f"https://www.youtube.com/results?search_query={words}&sp=EgIQAQ%253D%253D"
    response = requests.get(url)
    return [get_video(video) for video in get_videos(get_json(response.text))]

def get_json(html):
    START_TEXT = "var ytInitialData = "
    END_TEXT = "</script>"
    reduced_html = html[html.find(START_TEXT) + len(START_TEXT):]
    json_text = reduced_html[:reduced_html.find(END_TEXT)].strip()[:-1]
    return yaml.load(json_text, Loader=yaml.FullLoader)

def get_videos(data):
    data = data["contents"]["twoColumnSearchResultsRenderer"]
    data = data["primaryContents"]["sectionListRenderer"]["contents"]
    return data[0]["itemSectionRenderer"]["contents"]

def get_video(data):
    data = data["videoRenderer"]
    video = {
        "id": data["videoId"],
        "title": data["title"]["runs"][0]["text"],
        "thumbnail": data["thumbnail"]["thumbnails"][-1]["url"],
        "channel": {
            "title": data["ownerText"]["runs"][0]["text"],
            "id": data["ownerText"]["runs"][0]["navigationEndpoint"]["browseEndpoint"]["browseId"],
            "thumbnail": data["channelThumbnailSupportedRenderers"]["channelThumbnailWithLinkRenderer"]["thumbnail"]["thumbnails"][-1]["url"]
        }

    }
    video["url"] = f"https://www.youtube.com/watch?v={video['id']}"
    video["channel"]["url"] = f"https://www.youtube.com/channel/{video['channel']['id']}"
    return video

def print_json(data):
    print(json.dumps(data, indent=4))

def main():
    results = search("house music")
    print_json(results)
    return results

if __name__ == "__main__":
    main()