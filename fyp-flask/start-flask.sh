#!/usr/bin/env bash
echo "Moving data to shared volume"
if [ ! -f "/opt/data/default/movie"]; then
    mv movie/ /opt/data/default/
fi
echo "Moving data to shared volume (done)"
echo "Starting Flask"

flask run --host=0.0.0.0