#!/usr/bin/env bash

if [[ $(pwd) != */GIMP/3.0/plug-ins ]]; then
  echo "Script must be executed in a GIMP plug-ins directory."
  exit 1
fi

rm -rf gimp-minecraft-bridge && \
  git clone https://github.com/omgimanerd/gimp-minecraft-bridge && \
  rsync -a --delete gimp-minecraft-bridge/gimp-minecraft-bridge-lib/ \
    gimp-minecraft-bridge-lib/ && \
  rsync -a --delete gimp-minecraft-bridge/gimp-to-minecraft/ \
    gimp-to-minecraft/ && \
  rsync -a --delete gimp-minecraft-bridge/minecraft-to-gimp/ \
    minecraft-to-gimp/ && \
  rm -rf gimp-minecraft-bridge

if [[ $? -ne 0 ]]; then
  echo "Failed to install gimp-minecraft-bridge. Please file an issue."
  exit 1
fi
