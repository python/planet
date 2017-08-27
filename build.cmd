IF NOT EXIST _cache MKDIR _cache
DEL /Q _cache\*
IF NOT EXIST _output MKDIR _output

py -2 code\planet.py --verbose config\config.ini
