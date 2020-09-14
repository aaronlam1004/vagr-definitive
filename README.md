# Vagr (Python Version)
## What is Vagr?
It is a pretty badly coded implementation of how the software Vagrant works using **Python**. I made this because my old computer at home ran Vagrant really slowly and it got to the point where it would sometimes freeze my computer. 

NOTE: *The version [here](https://github.com/aaronlam1004/vagr) is an older, worse version.*
## Requirements
- Windows Operating System
- VirtualBox
- Vagr Compatible OVAs
    -  Can create custom based on [the Vagr OVAs guidelines](https://github.com/aaronlam1004/vagr-definitive/blob/master/ovas/vagr_ovas_notes.txt)
    -  Can be downloaded from [the Vagr OVAs downloads](https://mega.nz/#F!fslWECaS!ff9DvPb9DRk7nIcA85ZNLQ)
## Using Vagr (but why would you?)
## Commands
```
Usage: vagr [command]
Commands:
    ovas
    init [vagr machine ova] [vmname]
    up
    down
    reload
    rename [vmname]
    destroy
    status
```
## TODO
1. More network functionality (so far only works for NAT)
    - Specifically, add features to allow users to use Bridged Adapter, etc.
