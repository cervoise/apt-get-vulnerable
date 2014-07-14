import urllib

def clean(packet_list_to_update):
    #No need to clean packet list to update
    return packet_list_to_update

#get packet page
def get_packet_page(distrib, packet):
    #try to implement a db with source package to avoid requesting twice the same page
    packet_page_url = "https://packages.debian.org/en/" + distrib + "/"
    packet_page_url += packet
    #print packet_page_url
    return urllib.urlopen(packet_page_url).read()

def get_source_packet_page(distrib, packet):
    packet_page_url = "https://packages.debian.org/en/source/" + distrib + "/"
    packet_page_url += packet
    #print packet_page_url
    return urllib.urlopen(packet_page_url).read() 

#get source packet
def get_source_packet(distrib, packet):
    packet_page = get_packet_page(distrib, packet)
    if packet_page.partition('<div id="psource">')[1] == '<div id="psource">':
        source_packet = packet_page.partition('<div id="psource">')[2].partition('</div>')[0]
        source_packet = source_packet.partition('>')[2].partition('</a>')[0]
    else:
        source_packet = packet
        
    return source_packet

def get_changelog_url(packet_page):
    changelog_url = packet_page.partition("_changelog")[0].rpartition('http://')[2]
    return "http://" + changelog_url + "_changelog"

def get_regex(actual_version):
    return actual_version.replace('.', '\.').replace('+', '\+')

def get_system_string():
    return "debian"
