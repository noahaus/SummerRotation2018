#script to append "lcl|" to GFF unitig column
#author: Noah A. Legall
#created: June 18th 2018
##########

#Take in arguements and save to variable filename
import sys # use to access arguments
import os # use in order to call commands from terminal script is called in
import re # regular expressions used to 

#read in file name i want to change
filename = sys.argv[1] 

#name of the output file we wish to create, then activly create it
output = sys.argv[2] 
os.system('touch '+output) 


file = open(filename, "r")
out = open(output, "w")

#read the input file line by line and make changes where appropriate
#save these changes in the output file line by line
for line in file:
    # this is the pattern we are trying to match to see if we need to add 'lcl|' to the beginning of the string
    if re.match('unitig', line) is not None:
        #if the match occurs, then append the string and write the line into the output file
        new_line = line.replace('unitig','lcl|unitig')
        out.write(new_line)
    else:
        #otherwise just take the line and write it to the new file. this ensures that the information between files is consistent.
        out.write(line)

# it should now be easier for cufflinks to compare read information with gff now

