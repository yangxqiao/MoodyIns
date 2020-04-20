import urllib.request, json 
# urllib.request.urlopen("https://www.instagram.com/p/B_L3uA2Fzma/?__a=1") as url:
#     data = json.loads(url.read().decode())
#     print(data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"])

url = urllib.request.urlopen("https://www.instagram.com/p/B_L3uA2Fzma/?__a=1")
data = json.loads(url.read().decode())
print(data["graphql"]["shortcode_media"]["edge_media_to_caption"]["edges"][0]["node"]["text"])
