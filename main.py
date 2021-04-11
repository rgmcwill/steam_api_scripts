import dotenv, os, pprint, requests, urllib, json

dotenv.load_dotenv()

cache_path = '.cache/game_lookup.json'
output_path = 'output/'

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
    response = make_call('ISteamUserStats', 'GetPlayerAchievements', 'v1', {'key' : key, 'appid' : gameid, 'steamid' : player_id})
    player_achevement_dic = response.json()

    player_achevements = player_achevement_dic['playerstats'].get('achievements')
    player_achevement_success = player_achevement_dic['playerstats'].get('success')
    player_achevements_lookup = {}
    if player_achevement_success and player_achevements != None:
        for ach in player_achevements:
            player_achevements_lookup.update({ach['apiname'] : True if ach['achieved'] else False})
    else:

        print(player_achevement_dic['playerstats'].get('error') if player_achevement_dic['playerstats'].get('error') else 'Requested app has no achevements')
    # ---------------------------------------

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
                    if v.get('description') != None:
                        description = v.get('description')
                    else:
                        description = None
                    dic_to_add = {
                        'displayName' : v['displayName'],
                        'description' : description
                    }
                    internal_aid_to_text_aid.update({k: dic_to_add})

    # ---------------------------------------

    aid_to_per = {}
    achievement_percentage = dic.get('achievementpercentages')
    if achievement_percentage != None or player_achevements != None:
        for i in dic['achievementpercentages']['achievements']:
            ach_dets = internal_aid_to_text_aid[i['name']]
            dic_to_add = {
                'name' : ach_dets['displayName'],
                'discription' : ach_dets['description'],
                'percent' : i['percent'],
                'has' : player_achevements_lookup[i['name']] if player_achevement_success else  None
            }
            aid_to_per.update({i['name']: dic_to_add})

        main_dic[gameid]['achievements'] = aid_to_per

# --------------------------------------------------------------------------------------------------------------------

if not os.path.exists(output_path):
    os.mkdir(output_path)
with open(output_path + player_id + '.json', 'w') as outfile:
    json.dump(main_dic, outfile)
