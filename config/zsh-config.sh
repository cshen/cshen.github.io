#!/usr/bin/env zsh


if [ ! -d "${ZDOTDIR:-$HOME}/.zprezto" ]
then
    git clone --recursive https://github.com/sorin-ionescu/prezto.git "${ZDOTDIR:-$HOME}/.zprezto"
fi
#
# Create a new Zsh configuration by copying/linking the Zsh configuration files provided
#
setopt EXTENDED_GLOB
for rcfile in "${ZDOTDIR:-$HOME}"/.zprezto/runcoms/^README.md(.N); do
  ln -s "$rcfile" "${ZDOTDIR:-$HOME}/.${rcfile:t}"
done

echo "check https://github.com/sorin-ionescu/prezto"

