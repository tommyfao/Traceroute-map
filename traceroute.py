#!/bin/python3

#This is a custom made traceroute program
#usage: ./traceroute <ip_to_trace_route_to> [max_path=32]

import sys
import os
import socket
import geoip2.database
import cartopy.crs as ccrs
import matplotlib.pyplot as plt




####################################################################################
######FIRST get ip address list.
####################################################################################

max_path=32

if len(sys.argv) >= 2:
	destination = str(sys.argv[1])
	if len(sys.argv) == 3:
		max_path = int(sys.argv[2])
else:
	print("Please provide an argument. Please")
	sys.exit()

last='last';
iplist=[]
##
#Use ping with varying ttl's and read the ip address of the responding router
##
for ttl in range(1,max_path):
    out=os.popen("ping -W 2 -c 1 -t "+str(ttl)+ " " + destination + " | grep \"Time to live\" | awk -F \"[()]\" \'{print $2}\'").read()
    #out=os.popen("ping -c 1 -t "+str(ttl)+ " " + destination).read()
    if out == last:
        break
    last=out
    iplist.append(out)
    #host=socket.gethostbyaddr(out)
    print(out)

####################################################################################
#######NEXT get geo coordinates of each ip address.
#######if the ip address is not in the database(typically private ip), ignore
####################################################################################

coords =[];
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

for ip in iplist:
        try:
            ipcity=reader.city(ip.rstrip())
            coords.append([ipcity.location.longitude,ipcity.location.latitude])
        except:
            continue
print(coords)

####################################################################################
#########FINALLY plot those coordinates on a map
####################################################################################
img_extent = (-180,180,-90,90)
img=plt.imread('map.jpg')

ax = plt.axes(projection=ccrs.PlateCarree())
#ax.imshow(img, origin='upper',extent=img_extent,transform=ccrs.PlateCarree())
ax.stock_img()
ax.coastlines(resolution='50m',color='black',linewidth=1)

for i in range(0,len(coords)-1):
    plt.plot([coords[i][0],coords[i+1][0]],[coords[i][1],coords[i+1][1]],color='blue',linewidth=2,marker='o',transform=ccrs.Geodetic())

data_extent=(min(item[0] for item in coords) - 20, max(item[0] for item in coords) + 10, min(item[1] for item in coords) -10 , max(item[1] for item in coords) + 10)
ax.set_extent(data_extent)
plt.show()

