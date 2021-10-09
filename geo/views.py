from django.shortcuts import render
import requests
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import views # for django's api view
import re # support for regular expressions -> used to verify ip address is valid
from django.core.cache.backends import locmem # Used to check contents of cache
from rest_framework import status # HTTP status responses
from rest_framework.views import APIView
import json


# Returns individual ip information
class IpDetails(APIView):
    def get(self, request, ip):
        # validate ip address
        if not is_valid_ip(ip):
            return Response({'ip address': 'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        # check cache for ip address
        info = cache.get(ip)
        data = {}

        # if ip information is not found in cache request information from GeoJS
        if not info and is_valid_ip(ip):
            req = requests.get('https://get.geojs.io/v1/ip/geo/' + ip + '.json', params=request.GET)
            data = req.json()
            # Handling case where city/country are not present
            validate_ip_data(data)
            save_to_cache(ip, data['city'], data['country'])
            data = [{'city': data['city'], 'country': data['country']}]
        # information was in cache and is being added to JSON
        elif info:
            info['ip'] = ip
            data = info
        return Response({"data": data}, status=status.HTTP_202_ACCEPTED)


# Filter IPs from cache by city or country
class AllIpFilter(APIView):
    def get(self, request, filter):
        filter = filter.lower()
        all_info = cache.get('all')
        if all_info:
            all_info = [ x for x in all_info if x['country'].lower() == filter or x['city'].lower() == filter]
        return Response({"data": all_info}, status=status.HTTP_202_ACCEPTED)


# Sorts and returns IPs by Country unless 'city' is specified in the sort_flag
class AllIpSort(APIView):
    def get(self, request, sort_flag):
        all_info = cache.get('all')
        if sort_flag.lower() == 'city' and all_info:
            # found a city at 86.88.88.88 that started with a tild, probably could have just left out the if statement
            all_info = sorted( all_info, key = lambda i: i['city'] if i['city'][0].isalpha() else i['city'][1:] )
        elif all_info:
            all_info = sorted( all_info, key = lambda i: i['country'])

        return Response({"data": all_info}, status=status.HTTP_202_ACCEPTED)


# Default list
class ListIPs(APIView):
    def get(self, request):
        data = cache.get('all')
        if not data:
            return Response({"data" : "No IPs in memory"}, status=status.HTTP_202_ACCEPTED)
        return Response({"data": data}, status=status.HTTP_202_ACCEPTED)


# Helper functions below

def validate_ip_data(data):
    # validate data
    if 'city' not in data:
        data['city'] = 'NA'
    if 'country' not in data:
        data['country'] = 'NA'

# Validate an ip address
def is_valid_ip(ip):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if re.search(regex, ip):
        return True
    return False

def save_to_cache(ip, city, country):
    if not cache.get(ip):
        new_ip_info = {'country': country, 'city': city}
        cache.set(ip, new_ip_info)
        new_ip_info.update({'ip': ip})
        all_info = cache.get('all')
        # if the cache isn't empty, pull all ips and update the json
        if all_info:
            all_info.append(new_ip_info)
            cache.set('all', all_info)
        else:
            all_info = list()
        all_info.append(new_ip_info)
        cache.set('all', all_info)


'''
Cache:
-Storing values in cache as a {ip: {city,country}} as well as {'all': {ip(1), city(1), country(1)},... {ip(n), city(n), country(n)} }.
 This was done becuase it is the easiest way to track/pull IPs from the cache. This will come with issues when the cache memory
 is full. This specific cache uses the LRU algorithm. Assuming the 'all' key/value entry is used more than the indiviual ip searches,
 the individual IP entries will start to dissappear from the cache even though they will be contained in the 'all' entry. If the entry
 that was removed is searched again, it will result in a duplicate entry in the 'all' values.

-Another option would have been to give each entry an index so that the entries look as: {index: {ip, city, country}
 But if wanted to pull all records one would use a while loop until cache.get() returned a value of None. This would be
 slow.

Sorting:
-One could sort the values in the JSON before storing them in the cache which would speed up the retrieval time when requesting all data
 in a sorted order.
'''
