#!/bin/bash

# A script to generate Control Flow Graph (CFG) diagrams for C programs using GCC and Graphviz.

echo "--- Starting CFG Generation ---"

C_FOLDER="c_files"

# Array of C source files to process
C_FILES=("new_test.c" "scheduler_rr.c" "adventure.c" "2048.c")

# Create output directories if they don't exist
mkdir -p cfgs dots pngs

# Loop through each C file
for c_file in "${C_FILES[@]}"; do
  src_path="${C_FOLDER}/${c_file}"

  if [ -f "$src_path" ]; then
    base_name=$(basename "$c_file" .c)
    echo "Processing $src_path..."

    # Run GCC on the source file
    gcc -fdump-tree-cfg-graph-lineno "$src_path"

    # Find the generated .dot file (example: a-2048.c.016t.cfg.dot)
    dot_file=$(find . -maxdepth 1 -name "a-${c_file}.*.cfg.dot" -print -quit)

    if [ -f "$dot_file" ]; then
      # Define organized filenames
      cfg_file="cfgs/${base_name}.cfg"
      dot_output="dots/${base_name}.dot"
      png_output="pngs/${base_name}_cfg.png"

      # Move the .dot file
      mv "$dot_file" "$dot_output"

      # Move all related CFG dump files (.cfg, .c.*.cfg, etc.) to cfgs/
      find . -maxdepth 1 -type f -name "a-${c_file}.*.cfg" -exec mv {} "$cfg_file" \; 2>/dev/null

      # Convert .dot to .png using Graphviz
      dot -Tpng "$dot_output" -o "$png_output"
      echo "✅ Created $png_output"
    else
      echo "❌ Error: Could not find the .dot file for $c_file."
    fi
    echo "---------------------------------"
  else
    echo "⚠️ Warning: Source file $c_file not found. Skipping."
  fi
done

echo "--- CFG Generation Complete ---"