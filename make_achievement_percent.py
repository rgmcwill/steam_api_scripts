import dotenv, os, pprint, requests, urllib

dotenv.load_dotenv()

key = os.getenv('STEAM_API_KEY')
base_url = 'http://api.steampowered.com/'
interface = 'ISteamUserStats'
method = 'GetGlobalAchievementPercentagesForApp'
version = 'v2'
seperator = '/'

appid = 413150

qparams = {
    'key' : key,
    'gameid' : appid
}
 
url = (base_url + seperator.join([interface, method, version]) + '/?' + urllib.parse.urlencode(qparams))

response = requests.get(url)
dic = response.json()

a_dic = {}
for i in dic['achievementpercentages']['achievements']:
    a_dic.update({i['name']: i['percent']})

pprint.pprint(a_dic)
