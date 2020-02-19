# -*- coding: utf-8 -*-
"""
    __init__

    A library to get text to speech from Google cloud engine.

    See: https://cloud.google.com/text-to-speech/docs/basics

"""

try:
    import simplejson as json
except ImportError:
    import json
import logging

import base64

try:
    import httplib
except ImportError:
    import http.client as httplib


class BadRequestException(Exception):
    def __init__(self, message):
        self.message = "{} {}".format(
            message.status,
            message.reason
            )
        super(
            BadRequestException,
            self
            ).__init__(
                self.message
                )
        
class AuthException(Exception):
    def __init__(self, message):
        self.message = "{} {}".format(
            message.status,
            message.reason
            )
        super(
            AuthException,
            self
            ).__init__(
                self.message
                )
        
class LanguageException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
            )
        super(
            LanguageException,
            self
            ).__init__(
                self.message
                )

class GeneralException(Exception):
    def __init__(self, message):
        self.message = "{}".format(
            message
            )
        super(
            GeneralException,
            self
            ).__init__(
                self.message
                )


class Translator(object):
    """
    Implements API for the Google Cloud TTS service
    """

    def __init__(self, client_secret, debug=False):
        """
        :param clien_secret: The API key provided by Azure
        :param debug: If true, the logging level will be set to debug
        """
        self.base_host = 'texttospeech.googleapis.com'
        self.base_path = '/v1beta1/text:synthesize'
        self.client_secret = client_secret
        self.debug = debug
        self.logger = logging.getLogger(
            "bingtts"
            )
        self.access_token = None
        if self.debug:
            self.logger.setLevel(
                level=logging.DEBUG
                )
        
   
    def call(self, headerfields, path, body):
        """
        Calls Bing API and retrieved audio
        
        :param headerfields: Dictionary of all headers to be sent
        :param path: URL path to be appended to requests
        :param body: Content body to be posted
        """
        
        # Post to Bing API
        pathparams = "?key={}".format(
            self.client_secret
            )
        urlpath = "/".join(
            [
                self.base_path,
                pathparams
            ]
            )
        conn = httplib.HTTPSConnection(
            self.base_host
            )
        conn.request(
            method="POST",
            url=urlpath,
            headers=headerfields,
            body=body.encode('utf-8')
            )
        resp = conn.getresponse()
        # If token was expired, get a new one and try again
        if int(resp.status) == 401:
            raise AuthException(
                resp
                )
        
        # Bad data or problem, raise exception    
        if int(resp.status) != 200:
            raise BadRequestException(
                resp
                )
        try:
            payload = json.loads(
                resp.read().decode('utf-8')
                )
        except Exception as e:
            raise GeneralException(
                e
                )
        return base64.b64decode(
            payload['audioContent']
            )
        
    def speak(self, text, lang, voice, fileformat="LINEAR16", samplerate=16000):
        """
        Gather parameters and call.
        
        :param text: Text to be sent to Google Cloud TTS API to be
                     converted to speech
        :param lang: Language to be spoken
        :param voice: Voice of the speaker
        :param fileformat: File format (see link below)
        
        Name maps and file format specifications can be found here:
        https://cloud.google.com/text-to-speech/docs/voices
        """
        
        namemap = {
            "nl-NL" : [
                "nl-NL-Standard-A"
                ],
            "en-AU" : [
                "en-AU-Standard-A",
                "en-AU-Standard-B",
                "en-AU-Standard-C",
                "en-AU-Standard-D"
                ],
            "en-GB" : [
                "en-GB-Standard-A",
                "en-GB-Standard-B",
                "en-GB-Standard-C",
                "en-GB-Standard-D"
                ],
            "en-US" : [
                "en-US-Standard-B",
                "en-US-Standard-C",
                "en-US-Standard-D",
                "en-US-Standard-E",
                "en-US-Wavenet-A",
                "en-US-Wavenet-B",
                "en-US-Wavenet-C",
                "en-US-Wavenet-D",
                "en-US-Wavenet-E",
                "en-US-Wavenet-F",
                ],
            "fr-FR" : [
                "fr-FR-Standard-C",
                "fr-FR-Standard-D",
                ],
            "fr-CA" : [
                "fr-CA-Standard-A",
                "fr-CA-Standard-B",
                "fr-CA-Standard-C",
                "fr-CA-Standard-D"
                ],
            "de-DE" : [
                "de-DE-Standard-A",
                "de-DE-Standard-B"
                ],
            "ja-JP" : [
                "ja-JP-Standard-A"
                ],
            "pt-BR" : [
                "pt-BR-Standard-A"
                ],
            "es-ES" : [
                "es-ES-Standard-A"
                ],
            "sv-SE" : [
                "sv-SE-Standard-A"
                ],
            "tr-TR" : [
                "tr-TR-Standard-A"
                ],
            "cmn-TW" : [
                "cmn-TW-Wavenet-A-Alpha",
                "cmn-TW-Wavenet-B-Alpha",
                "cmn-TW-Wavenet-C-Alpha"
                ]
            }
        if not text:
            raise LanguageException(
                "Text to convert is not defined!"
                )
        if not voice and not lang:
            # Default to English voice if nothing is defined
            voice = 'en-US-Standard-B'
            lang = 'en-US'
        if voice and not lang:
            raise LanguageException(
                "Voice defined witout defining language!"
                )
        if lang not in namemap:
            raise LanguageException(
                "Requested language {} not available!".format(
                    lang
                    )
                )
        if lang and not voice:
            # Default to first voice in array
            voice = namemap[lang][0]
        if voice not in namemap[lang]:
            raise LanguageException(
                "Requested language {} does not have voice {}!".format(
                    lang,
                    voice
                    )
                )
        if not fileformat:
            fileformat = 'LINEAR16'
        if not samplerate:
            samplerate = 16000
        # Set the service name sent to Bing TTS
            
        headers = {
            "Content-type" : "application/json; charset=utf-8",
            }
        body = """{{
            'input' : {{
                'text' : "{}"
            }},
            'voice' : {{
                'languageCode' : '{}',
                'name' : '{}'
            }},
            'audioConfig' : {{
                'audioEncoding' : '{}',
                'sampleRateHertz' : {}
            }}
        }}
        """.format(
            text,
            lang,
            voice,
            fileformat,
            samplerate
        )       
        return self.call(headers, self.base_path, body)
