# Technology Review #1
---
# Sequencing Software

## Problem

Data we have access to:      

* ~ 31 million random oligonucleotide sequences, each of 80 bp in length, with an associated experimental expression level. 
* 15,000 scaffold sequences, consisting of distal and proximal regions that flank an 80 bp variable region.

_For descriptions and contextualization of our data, please see our [use cases](https://github.com/yeastpro/ExpressYeaself/blob/master/doc/use_cases.md)._

In order to generate a complete nucleotide sequence for a promoter, we need to insert each of the random sequences into each of the appropriate scaffold sequences. This will result in a very large (potentially 465 billion) number of unique promoter sequences, that need to be outputted to a separate file with their associated expression levels. The sequences will then need to be encoded or embedded, ready to be passed into a neural network.  

Because storing such a large volume of data will be an issue, we need a fast and memory efficient method to generate the unique promoter sequences on the fly. This may be combined with functions to encode the sequences on the fly also, but this component isn't considered in this technology review.

## Solutions

### A. _Bowtie2_

#### Description

_Bowtie2_ is a 


#### Suitability


### B. _Scaffolder_

#### Description  

Implemented in Ruby, _Scaffolder_ 

## hello 
--
this is better than vim 

<center> heel </center>
