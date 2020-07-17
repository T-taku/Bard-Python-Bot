import json
import base64
url = "https://texttospeech.googleapis.com/v1/text:synthesize"


async def request_tts(access_token, session, req):
    headers = {
        "Authorization": "Bearer " + access_token[:-1],
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    body = {
        "input": {
            "text": req.text
        },
        "voice": {
            "languageCode": convert_lang(req.lang),
            "name": convert_voice(req.lang, req.voice),
        },
        "audioConfig": {
            "audioEncoding": "LINEAR16",
            "speakingRate": req.speed,
            "sampleRateHertz": 48000,
            "pitch": req.pitch,
        }
    }

    async with session.post(url, json=body, headers=headers) as r:
        text = await r.text()
    res = json.loads(text)
    content = base64.b64decode(res["audioContent"])
    return remove_header(content)


def remove_header(content):
    return content[44:]


def convert_lang(lang):
    if lang == "ja":
        return "ja-JP"
    else:
        return "en-US"


def convert_voice(lang, voice):
    if lang == "ja":
        return f"ja-JP-Wavenet-{voice}"
    else:
        return f"en-US-Wavenet-{voice}"

