# Python-Google-TTS
Google Cloud Text to Speech library for Python

# Installation
To install using pip, run the following command:

    pip install git+https://github.com/jpattWPC/Python-Google-TTS.git

# API Key
To generate an API key follow the [Setting up API keys](https://support.google.com/cloud/answer/6158862) help document. **NOTE: ENSURE YOU HAVE [PROPERLY RESTRICTED ACCESS](https://support.google.com/cloud/answer/6310037?hl=en) VIA THE API KEY!**

# Usage
The following is the usage of the library

    translator.speak(text, language, voice, fileformat, samplerate)

Variable | Description | Note
--- | --- | ---
text | The text that you wish to convert to speech | 
language | The language/country you wish to hear the speech in | Case sensitive. See [Supported Voices API Reference](https://cloud.google.com/text-to-speech/docs/voices) for list
voice | The name of the voice to use | Case sensitive
fileformat | File format to encode the speech to | Optional, defaults to LINEAR16 See [Method: text.synthesize API Reference](https://cloud.google.com/text-to-speech/docs/reference/rest/v1beta1/text/synthesize#AudioEncoding) for list of formats
samplerate | Samplerate in hertz) for the speech synthesis| Optional, defaults to 16000. Must be integer. Samplerate examples are 8000, 16000, 22050, 44000, 48000

# Example
    from googletts import Translator
    translator = Translator('YOUR-API-KEY-HERE')
    output = translator.speak("This is a text to speech translation", "en-US", "en-US-Standard-B", "LINEAR16", 8000)
    with open("file.wav", "wb") as f:
        f.write(output)
