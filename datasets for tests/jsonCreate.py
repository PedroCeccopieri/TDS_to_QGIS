import json
import os
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

datasets = [
{"name": 'local',
"url": str(ROOT_DIR) + '\\datasets\\netcdf_file_example.nc',
"style": str(ROOT_DIR) + '\\styles\\sea_level_anomaly.qml'}
,
{"name": 'local2',
"url": str(ROOT_DIR) + '\\datasets\\netcdf_file_example2.nc',
"style": str(ROOT_DIR) + '\\styles\\sea_level_anomaly.qml'}
]

# Serializing json
json_object = json.dumps(datasets)
 
# Writing to sample.json
with open("datasets.json", "w") as outfile:
    outfile.write(json_object)