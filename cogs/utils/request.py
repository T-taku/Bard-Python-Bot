import aiohttp
import json
import os
import base64
url = "https://texttospeech.googleapis.com/v1/text:synthesize"


async def request_tts(session, text, speed, pitch, lang, voice):
    headers = {
        "Authorization": "Bearer " + os.environ.get('tts'),
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    body = {
        "input": {
            "text": text
        },
        "voice": {
            "languageCode": lang,
            "name": voice,
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "speakingRate": speed,
            "sampleRateHertz": 48000,
            "pitch": pitch,
        }
    }

    async with session.post(url, json=body, headers=headers) as r:
        res = json.loads(await r.text())

    content = base64.b64decode(res["audioContent"])
    return remove_header(content)


def remove_header(content):
    return content[44:]



