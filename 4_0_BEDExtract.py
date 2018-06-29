#script to extract the region between gene pairs
#with disparate gene expression 
#author: Noah A. Legall
#created: June 29th 2018
##########

import sys # use to access arguments
import os # use in order to call commands from terminal script is called in
import re # regular expressions used to find specific elements in file

#read in file name you want to parse
filename = sys.argv[1] 

#name of the output file we wish to create, then activly create it
output = sys.argv[2] 
os.system('touch '+output) 

file = open(filename, "r")
out = open(output, "w")

#the variable file doesn't seem to be iterable, so we create a list
new_file = []
for line in file.readlines():
    new_file.append(line)
    
#The patterns that we wish to extract
label = re.compile('(unitig_\d*)')
right_coordinate = re.compile('unitig_\d*\t\d*\t(\d*)')
left_coordinate = re.compile('unitig_\d*\t(\d*)')


#parse the BED file to extract the information that we need
#write out to the output file 
for i in range(0,len(new_file)-2,2): 
    left_line = new_file[i]
    right_line = new_file[i+1]
    
    bed_name = label.search(left_line).group(1)
    bed_right_coordinate = right_coordinate.search(left_line).group(1)
    bed_left_coordinate = left_coordinate.search(right_line).group(1)
    
    #a minute point, but in order to have regions that are generally consistent
    #we would need to move the right coordinate up 1 and the left coordinate down 1
    out.write(tag+'\t'+str(int(bed_right_coordinate )+1)+'\t'+str((int( bed_left_coordinate)-1))+'\n')
    
    #now we have regions where we can start analysis.
    #I believe searching for motifs would be the next step, but I will 
    #consult with dr. wallace later on.