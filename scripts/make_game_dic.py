import dotenv, os, pprint, requests, urllib, json

dotenv.load_dotenv()


cache_path = '../.cache/game_lookup.json'

key = os.getenv('STEAM_API_KEY')
base_url = 'http://api.steampowered.com/'
interface = 'ISteamApps'
method = 'GetAppList'
version = 'v2'
seperator = '/'

qparams = {
    'key' : key
}
 
url = (base_url + seperator.join([interface, method, version]) + '/?' + urllib.parse.urlencode(qparams))

game_dic = {}
if not os.path.exists(cache_path) or os.stat(cache_path).st_size == 0:
    print('fetching data')
    response = requests.get(url)
    dic = response.json()

    for i in dic['applist']['apps']:
        game_dic.update({i['appid']:i['name']})

    with open(cache_path, 'w') as outfile:
        json.dump(game_dic, outfile)
else:
    print('reading cached data')
    with open(cache_path) as json_file:
        game_dic = json.load(json_file)

print(len(game_dic))