import os
import shutil
import tempfile
from gtts import gTTS
from anki.storage import Collection

# Input path to the original .apkg file
input_path = "test-data/french.apkg"

# Output path for the updated .apkg file
output_path = "test-data/output.apkg"

# Path to the folder where audio files will be saved
audio_path = "audio"


# Create a temporary directory to extract the contents of the original .apkg file
with tempfile.TemporaryDirectory() as temp_dir:

    # Extract the contents of the original .apkg file to the temporary directory
    shutil.unpack_archive(input_path, temp_dir, "zip")

    # Load the collection.anki2 file from the extracted directory
    collection_path = os.path.join(temp_dir, "collection.anki2")
    collection = Collection(collection_path)

    # Modify the notes in the collection
    for note_id in collection.find_notes(""):
        note = collection.get_note(note_id)

        # Get the French text from the note
        french_text = note.fields[1]

        # Generate the audio file
        tts = gTTS(french_text, lang="fr")
        audio_file = f"{note_id}.mp3"
        audio_file_path = os.path.join(audio_path, audio_file)
        tts.save(audio_file_path)

        # Add the audio file to the note
        note.fields[3] = f"[sound:{audio_file}]"

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
