#!/bin/sh

cd /data/planet
exec python /data/planet/code/planet.py $* 2>/dev/null
	
