#!/bin/bash

# Define output file
OUTPUT_FILE="./master_markdown.txt"

# Remove output file if it exists
if [ -f "$OUTPUT_FILE" ]; then
  rm "$OUTPUT_FILE"
fi

# Find all .md files and process them
find . -name "*.md" -type f | sort | while read -r file; do
  # Add file path separator and file path to output with exactly 6 slashes
  echo "////// $file" >> "$OUTPUT_FILE"
  # Add file content to output
  cat "$file" >> "$OUTPUT_FILE"
  # Add a newline after each file for better separation
  echo "" >> "$OUTPUT_FILE"
done

echo "Master markdown file created at $OUTPUT_FILE"
