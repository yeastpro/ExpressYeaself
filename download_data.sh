#!/bin/bash

# This script automates the download of raw data as published by Carl de Boer.
echo 'Request to download raw data received.'
echo ''
echo ''
sleep 1.5s

# Report data the be downloaded and where it is being downloaded from
echo 'Data courtesy of Carl de Boar et al.'
echo 'Published alongside publication "Deciphering cis-regulatory logic with 100 million synthetic promoters"'
echo 'Data to be downloaded from https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878'
echo '    Data Set 1: pTpA'
echo '        Filename on website: GSE104878_20160609_average_promoter_ELs_per_seq_pTpA_ALL.shuffled.txt.gz'
echo '    Data Set 2: Abf1TATA'
echo '        Filename on website: GSE104878_20160609_average_promoter_ELs_per_seq_Abf1TATA_ALL.shuffled.txt.gz'
echo ''
echo ''
sleep 1.5s

# Download pTpA data
echo 'Downloading 1st data set: pTpA data'
echo ''
echo '    Please wait...'
curl ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE104nnn/GSE104878/suppl/GSE104878_20160609_average_promoter_ELs_per_seq_pTpA_ALL.shuffled.txt.gz -o ./example/pTpA_data/raw_data_pTpA.txt.gz -s
wait
echo '    Successfully downloaded.'
echo '    Location: ./example/pTpA_data/raw_data_pTpA.txt.gz'
echo ''
echo ''
sleep 1.5s

# Download Abf1TATA data
echo 'Downloading 2nd data set: Abf1TATA data'
echo ''
echo '    Please wait...'
curl ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE104nnn/GSE104878/suppl/GSE104878_20160609_average_promoter_ELs_per_seq_Abf1TATA_ALL.shuffled.txt.gz -o ./example/Abf1TATA_data/raw_data_Abf1TATA.txt.gz -s
wait
echo '    Successfully downloaded.'
echo '    Location: ./example/Abf1TATA_data/raw_data_Abf1TATA.txt.gz'
echo ''
echo ''
sleep 1.5s

# Print conclusion
echo 'Process complete.'

