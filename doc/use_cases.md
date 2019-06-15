# Use Cases

### _ExpressYeaself_

----
### Background

The development of biotherapeutic agents for treatment of human conditions is a lengthy, multi-step process. Part of the design process is manipulating the genomic sequences responsible for the expression of the protein biotherapeutic agent.

In order to reduce the cost of making the biotherapeutic, higher expressing gene sequences are highly sought after. There is therefore a lot of research being done to find a way to quantify and rationalize the mechanism by which expression of proteins is affected.

One well known effect is that of the _promoter sequence_; this regulates the transcription of genes upstream from it in a nucleotide, and hence affects the expression level. The trial-and-error process of finding the best promoter sequences is not only costly, but also very time consuming. 

By implementing deep learning methods through the use of neural network predictive modelling, _ExpressYeaself_ aims to predict the extent to which given promoter sequences may affect the expression level of the gene for which it is promoting. Having this tool can saves researchers a lot of time as they will quickly be able to discard sequences that have a very low probability of being effective before even entering the lab. They can then carry out the same trial and error process, but with a sample of promoter sequences that is potentially many orders of magnitude smaller than they typically would.

This will have positive effects on the whole process; making it more streamlined and reducing downstream costs for consumers.

We are able to build statistical models with such high accuracy due to the public availability of very large (~ 62 million sequence) data sets. These have been produced by the systematic exploration and evaluation of natural and synthetic gene sequences over many years worth of research.

----
### Objectives

Through predictive modeling, _ExpressYeaself_ aims to develop a greater understanding of protein expression in yeast based on the deep learning of relationships between motifs present in promoter sequences.

----
### Components

#### Data Processing

_ExpressYeaself_ will use data published by Carl de Boer as part of his publication "_Deciphering cis-regulatory logic with 100 million synthetic promoters_". We will develop a mechanism by which data can be processed in a large number of ways to allow different information to be conveyed by the data, and therefore different predictions to be made after training models. 

#### Predictive Models

This model will employ the use of a three neural networks:
  
* 1-dimensional convolutional neural network (**1DCNN**)  
* 1-dimensional locally connected network (**1DLOCCON**)  
* Long-Short-Term Memory (**LSTM**), a type of recurrent neural network.

These models can be trained on both pTpA and Abf1TATA data, processed as desired by our back-end processing systems. The best architectures for each model type will be found through **_hyper-paramterization_** searches; a type of trial-and-error that finds the best parameters by brute force changing of parameters, retraining, and re-validation.

----
### Implications

Better understanding of genetic structural motifs that affect protein expression in yeast will eventually allow the development of biotherapeutics (such as insulin) to be greatly improved with respect to time, cost, environmental consciousness and efficiency.
 
