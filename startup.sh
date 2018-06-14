#!/bin/bash
sudo apt-get install nmap && sudo apt-get install nikto
cp spider.py ~
python ~/spider.py -l logs.txt > /etc/rc.local



