import dotenv, os, pprint, requests, urllib

dotenv.load_dotenv()

key = os.getenv('STEAM_API_KEY')
base_url = 'http://api.steampowered.com/'
interface = 'ISteamUserStats'
method = 'GetSchemaForGame'
version = 'v1'
seperator = '/'

appid = 413150

qparams = {
    'key' : key,
    'appid' : appid
}
 
url = (base_url + seperator.join([interface, method, version]) + '/?' + urllib.parse.urlencode(qparams))

response = requests.get(url)
game_dic = response.json()
# pprint.pprint(response.json())

achievements = game_dic['game']['availableGameStats']['achievements']
for k,v in achievements.items():
    print(v['displayName'])