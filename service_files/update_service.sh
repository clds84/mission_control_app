#!/bin/bash

files=("battery_status.service" "start_chromium.service")
source_dir="$HOME/.config/systemd/user"
target_dir="$HOME/mission_control/service_files"

mkdir -p "$target_dir"

for f in "${files[@]}"; do
  # If the file in source_dir differs from target_dir or target file doesn't exist
  if ! cmp -s "$source_dir/$f" "$target_dir/$f"; then
    cp "$source_dir/$f" "$target_dir/"
    echo "Copied $f from $source_dir to $target_dir"
  else
    echo "No changes in $f, skipping."
  fi
done