#!/bin/sh

nohup python run.py &
cd theater

echo "Waiting for website to be up until asset server can be started..."
sleep 15

exec ./theater