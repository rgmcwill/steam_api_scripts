import dotenv, os, pprint, requests, urllib, json

dotenv.load_dotenv()

cache_path = '.cache/game_lookup.json'
output_path = 'output.json'

key = os.getenv('STEAM_API_KEY')
player_id = os.getenv('PLAYER_ID')
base_url = 'http://api.steampowered.com/'
seperator = '/'

def make_call(interface, method, version, qparams):
    url = (base_url + seperator.join([interface, method, version]) + '/?' + urllib.parse.urlencode(qparams))
    return requests.get(url)

id_to_game_dic = {}
if not os.path.exists(cache_path) or os.stat(cache_path).st_size == 0:
    print('fetching data')
    response = make_call('ISteamApps', 'GetAppList', 'v2', {'key' : key})
    dic = response.json()

    for i in dic['applist']['apps']:
        id_to_game_dic.update({i['appid']:i['name']})

    with open(cache_path, 'w') as outfile:
        json.dump(id_to_game_dic, outfile)
else:
    print('reading cached data')
    with open(cache_path) as json_file:
        id_to_game_dic = json.load(json_file)

# ------------------------------------------------------------------------------------------------------------------

response = make_call('IPlayerService', 'GetOwnedGames', 'v1', {'key' : key, 'steamid' : player_id})
dic = response.json()

games = []
for i in dic['response']['games']:
    games.append(i['appid'])

# ------------------------------------------------------------------------------------------------------------------

main_dic = {}
for i in games:
    name = id_to_game_dic.get(str(i))
    if name != None:
        main_dic.update({i:{'name': name, 'achievements': None}})
    else:
        main_dic.update({i:{'name': None, 'achievements': None}})

# ------------------------------------------------------------------------------------------------------------------

for gameid in main_dic.keys():
    response = make_call('ISteamUserStats', 'GetGlobalAchievementPercentagesForApp', 'v2', {'key' : key, 'gameid' : gameid})
    dic = response.json()

    # ---------------------------------------
    response = make_call('ISteamUserStats', 'GetSchemaForGame', 'v1', {'key' : key, 'appid' : gameid})
    game_dic = response.json()

    internal_aid_to_text_aid = {}
    a_game = game_dic.get('game')
    if a_game != None:
        game_stats = a_game.get('availableGameStats')
        if game_stats != None:
            achievements = game_stats.get('achievements')
            if achievements != None:
                for k,v in achievements.items():
                    internal_aid_to_text_aid.update({k: v['displayName']})

    # ---------------------------------------

    aid_to_per = {}
    achievement_percentage = dic.get('achievementpercentages')
    if achievement_percentage != None:
        for i in dic['achievementpercentages']['achievements']:
            aid_to_per.update({internal_aid_to_text_aid[i['name']]: i['percent']})

        main_dic[gameid]['achievements'] = aid_to_per

# --------------------------------------------------------------------------------------------------------------------

with open(output_path, 'w') as outfile:
        json.dump(main_dic, outfile)