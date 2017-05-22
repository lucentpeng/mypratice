#!/bin/sh


for package in "$@"; do
    dpkg -s "$package" 2>&1 && {
        echo "$package is installed."
    } || {
        printf "\nThe following packages need to be installed:\n$package\n\n"
        sudo apt-get install $package
    }
done
