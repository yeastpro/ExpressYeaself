[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/yeastpro/ExpressYeaself.svg?branch=master)](https://travis-ci.com/yeastpro/ExpressYeaself)
[![Coverage Status](https://coveralls.io/repos/github/yeastpro/ExpressYeaself/badge.svg?branch=master)](https://coveralls.io/github/yeastpro/ExpressYeaself?branch=master)

# ExpressYeaself 
  
  
  
Authors: **Joe Abbott**, **Keertana Krishnan**, **Guoyao Chen**.  

----
### Overview

_ExpressYeaself_ is an open source scientific software package that aims to quickly and accurately predict the contribution a promoter sequence has on on the expression of genes in **_Saccharomyces cerevisiae_** (or '_Brewer's yeast_ '). Doing so will streamline the  process in the synthesis of biotherapeautics - such as insulin -  

For further details on the background science and operation of our package, please see our [use cases](https://github.com/yeastpro/ExpressYeaself/blob/master/doc/use_cases.md).

----
### Current Features

1. [Raw data](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE104878)<sup>1</sup> consisting of ~ 62 million sequences and their associated expression levels, can be **processed** in an automated and highly **streamlined** manner, according to a large number of **tunable parameters**.

2. Processed data can be manipulated for input into our **neural networks** by either **_one-hot encoding_** or **_embedding_**.

3. **Three different models** can then be trained on this encoded data:
	* 1-dimensional convolutional neural network (**1DCNN**)
	* 1-dimensional locally connected network (**1DLOCCON**)
	* Long-Short-Term Memory (**LSTM**), a type of recurrent neural network.

3. These trained models can then be used to **make predictions** on the extent to which a promoter sequence will contribute to a gene's expression level.


----
### Future Work
* We are currently in the process of developing some data mining tools to identify and extract so called **_magic motifs_** from our raw data. 
* These are shorter nucleotide sequences that are present within complete promoter sequences that contribute to the **highest** expression levels.
* Identifying and extracting these will allow us to make **recommendations** on what motifs a promoter sequence should contain in order to result in a high expression level of the gene being promoted.  

----
### Configuration

#### Pre-requirements
* Python 3.6.7 or later
* Conda version 4.6.8 or later
* GitHub

#### Installation
Execute the following ``commands`` in your computer's terminal application to install our package:  

1. a) Either clone the _ExpressYeaself_ repository:

	``git clone https://github.com/yeastpro/ExpressYeaself.git`` 

2. Navigate into the repository: ``cd ExpressYeaself``
3. Install our virtual environment: ``conda env create -n environment.yml``
4. Enter the virtual environment: ``conda activate yeast``
5. Download the raw data: ``chmod +x download_data.sh && ./download_data.sh``


#### Getting started
Now you have installed our package and downloaded the raw data, you are ready to start using our features! You can use our interactive notebooks to take you through the process. 

* Navigate into the directory containing our _How to_ guides:  
	``cd doc/how_to_guides``
* To start processing the data, use _jupyter_ to open our first interactive notebook:
	`` jupyter notebook 1_how_to_process_raw_data.ipynb &``
* Follow the instructions in the notebook, choose your parameters, and process the data. When you're done, save and exit the notebook.

----
### References
<sup>1</sup> Carl G. de Boer _et al._, _Deciphering cis-regulatory logic with 100 million synthetic promoters_, doi: [_http://dx.doi.org/10.1101/224907_](http://dx.doi.org/10.1101/224907), **2017**.

----
### License

_ExpressYeaself_ is licensed under the [MIT license](https://github.com/yeastpro/ExpressYeaself/blob/master/README.md). 

----
### Troubleshooting

* Module not found errors:
	* Make sure you're in our virtual environment! 
	* Re-enter it with: ``conda activate yeast``
* Permission denied errors when running shell scripts from terminal:
	* You need to grant yourself access to execute the scripts.
	* Do so with: ``chmod +x <filename>.sh``
