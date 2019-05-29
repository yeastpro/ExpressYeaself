# Use Cases

## Background

Transcription factors are proteins that regulate the rate of transcription of DNA into mRNA, the polynucleotides needed to express proteins. These factors ensure that the right genes are expressed in the right cells at the right time. This is controlled through the turning 'on' or 'off' of specific genes by binding to DNA upstream of the gene at a certain target sequence. Once bound, the factor can make it easier or more difficult for RNA polymerase to bind to the promoter of the gene and transcribe it into mRNA.

Protein expression refers to the way in which proteins are synthesized, modified and regulated. In the case of this project… [more biological background]

Determining the heterologous protein expression in eukaryotes, such as yeast, has been an ongoing challenge in research. However, with a greater understanding of transcription factors, it should be possible to manipulate and fine-tune levels of expression. Ultimately, this aids in improving the efficiency and reducing the cost and environmental burden of producing necessary biopharmaceuticals, such as insulin.

In the past few years, there has been a collective effort to systematically explore these transcription factors and their impacts using natural and synthetic biology. This has generated millions of data points which can now be integrated together to identify transcriptional motifs, sequences, and positions, using machine learning techniques. This allows the determination of the transcription factors that have the greatest impact on protein expression, which can then be used to develop an optimized predictive model.

## Objectives

Through predictive modeling, _ExpressYeaself_ aims to develop a greater understanding of protein expression in yeast based on the configurations of transcription factors.

## Components

(Flow Chart of package consisting of three different neural networks combined together, 
including information about the layers and parametrization.)

### Data cleaning
_ExpressYeaself_ will use combined publicly available data from www.yeastract.com, yetfasco.ccbr.utoronto.ca/ and www.yestss.org/ as training data. This combination will require some cleaning to ensure uniformity, as well as encoding of gene sequences. 

### Cross-Validation of existing models
Existing models developed by Carl G. de Boer _et al._ will be used as a baseline to compare the 
efficiency of the _ExpressYeaself_ model. We will also perform the:  
  
* Regularization the motif sequences  
* Pair transcription factor effects with protein expressions

### Predictive Models
This model will employ the use of a convolutional neural network (CNN), a long short term memory 
network (LSTM) and a 1D locally connected netowrk as three separate systems, which are then combined 
after their completing to determine an overall efficiency value. The data will be trained on both pTpA 
and Abf1TATA data used by Carl G. de Boer in his work on [cis-regulatory models]
(https://github.com/Carldeboer/CisRegModels). This will involve manipulation of hyperparameters to 
deliver the most effective model for both sequence types.

## Implications

Better understanding of genetic structural motifs that affect protein expression in yeast will eventually
allow the process of protein synthesis for the development of _human_ therapeutics (such as insulin) to
be greatly improved with respect to time, cost, environmental consciousness and efficiency.
 
