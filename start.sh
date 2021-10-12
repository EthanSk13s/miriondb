#!/bin/sh

CMD=$1; shift
case "$CMD" in
    mirion) 
        exec python run.py
        ;;
    theater)
        cd theater
        exec ./theater
        ;;
    *) echo "Did not supply an argument"
        ;;
esac