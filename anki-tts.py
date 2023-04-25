import os
import shutil
import tempfile
import argparse
from gtts import gTTS
from anki.storage import Collection


def generate_audio_apkg(input_path, output_path, audio_path, text_index, speech_index):
    '''
    Fn to perform TextToSPeech on a given file of an ANKI package and add it to another field
    '''

    # Create a temporary directory to extract the contents of the original .apkg file
    with tempfile.TemporaryDirectory() as temp_dir:

        # Extract the contents of the original .apkg file to the temporary directory
        shutil.unpack_archive(input_path, temp_dir, "zip")

        # Load the collection.anki2 file from the extracted directory
        collection_path = os.path.join(temp_dir, "collection.anki2")
        collection = Collection(collection_path)

        # Modify the notes in the collection
        for note_id in collection.find_notes(""):
            print(note_id)
            note = collection.get_note(note_id)

            # Get the French text from the note
            french_text = note.fields[text_index]

            # Generate the audio file
            tts = gTTS(french_text, lang="fr")
            audio_file = "anki-tts-{}.mp3".format(note_id)
            audio_file_path = os.path.join(audio_path, audio_file)
            tts.save(audio_file_path)

            # Add the audio file to the note
            note.fields[speech_index] = "[sound:{}]".format(audio_file)

            # Update the note in the collection
            collection.update_note(note)

        # Save the changes to the collection
        collection.close()

        # Create a new .apkg file in a separate directory
        with tempfile.TemporaryDirectory() as output_dir:

            # Compress the modified contents into a new .apkg file
            shutil.make_archive(
                os.path.join(output_dir, "updated"),
                "zip",
                temp_dir
            )

            # Copy the new .apkg file to the output directory
            shutil.copy(
                os.path.join(output_dir, "updated.zip"),
                output_path
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate audio files and create updated .apkg file')
    parser.add_argument('input_path', type=str, help='Path to the original .apkg file')
    parser.add_argument('output_path', type=str, help='Path to the output .apkg file')
    parser.add_argument('audio_path', type=str, help='Path to the folder where audio files will be saved')
    parser.add_argument('text_index', type=int, help='index of the text field in a given note. Make sure text has no HTML formatting')
    parser.add_argument('speech_index', type=int, help='index of the speech feld in a given note')
    args = parser.parse_args()
    
    generate_audio_apkg(args.input_path, args.output_path, args.audio_path, args.text_index, args.speech_index)
