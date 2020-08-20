[![pypiv](https://img.shields.io/pypi/v/gitutor.svg)](https://pypi.python.org/pypi/gitutor)
[![pyv](https://img.shields.io/pypi/pyversions/gitutor.svg)](https://pypi.python.org/pypi/gitutor)

# Gitutor

Welcome to Gitutor. This tool is meant to get you up and running using gitmin the shortest time possible while learning on the go.

Gitutor is a command line application that wraps git and provides beginner friendly versions of git's commands. It's Git the easy way.

You can check out the tutorial and a further explanation of the commands in the [docs](https://gitutor.io/guide). And don't worry if you forget how to use a command you can always run

    $ gt <command> --help

If you have any problems please send us an email at support@gitutor.io or open an issue in our [repo](https://github.com/artemisa-mx/gitutor/issues), we usually answer in less than a day.

## Available commands

1. gt init - Initialize your local and remote repository.
2. gt save - Save you changes in the local and remote repository.
3. gt goback - Return to a previous commit.
4. gt compare - Compare the current state with a previous commit.
5. gt ignore - Make git ignore selected files.
6. gt lesson - See gitutor lessons and documentation.

## Installation guide

> **NOTE**: pipx and gitutor work with Python3.6+

In order to use gitutor without any dependencies version conflicts we recommend installing it using pipx. Pipx creates a virtual environment for your package and exposes its entry point so you can run gitutor from anywhere. 

To install pipx and configure the $PATH run the following commands

For Windows: 

    $ python -m pip install pipx
    $ python -m pipx ensurepath

For MacOS use:

    $ brew install pipx

For Linux use:

    $ python3 -m pip install pipx
    $ python3 -m pipx ensurepath

> **NOTE**: You may need to restart your terminal for the path updates to take effect.

Once pipx is installed, run the following to install gitutor:

    $ pipx install gitutor

And to upgrade gitutor to its latest version you only need to run:

    $ pipx upgrade gitutor

To install gitutor without using pipx just run:

    $ pip install gitutor

## Additional notes

Before using gitutor you need to have Git available in your computer. You can check the installation guide [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

It's also recommended to store your GitHub credentials so you won't have to authenticate everytime you realize a push or pull. You can do this by running

    $ git config --global credential.helper store

This will store your credentials in a plain-text file (.git-gredentials) under your project directory. If you don't like this you can use any of the following approaches:

On Mac OS X you can use its native keystore with

    $ git config --global credential.helper oskeychain

For Windows you can install a helper called [Git Credential Manager for Windows](https://github.com/Microsoft/Git-Credential-Manager-for-Windows) and then run

    $ git config --global credential.helper manager


If you like what we're doing you can buy as a [coffee](https://ko-fi.com/artemisamx)
