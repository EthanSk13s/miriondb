#!/bin/sh

CMD=$1; shift
case "$CMD" in
    mirion) 
        exec python run.py
        ;;
    theater)
        sleep 10
        cd theater || exit
        exec ./theater
        ;;
    deploy)
        exec gunicorn --workers=1 -b 0.0.0.0:5500 "run:create_app('config.Config')"
        ;;
    *) echo "Did not supply an argument"
        ;;
esac