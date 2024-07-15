#!/bin/bash

# Function to concatenate files with a separator
concat_files() {
    local dir=$1
    local depth=$2
    local output_file=$3

    find "$dir" -maxdepth "$depth" -type f | while read -r file; do
        echo "=== $(basename "$file") ===" >> "$output_file"
        cat "$file" >> "$output_file"
        echo -e "\n" >> "$output_file"
    done
}

# Usage
# First argument: Directory to search for files
# Second argument: Depth level
# Third argument: Output file
concat_files "$1" "$2" "$3"

