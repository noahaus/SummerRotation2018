#script to find adjacent gene pairs that could potentially
#share an insulator region of interest between them
#author: Noah A. Legall
#created: June 21th 2018
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

#here we create an empty list to put a more filtered version of the file into. 
#I found that I had a ton of white space at the end, so this just checks for that in the csv.
new_file = []

#Scan file and see where the whitespace begins.
for line in file.readlines():
    #If you find the whitespace. stop transcribing
    #Else, just print the new line to the list new_file
    if re.match(',,,,,,,,,,,,', line) is not None:
        break
    else:
        new_file.append(line)
        
#Now, let's find the values that are adjacent to each other. 
#Only extract the expression value and the chromosome label and coordinates
#should be useful in crafting a BED file soon
expression_value = re.compile(',-,-,(\d*.\d*),')
label = re.compile('(unitig_\d*:\d*-\d*)')

#only take lines that have the information we want. We want to look ahead one index every iteration
#so we need to make the looping happen in a way to incorporate every pair
for i in range(0,len(new_file)-2): 
    #if we find a value, start the algorithm
    if expression_value.search(new_file[i]) is not None:
        #extract the expression of adjacent genes
        extracted_expression_upstream = expression_value.search(new_file[i]).group(1)
        extracted_expression_downstream = expression_value.search(new_file[i+1]).group(1)
        #extract the labels of adjacent genes
        extracted_label_upstream = label.search(new_file[i]).group(1)
        extracted_label_downstream = label.search(new_file[i+1]).group(1)
        
        #further breakdown the label to extract information necessary for a BED file
        label_parts_upstream = extracted_label_upstream.split(':')
        chromosome_upstream = label_parts_upstream[0]
        coordinates_upstream = label_parts_upstream[1]
        upstream_first_coords = coordinates_upstream.split('-')[0]
        upstream_last_coords = coordinates_upstream.split('-')[1]
        
        label_parts_downstream = extracted_label_downstream.split(':')
        chromosome_downstream = label_parts_downstream[0]
        coordinates_downstream = label_parts_downstream[1]
        downstream_first_coords = coordinates_downstream.split('-')[0]
        downstream_last_coords = coordinates_downstream.split('-')[1]

        #furthermore, exclude results that contain no expression value
        if extracted_expression_upstream == '0,0' or extracted_expression_downstream == '0,0':
            continue
        #ultimately looking for adjacent genes where the expression is very disparate    
        elif float(extracted_expression_upstream)/float(extracted_expression_downstream) < 50 or float(extracted_expression_upstream)/float(extracted_expression_downstream) < 50:
            continue
        #if the adjacent genes make it through the tests, then write out to the desired output file
        else:
            out.write(chromosome_upstream+'\t'+upstream_first_coords+'\t'+upstream_last_coords+'\t'+extracted_expression_upstream+'\n')
            out.write(chromosome_downstream+'\t'+downstream_first_coords+'\t'+downstream_last_coords+'\t'+extracted_expression_downstream+'\n')

#Now that we have this tab delimited spreadsheet, we can now go through the process of
#creating a BED file that can later lead to extracting DNA values to search for possible motifs
