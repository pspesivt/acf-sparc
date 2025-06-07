#!/bin/bash

# Define output file
OUTPUT_FILE="./roo-acf-sparc-workflow.txt"

# Remove output file if it exists
if [ -f "$OUTPUT_FILE" ]; then
  rm "$OUTPUT_FILE"
fi

# First, process rules/ directory files alphabetically
find ./rules -name "*.md" -type f | sort | while read -r file; do
  echo "---# File: $file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
done

# Second, process .roomodes files alphabetically
find . -name "*.roomodes" -type f | sort | while read -r file; do
  echo "---# File: $file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
done

# Finally, process all other .md files (excluding rules/) alphabetically
find . -name "*.md" -type f -not -path "./rules/*" | sort | while read -r file; do
  echo "---# File: $file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  cat "$file" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
done

echo "Master markdown file created at $OUTPUT_FILE"
