#Covered by GPL V2.0

import os
import urllib

import functions

#TODO
#review folders write after creation
def init_cache_folders(distrib):
    if os.path.isdir("cache") is False:
        os.mkdir("cache")

    if os.path.isdir("cache/" + distrib) is False:
        os.mkdir("cache/" + distrib)

    return os.path.isdir("cache/" + distrib)

def is_cache_file_exist(distrib, source_packet, version):
    return os.path.isfile("cache/" + distrib + "/" + source_packet + "_" + version + ".txt")

def write_cache_file(distrib, source_packet, version):
    packet_page = functions.get_source_packet_page(distrib, source_packet)
    #print packet_page
    changelog_url = packet_page.partition("_changelog")[0].rpartition('http://')[2]
    changelog_url = "http://" + changelog_url + "_changelog"
    
    changelog_file = open("cache/" + distrib + "/" + source_packet + "_" + version + ".txt",'w')
    changelog_file.write(urllib.urlopen(changelog_url).read())
    return changelog_file.close()

def get_cache_file(distrib, source_packet, version):
    if is_cache_file_exist(distrib, source_packet, version) is False:
        write_cache_file(distrib, source_packet, version)
        
    with open("cache/" + distrib + "/" + source_packet + "_" + version + ".txt", 'r') as content_file:
        changelog = content_file.read()
    return changelog
