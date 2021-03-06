
#!/usr/bin/env python3

# Program uses Wireshark and Pyshark
# Install Wireshark - sudo apt-get install wireshark
# Install Pyshark - pip install pyshark

import pyshark
import sys

# Global variables
_g_packets_array = []                               # Array to hold all packets
_g_arguments_dict = {}

####################  FUNCTIONS  ##################################

def module_name():
    return "net-analyzer"

def module_help():
    return """This module captures live network packets into an rcap file.
            Arguments:
            # -i: Capture interface [ex: eth0]
            # -f: RCAP filename
            # -t: How long the capture will run in seconds (timeout or number of packets which comes first)
            # -p: How many packets to capture (timeout or number of packets which comes first)
            # -a: Whether to save the capture in a local array [ex: yes]
            # -v: Whether to print the captured packets [ex: yes]"""

def module_usage():
    return "{0} -i <interface: eth0> -f <file: net-analyzer.cap> -t <timeout: 100> -p <packet_limit: 100> -a <local_array: yes> -v <verbose: yes>".format(module_name())


def readArguments():
    for i, arg in enumerate(sys.argv[1:]):
        if(arg == "-i"):
            _g_arguments_dict['-i'] = sys.argv[i+2]
        if(arg == "-f"):
            _g_arguments_dict['-f'] = sys.argv[i+2]
        if(arg == "-t"):
            _g_arguments_dict['-t'] = sys.argv[i+2]
        if(arg == "-p"):
            _g_arguments_dict['-p'] = sys.argv[i+2]
        if(arg == "-a"):
            _g_arguments_dict['-a'] = sys.argv[i+2]
        if(arg == "-v"):
            _g_arguments_dict['-v'] = sys.argv[i+2]

#-----------------------------------------------------------------
# Callback function each time a packet is captured
def callbackOnCapture(*args):
    if _g_arguments_dict['-a'] == 'yes':
        _g_packets_array.append(args[0])
    if _g_arguments_dict['-v'] == 'yes':
        print(args[0])

#-----------------------------------------------------------------
# Capturing realtime packets
def capturePackets(arg_dict):
    _cap = pyshark.LiveCapture(interface=arg_dict['-i'], output_file=arg_dict['-f'])
    try:
        _cap.apply_on_packets(callbackOnCapture, packet_count=int(arg_dict['-p']), timeout=int(arg_dict['-t']))
    except Exception as e:
        print(e)
        #return len(_g_packets_array)

#------------------------------------------------------------------
# Main program
def main():
    readArguments()
    capturePackets(_g_arguments_dict)
    print('\nTotal number of captured packets: ' + str(len(_g_packets_array)) + '\n')



###################  PROGRAM STARTS  ################################
if __name__ == "__main__":
    main()
