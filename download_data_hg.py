"""
Download and format dataset from Hugging Face for evaluation.
"""
import os
import argparse
import datasets as hugDS
import soundfile as sf

def main():
    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="Download and process dataset from Hugging Face.")
    parser.add_argument("--sampling_rate", type=int, default=24000, help="Sampling rate for audio files.")
    parser.add_argument("--dataset_name", type=str, default="doof-ferb/infore1_25hours", help="Name of the dataset on Hugging Face.")
    parser.add_argument("--split", type=str, default="train", help="split of the dataset to download.")
    parser.add_argument("--audio-column", type=str, default="audio", help="Name of the audio column in the dataset.")
    parser.add_argument("--text-column", type=str, default="transcription", help="Name of the text column in the dataset.")
    args = parser.parse_args()

    # Extract metadata file name from dataset name
    dataset_name = args.dataset_name
    sampling_rate = args.sampling_rate
    split = args.split
    audio_column = args.audio_column
    text_column = args.text_column
    base_dir = os.path.join("data", dataset_name.split('/')[-1])
    output_dir = os.path.join(base_dir, "wavs")
    metadata_file = os.path.join(base_dir, "metadata.lst")

    # Load dataset
    dataset = hugDS.load_dataset(
        path=dataset_name, 
        split=split, 
        trust_remote_code=True, 
        streaming=True
    ).cast_column(audio_column, hugDS.Audio(sampling_rate=sampling_rate))

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Process dataset and save audio files
    with open(metadata_file, "w", encoding="utf-8") as metadata_file_handle:
        index = 0  # Initialize the index counter
        dataset_iter = iter(dataset)
        try:
            while True:
                # Find a valid example1
                while True:
                    example1 = next(dataset_iter)
                    audio_data1 = example1[audio_column]["array"]
                    transcription1 = example1[text_column]
                    duration1 = len(audio_data1) / sampling_rate

                    if 3 <= duration1 <= 40:
                        break

                # Save example1 audio file
                filename1 = f"{index:06d}.wav"
                filepath1 = os.path.join(output_dir, filename1)
                sf.write(filepath1, audio_data1, sampling_rate)

                # Find a valid example2
                while True:
                    example2 = next(dataset_iter)
                    audio_data2 = example2[audio_column]["array"]
                    transcription2 = example2[text_column]
                    duration2 = len(audio_data2) / sampling_rate

                    if 3 <= duration2 <= 40:
                        break

                # Save example2 audio file
                filename2 = f"{index + 1:06d}.wav"
                filepath2 = os.path.join(output_dir, filename2)
                sf.write(filepath2, audio_data2, sampling_rate)

                # Write metadata for both examples
                metadata_file_handle.write(f"{filename1}|{transcription1}|{filename2}|{transcription2}\n")
                index += 2  # Increment the index by 2

                if index % 1000 == 0:
                    print(f"Processed {index} files...")

        except StopIteration:
            print("Processing complete!")

if __name__ == "__main__":
    main()