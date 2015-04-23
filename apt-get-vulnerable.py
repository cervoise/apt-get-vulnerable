#!/usr/bin/python

#Covered by GPL V2.0

import getopt
import sys

import functions
import report
import cache

import debian
import raspianfast

def get_system_link(system_string):
    if system_string == 'debian':
        return debian
    elif system_string == 'raspianfast':
        return raspianfast
    #elif system_string == 'raspian':
        #return raspina
    #elif system_string == 'ubuntu':
        #return ubuntu
    else:
        print system_string + " is not supported as a system."
        return sys.exit()

def usage():
    print "apt-get-vulnerable -s system -d distrib -i input-file1  -j input-file2 -o output"
    print "   input-file1 is the return of 'apt-get --simulate upgrade'"
    print "   input-file2 is the return of 'dpkg -l'"
    print ""
    print "system: debian (default), raspianfast"
    print "distrib: squeeze (default), wheezy, jessie"

###Main###

def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:d:i:j:o:h")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
        
    system = debian
    distrib = "squeeze"
    firstinput = ""
    secondinput = ""
    output = "Security-update-analysis"
    
    for o, a in opts:
        if o in ("-h"):
            usage()
            sys.exit()
        elif o in ("-s"):
            system = get_system_link(a)
        elif o in ("-d"):
            distrib = a
        elif o in ("-i"):
            firstinput = a
        elif o in ("-j"):
            secondinput = a
        elif o in ("-o"):
            output = a
        else:
            usage()
            sys.exit()

    if cache.init_cache_folders(system, distrib) is False:
        print "Error with cache function"
        return 1
        
    packet_list_to_update = functions.get_update_list(firstinput)
    packet_list_to_update = system.clean(packet_list_to_update)
    
    packet_list = functions.get_packet_dict(secondinput)

    packet_update_info = []
    for packet in packet_list_to_update:
    #for packet in packet_list:
        packet_update_info.append(functions.analyse_packet(system, distrib, packet[0], packet_list[packet[0]], packet[1]))

    source_packet_update_info = functions.get_update_packet_list_by_source_packet(system, distrib, packet_update_info)

    return report.export_to_html(source_packet_update_info, output)
    
if __name__ == "__main__":
    main()
