# Traceroute-map
Simple python program that manually performs a traceroute and then maps it.

Requires geoip2, cartopy, and matplotlib

Cartopy installation guide: https://scitools.org.uk/cartopy/docs/latest/installing.html#installing

IP geolocation database from MaxMind, used under Creative Commons Attribution 4.0 License.

Usage:

./traceroute.py <destination address or hostname> [max path length to try=32]
