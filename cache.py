#Covered by GPL V2.0

import os
import urllib

import functions

import debian
import raspianfast

#TODO
#review folders write after creation
def init_cache_folders(system, distrib):
    if os.path.isdir("cache") is False:
        os.mkdir("cache")

    if os.path.isdir("cache/" + system.get_system_string()) is False:
        os.mkdir("cache/" + system.get_system_string())
    
    if os.path.isdir("cache/" + system.get_system_string() + "/" + distrib) is False:
        os.mkdir("cache/" + system.get_system_string() + "/" + distrib)

    return os.path.isdir("cache/" + system.get_system_string() + "/" + distrib)

def is_cache_file_exist(system, distrib, source_packet, version):
    return os.path.isfile("cache/" + system.get_system_string() + "/" + distrib + "/" + source_packet + "_" + version + ".txt")

def write_cache_file(system, distrib, source_packet, version):
    packet_page = system.get_source_packet_page(distrib, source_packet)
    #print packet_page
    changelog_url = system.get_changelog_url(packet_page)
    #print changelog_url
    changelog_file = open("cache/" + system.get_system_string() + "/" + distrib + "/" + source_packet + "_" + version + ".txt",'w')
    changelog_file.write(urllib.urlopen(changelog_url).read())
    return changelog_file.close()

def get_cache_file(system, distrib, source_packet, version):
    if is_cache_file_exist(system, distrib, source_packet, version) is False:
        write_cache_file(system, distrib, source_packet, version)
        
    with open("cache/" + system.get_system_string() + "/" + distrib + "/" + source_packet + "_" + version + ".txt", 'r') as content_file:
        changelog = content_file.read()
    return changelog
