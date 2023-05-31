import requests

def create_room():
    url = "https://easyedu.metered.live/api/v1/room"

    url_key = url + "/?secretKey=Kxy0vx2zjvCvznvdE3r0jiufv2jQglbxh60XsFBi8HSDw2RN"

    payload = {
        "privacy": "public",
        "ejectAtRoomExp": False,
        "enableRequestToJoin": True,
        "enableChat": True,
        "enableScreenSharing": True,
        "joinVideoOn": False,
        "joinAudioOn": False,
        "recordRoom": False,
        "audioOnlyRoom": False
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url_key, json=payload, headers=headers)

    return response.text

