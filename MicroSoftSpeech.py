# -*- coding: utf-8 -*-
import requests, time
from xml.etree import ElementTree

class TextToSpeech(object):
    def __init__(self, subscription_key,file_name,context):
        self.subscription_key = subscription_key
        self.tts = context
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None
        self.file_name = file_name
        
    def get_token(self):
        fetch_token_url = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
    
    def save_audio(self):
        base_url = 'https://eastasia.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3',
            'User-Agent': 'TTSforRespeaker'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-TW')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'zh-TW')
        voice.set('name', 'Microsoft Server Speech Text to Speech Voice (zh-TW, Yating, Apollo)')
        voice.text = self.tts
        body = ElementTree.tostring(xml_body)
    
        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open(self.file_name, 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) + "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) + "\nSomething went wrong. Check your subscription key and headers.\n")
    
if __name__ == "__main__":
    subscription_key = "your_key"
    app = TextToSpeech(subscription_key,'test.mp3','你好')
    app.get_token()
    app.save_audio()
