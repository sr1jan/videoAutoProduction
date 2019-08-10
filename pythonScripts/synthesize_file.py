import argparse


# [START tts_synthesize_text_file]
def synthesize_text_file(text_file):
    """Synthesizes speech from the input file of text."""
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    with open(text_file, 'r') as f:
        text = f.read()
        input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-AU',
        name='en-AU-Wavenet-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=0.80)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    filename = text_file
    try:
        filename = filename.replace('.txt', '.mp3')
        filename = filename.replace('../Articles/', '')
        filename = filename.replace(';', ' ')
        filename = filename.replace("'", " ")
    except Exception as e:
        print(e)
        print('Check replace command in synthesize_file.py file')

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file: \n{filename}\n')
# [END tts_synthesize_text_file]


# [START tts_synthesize_ssml_file]
def synthesize_ssml_file(ssml_file):
    """Synthesizes speech from the input file of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    from google.cloud import texttospeech
    client = texttospeech.TextToSpeechClient()

    with open(ssml_file, 'r') as f:
        ssml = f.read()
        input_text = texttospeech.types.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-AU',
        name='en-AU-Wavenet-D',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3,
        speaking_rate=0.80)

    response = client.synthesize_speech(input_text, voice, audio_config)

    # The response's audio_content is binary.
    filename = ssml_file
    try:
        filename = filename.replace('.txt', '.mp3')
        filename = filename.replace('../Articles/', '')
        filename = filename.replace(';', ' ')
        filename = filename.replace("'", " ")
    except Exception as e:
        print(e)
        print('Check replace command in synthesize_file.py file')

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file: \n{filename}\n')
# [END tts_synthesize_ssml_file]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text',
                       help='The text file from which to synthesize speech.')
    group.add_argument('--ssml',
                       help='The ssml file from which to synthesize speech.')

    args = parser.parse_args()

    if args.text:
        synthesize_text_file(args.text)
    else:
        synthesize_ssml_file(args.ssml)
