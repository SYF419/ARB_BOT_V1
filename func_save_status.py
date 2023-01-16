import json

#save status
def save_status(dict):
    try:
        with open("status.json","w") as fp:
            json.dump(dict, fp, indent=4)
    except:
        pass
    # print(dict)
