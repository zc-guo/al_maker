#!/bin/bash

# Default settings
generate_sequences=false
output_folder="output"

# Parse arguments
while getopts "go:" opt; do
  case $opt in
    g)
      generate_sequences=true
      ;;
    o)
      output_folder=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

# Generate sequence text files if the -g option is provided
if $generate_sequences; then
  echo "Generating sequence text files..."
  python gen_seq.py
fi

# Run the make_al.py script with the specified output folder
echo "Running make_al.py with output folder: $output_folder..."
python make_al.py $output_folder

echo "Processing complete."