#!/bin/bash
clear

#Prompts
echo "Type the name of the file you would like to create a fasta database of"
read wallace_output
echo "Type the PREFIX name of the output file you desire"
read final_output

#This is the simple way of excluding the header. 
#get the line count then subtract that value by 1.
#Use that new value in the parameters of the tail command
LINES=`cat $wallace_output | wc -l`
NO_HEADER=$(($LINES-1))
tail -n $NO_HEADER $wallace_output > no_header.bed

#The file I am working with has many columns, but we only need a small subset of them
#After extracting what is needed, combine the files for later processing
cut -f 1,3,4 no_header.bed > upstream_output.out
cut -f 1,7,8 no_header.bed > downstream_output.out
cat downstream_output.out >> upstream_output.out
cat upstream_output.out > temp_u_gibba_draft.bed

#We need to add lcl| to the label whether it be Scf or ctg
python 6_1_ChangeScfOrCTGTolcl.py temp_u_gibba_draft.bed u_gibba_draft.bed

#Now we that we have the appropriate bed file format needed to make a custom 
#BLAST database, time to actually make the fasta file.
#sort the bed file, then just create the fasta file
bedtools sort -i u_gibba_draft.bed > "$final_output.bed"
bedtools getfasta -fi Utricularia_gibba.4.1.fa -bed "$final_output.bed" -fo "$final_output.fa"

#Create the custom database that BLAST queries can be searched against
makeblastdb -in "$final_output.fa" -input_type fasta -dbtype nucl -title "$final_output.database" -parse_seqids -out "$final_output.database"

#example of how to call blastn
#blastn -query ../4_sequences/scripts/query.fa -db /home/noahaus/noahaus_data/6_fact_checking/"$final_output.database"