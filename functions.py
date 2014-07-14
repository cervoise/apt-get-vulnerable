#Covered by GPL V2.0

import urllib
import fileinput
import re

import cache

#get a list with [packet_name, uptodate_version] from "apt-get --simulate update"
def get_update_list(filename):
    update_list = []

    for line in fileinput.input(filename):
        if line[0:4] == 'Conf':
            packet_name = line.partition('Conf ')[2].partition(' ')[0]
            packet_version = line.partition('(')[2].partition(' ')[0]
            update_list.append([packet_name, packet_version])
    return update_list

#get a packet list with [packet_name, version] from "dpkg -l"
def get_packet_dict(filename):
    packet_dict = {}

    for line in fileinput.input(filename):
        if line[0:2] == 'ii':
            list_temp = line.split(' ')
            while '' in list_temp:
                list_temp.remove('')
            #you have to split :, because some packet have proc info in name
            #like "libc6:i386"
            packet_dict[list_temp[1].split(':')[0]] = list_temp[2]

    return packet_dict


#get changelog file for a packet and a version
def get_changelog_file(system, distrib, packet, version):
    source_packet = system.get_source_packet(distrib, packet)
    
    return cache.get_cache_file(system, distrib, source_packet, version)

def analyse_packet(system, distrib, packet, actual_version, new_version):
    changelog_file = get_changelog_file(system, distrib, packet, new_version).split('\n')
    
    packet_changelog = ""
    #escape specifics chars
    actual_version_regex = system.get_regex(actual_version)
    
    pattern_to_stop = ".*\(" + actual_version_regex + "\).*"
    pattern_for_security = ".*security.*"
    is_security_update = False

    for line in changelog_file:
        if re.match(pattern_for_security, line):
                is_security_update = True
        if re.match(pattern_to_stop, line):
            break
        else:
            packet_changelog += line + '<br/>\n'

    return [packet, actual_version, new_version, is_security_update, packet_changelog]

#extract cve from changelog (return a string)
def extract_cve(changelog):
    cve_string = ""
    cve_pattern = "CVE-[12][09][1-9]{2}-[0-9]{4}"
    cve_list = set(sorted(re.findall(cve_pattern, changelog)))
    for cve in cve_list:
        cve_string += cve + ", "

    return cve_string[:-2]

#return a dic with source packet as key from a list with [packet_name, actual_version, new_version, is_security_update, packet_changelog]    
def get_update_packet_list_by_source_packet(system, distrib, update_list):
    source_packet_update_info = {}
    for packet in update_list:
        #we only keep security update
        if packet[3]:
            source_packet = system.get_source_packet(distrib, packet[0])
            if source_packet in source_packet_update_info.keys():
                source_packet_update_info[source_packet][0].append(packet[0])
            else:
                source_packet_update_info[source_packet] = [[packet[0]], packet[1], packet[2], packet[4], extract_cve(packet[4])] 
    #format: [source_packet] = [packet_list, actual_version, new_version, packet_changelog, cve]
    return source_packet_update_info
