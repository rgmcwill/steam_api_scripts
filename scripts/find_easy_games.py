import json, pprint, sys

percentage_threshold = 50.00
args = sys.argv

steam_person_info = None

with open(args[1]) as json_file:
    steam_person_info = json.load(json_file)

if steam_person_info == None:
    sys.exit()

averages = {}
for game_id, dets in steam_person_info.items():
    ach = dets['achievements']
    if ach != None:
        numb = 0
        total = 0
        for ach_id, ach_dets in ach.items():
            numb = numb + 1
            total = total + ach_dets['percent']
        if total or numb is not 0:
            averages.update({dets['name'] : total/numb})

sorted_tuples = sorted(averages.items(), key=lambda item: item[1])
pprint.pprint(sorted_tuples) 
