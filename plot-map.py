import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import re
import sys

dir_name = "Activities"
wanted_activity = 'running'

j = 1
while j < len(sys.argv):
    o = sys.argv[j]
    if o not in ['-a','-d']:
        print('ERROR:', o, 'is not an option')
        sys.exit()
    else:
        if not j+1 < len(sys.argv):
            print('ERROR: value for option',o,'not given') 
            sys.exit()
        else:
            if o == '-a':
                wanted_activity = sys.argv[j+1]
            elif o == '-d':
                dir_name = sys.argv[j+1]
            else:
                assert o not in ['-a','-d']
    j += 2

files = os.listdir(dir_name)

print('Looking for',wanted_activity,'activites in',dir_name,'directory')

tot_num = len(files)
for i,file in enumerate(files):
    if file.endswith(".gpx"):        
        activity_type = re.split(r'<type>(\w+)',open(os.path.join(dir_name, file), 'r').read())[1]
        if activity_type == wanted_activity or wanted_activity == 'all':
            gpx_file = open(os.path.join(dir_name, file), 'r')
            gpx = gpxpy.parse(gpx_file)

            data = gpx.tracks[0].segments[0].points

            # start Position
            start = data[0]
            # end Position
            finish = data[-1]

            df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])

            for point in data:
                df = df.append({'lon': point.longitude, 'lat' : point.latitude, 'alt' : point.elevation, 'time' : point.time}, ignore_index=True)
            

            plt.plot(df['lon'], df['lat'],'k')
            print( i+1," file of ",tot_num,activity_type)
            del df
        else:
            print( i+1," is a ", activity_type, 'activity')

plt.show()

