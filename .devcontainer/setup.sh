#! /bin/bash

set -e

sudo apt update

# Install mise
curl https://mise.run | sh
echo 'eval "$(mise activate bash)"' >> $HOME/.bashrc

# Install dev tools
mise trust mise.toml
mise install -y

# Install project dependencies
mise use --global uv@0.6.7
uv sync