#!/bin/sh
filesize=5 #In megabytes
tcpdump -C $filesize -w capture 
