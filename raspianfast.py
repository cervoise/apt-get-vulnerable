import debian

#clean specific update info of Raspian (rpi)
def clean(packet_list_to_update):
    new_packet_list = []
    for elmt in packet_list_to_update:
        new_pacet_list.append(elmt[0], clean_packet_version(elmt[1]))
                              
    return new_packet_list

def clean_packet_version(packet_version):
    if re.match(".*\+rpi.*", packet_version):
        partition_rpi = packet_version.partition('+rpi')
        packet_version = partition_rpi[0]
        if partition_rpi[2].partition('+')[2] != "":
            packet_version += "+" + partition_rpi[2].partition('+')[2]

    return packet_version

#Fast analysis so ignore rpi specific update and uses Debians
def get_packet_page(distrib, packet):
    return debian.get_packet_page(distrib, packet)

def get_source_packet_page(distrib, packet):
    return debian.get_source_packet_page(distrib, packet)

#get source packet
def get_source_packet(distrib, packet):    
    return debian.get_source_packet(distrib, packet)

def get_changelog_url(packet_page):
    return debian.get_changelog_url(packet_page)

def get_regex(actual_version):
    return clean_packet_version(actual_version).replace('.', '\.').replace('+', '\+')
                              
def get_system_string():
    return "raspianfast"
