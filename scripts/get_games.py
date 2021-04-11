import dotenv, os, pprint, requests, urllib

dotenv.load_dotenv()

key = os.getenv('STEAM_API_KEY')
player_id = os.getenv('PLAYER_ID')
base_url = 'http://api.steampowered.com/'
interface = 'IPlayerService'
method = 'GetOwnedGames'
version = 'v1'
seperator = '/'

qparams = {
    'key' : key,
    'steamid' : player_id
}
 
url = (base_url + seperator.join([interface, method, version]) + '/?' + urllib.parse.urlencode(qparams))

print(url)
response = requests.get(url)
dic = response.json()

for i in dic['response']['games']:
    print(i['appid'])
