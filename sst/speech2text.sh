#!/usr/bin/env bash

source sst/config.sh

opusdec sst/uploads/blob sst/fuck.wav
sox sst/fuck.wav  -b 16 -c 1 -e signed -r 16000 -L -t raw sst/output.raw 

rm sst/fuck.wav
python sst/transcribe.py sst/output.raw
