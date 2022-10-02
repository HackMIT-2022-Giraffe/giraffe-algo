from email.mime import image
import fitz
import io
import base64
import os
from PIL import Image
from collections import defaultdict
from google.cloud import texttospeech
import openai


class PDF:
    def __init__(self, source: str, length: int, api_key=None):
        self.source = source
        self.length = length
        self.images, self.text = self.__extractFeatures()
        self.api_key = api_key

        print(self.api_key)
        

    def __extractFeatures(self):
        pdf_file = fitz.open(self.source)
        images = defaultdict(list)
        text = defaultdict(list)

        for page_index in range(len(pdf_file)):
                
            page = pdf_file[page_index]
            image_list = page.get_images()
            text_list = page.get_text()
            for text_value in text_list.split('\n '):
                if len(text_value) > 25:
                    text[page_index].append(text_value)



            for image_index, img in enumerate(image_list, start=1):
                xref = img[0]
                    
                base_image = pdf_file.extract_image(xref)
                if (base_image['width'] > 100 or base_image['height'] > 100):
                    images[page_index].append(base_image["image"])

                images[page_index].sort(key=len, reverse=True)
                images[page_index] = images[page_index][:min(3, len(images[page_index]))]

        print("Images and text have been properly loaded")

        return images, text

    def generateTranscript(self):
        openai.api_key = self.api_key
        
        transcript = list()

        for index in self.text:
            response = openai.Completion.create(
                        engine="text-davinci-002",
                        prompt='\n'.join(self.text[index]),
                        temperature=0.8,
                        max_tokens=600,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
            transcript.append(response.choices[0].text)

        return "\n".join(transcript)

class TTS:
    
    def __init__(self, text: str, api_key=None):
        self.text = text
        self.api_key = api_key

    def textToSpeech(self):
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.api_key
        client = texttospeech.TextToSpeechClient()
        
        text = self.text
        
        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            name='en-GB-Wavenet-B',
            language_code='en-GB'
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open('audio.mp3','wb') as output:
            output.write(response.audio_content)
        
        bytes = io.BytesIO(open('audio.mp3', 'rb').read())

        return response.audio_content
