# Vagr (Python Version)
## What is Vagr?
It is a pretty badly coded implementation Virtual Machine management software for VirtualBox made in **Python**. I made this because my old computer at home ran Vagrant really slowly and it got to the point where it would sometimes freeze my computer. 
- Written in Python 3.7.2
- Compiled with PyInstaller
- Based on [Vagrant](https://www.vagrantup.com/)

NOTE: *The version [here](https://github.com/aaronlam1004/vagr) is an older, worse version.*  

## Requirements
- [VirtualBox](https://www.virtualbox.org/)
- Vagr Compatible OVAs
    -  Can create custom based on [the Vagr OVAs guidelines](https://github.com/aaronlam1004/vagr-definitive/blob/master/ovas/vagr_ovas_notes.txt)
    -  Can be downloaded from [the Vagr OVAs downloads](https://mega.nz/#F!fslWECaS!ff9DvPb9DRk7nIcA85ZNLQ)
## Getting Started with Vagr (but why would you?)
1. **Check out repository** using Github or    
```git clone https://github.com/aaronlam1004/vagr-py.git```  
2. **Define enviornment variable** for **```vagr-py```**.
3. **Download Vagr OVA** at [Vagr OVAs downloads](https://mega.nz/#F!fslWECaS!ff9DvPb9DRk7nIcA85ZNLQ) or **make your own using** [the Vagr OVAs guidelines](https://github.com/aaronlam1004/vagr-definitive/blob/master/ovas/vagr_ovas_notes.txt).
4. **Add OVA** to **```vagr-py/ovas```**.
5. **Create a new Vagr machine** using **```init```**  
**```vagr init ubuntu-bionic vagr```**
    - You can check what OVAS you have by using **```vagr ovas```**.
## The Vagr.json file (I can't believe you got this far)
After initialization, you will have a **```Vagr.json```** in the directory you ran the **```init```** command.  
That file may look something like this  
```json
{
    "machine": "vagr",
    "ports": [
        ["ssh", "tcp", "", "2222", "", "22"]
    ],
    "shared": [
        ["vagr", "YOUR DIRECTORY", "/home/vagr_home"]
    ]
}
```
## Using Vagr (but seriously why would you?)
In a directory that has a **```Vagr.json```** file.
- **```vagr ovas```** shows all OVA files you have in your **```vagr-py/ovas```** directory.
- **```vagr up```** starts up Vagr machine.
- **```vagr down```** shuts down Vagr machine.
- **```vagr reload```** restarts your Vagr machine.
- **```vagr rename```** renames the Vagr machine to whatever **```vmname```** you give it.
- **```vagr destroys```** deletes the Vagr machine.
- **```vagr status```** gives you the status of your Vagr machine (if it's running, the forwarded NAT ports, the shared folders).

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
1. Finish basis of this README.md
2. More network functionality (so far only works for NAT) by editing Vagr.json
    - Specifically, add features to allow users to use Bridged Adapter, etc.
3. Ability to change name using Vagr.json
