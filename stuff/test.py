from pydub import AudioSegment
import math
import os


def split_mp3(source_file, minute_split=1):
    # Load the audio file
    audio = AudioSegment.from_mp3(source_file)

    # Calculate the length of each split (in milliseconds)
    split_length = minute_split * 60 * 1000

    # Calculate the number of full splits
    total_splits = math.ceil(len(audio) / split_length)

    # Create a directory to store the split files
    split_dir = os.path.splitext(source_file)[0] + "_splits"
    os.makedirs(split_dir, exist_ok=True)

    # Split the audio and export
    for i in range(total_splits):
        start_time = i * split_length
        end_time = min((i + 1) * split_length, len(audio))
        split_audio = audio[start_time:end_time]
        split_filename = f"{split_dir}/{os.path.splitext(os.path.basename(source_file))[0]}_part{i + 1}.mp3"
        split_audio.export(split_filename, format="mp3")
        print(f"Exported {split_filename}")


if __name__ == "__main__":
    # Example usage
    path_to_file = "ORIGIN.wav"
    duration_in_minutes = 5  # Change the duration per file as needed
    split_mp3(path_to_file, duration_in_minutes)