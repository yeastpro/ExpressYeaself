#!/bin/bash

# This script automates the download of raw data as published by Carl de Boer.
echo 'Request to download raw data received.'
echo ''
echo ''
sleep 1.5s

# Download pTpA data
echo 'Downloading 1st data set: pTpA data'
echo '...'
echo 'Please wait...'
echo ''
echo ''
curl -O https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE104878&format=file&file=GSE104878%5F20160609%5Faverage%5Fpromoter%5FELs%5Fper%5Fseq%5FpTpA%5FALL%2Eshuffled%2Etxt%2Egz > ./example/pTpA_data/raw_data_pTpA.txt.gz 
wait
echo ''
echo ''
echo 'Successfully downloaded.'
echo ''
echo ''
sleep 1.5s

# Download Abf1TATA data
echo 'Downloading 2nd data set: Abf1TATA data'
echo '...'
echo 'Please wait...'
curl -O https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE104878&format=file&file=GSE104878%5F20160609%5Faverage%5Fpromoter%5FELs%5Fper%5Fseq%5FAbf1TATA%5FALL%2Eshuffled%2Etxt%2Egz > ./example/Abf1TATA_data/raw_data_Abf1TATA.txt.gz 
wait
echo 'Successfully downloaded.'
echo ''
echo ''
sleep 1.5s

# Print acknowledgments
echo 'Data courtesy of Carl de Boar et. al'
echo 'Published along with with publication "Deciphering cis-regulatory logic with 100 million synthetic promoters".'
echo 'Data can be found at https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878'
echo ''
echo ''
sleep 1.5s

echo 'Process complete.'

