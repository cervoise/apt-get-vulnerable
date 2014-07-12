#!/usr/bin/python

#Covered by GPL V2.0

import functions
import report
import cache

###Main###

def main():

    distrib = 'wheezy'
    
    if cache.init_cache_folders(distrib) is False:
        print "Error with cache function"
        return 1
    
    packet_list_to_update = functions.get_update_list("upgrade.txt")
    
    packet_list = functions.get_packet_dict("dpkg.txt")

    packet_update_info = []
    for packet in packet_list_to_update:
        #anayse_packet(packet_name, version, update_version)
        packet_update_info.append(functions.analyse_packet(distrib, packet[0], packet_list[packet[0]], packet[1]))

    source_packet_update_info = functions.get_update_packet_list_by_source_packet(distrib, packet_update_info)

    return report.export_to_html(source_packet_update_info)
    
main()
