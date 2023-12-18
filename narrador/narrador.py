import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

from pathlib import Path
from openai import OpenAI
client = OpenAI()

def narrate(fileName: str, 
        voice: str = "onyx", 
        doc = str):
    speech_file_path = os.path.join(os.getcwd(), fileName)

    response = client.audio.speech.create(
      model="tts-1-hd",
      voice="onyx",
      input= doc
    )

    response.stream_to_file(speech_file_path)


def read_markdown_file(file_path):
    """
    Reads the contents of a Markdown file and returns it as a string.
    
    :param file_path: The path to the Markdown file.
    :return: A string containing the contents of the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return str(e)


def split_text_forWhisper(text, max_length=4096):
    """
    Splits a text into chunks, each with a maximum length of max_length,
    trying to break at full stops or other natural breakpoints.
    """
    chunks = []
    while text:
        # Find the nearest breakpoint
        split_index = min(len(text), max_length)
        breakpoint = text.rfind('.', 0, split_index) + 1
        if breakpoint == 0:
            breakpoint = text.rfind(' ', 0, split_index)
        if breakpoint == 0:
            breakpoint = split_index
        chunks.append(text[:breakpoint].strip())
        text = text[breakpoint:].strip()
    return chunks

from pydub import AudioSegment

def combine_all_mp3s_in_directory(directory, output_file):
    """
    Search for all mp3 files in the specified directory, combine them into one mp3 file,
    and insert a 5-second silence between each file.

    :param directory: Path to the directory to search for mp3 files.
    :param output_file: Path for the output combined mp3 file.
    """
    # Search for mp3 files in the directory
    mp3_files = [f for f in os.listdir(directory) if f.endswith('.mp3')]

    combined_sound = None
    silence = AudioSegment.silent(duration=5000)  # 5 seconds of silence

    # Loop through the found mp3 files and combine them
    for file in mp3_files:
        file_path = os.path.join(directory, file)
        sound = AudioSegment.from_mp3(file_path)

        if combined_sound is None:
            combined_sound = sound
        else:
            combined_sound += silence + sound

    # Check if any mp3 files were found and combined
    if combined_sound:
        # Export the combined sound file
        combined_sound.export(output_file, format="mp3")
        print(f"Combined MP3 with silence created at {output_file}")
    else:
        print("No MP3 files found in the directory.")