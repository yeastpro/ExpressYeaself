[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/yeastpro/ExpressYeaself.svg?branch=master)](https://travis-ci.com/yeastpro/ExpressYeaself)
[![Coverage Status](https://coveralls.io/repos/github/yeastpro/ExpressYeaself/badge.svg?branch=master)](https://coveralls.io/github/yeastpro/ExpressYeaself?branch=master)

# ExpressYeaself 
  
Authors: **Joe Abbott**, **Keertana Krishnan**, **Guoyao Chen**.  

----
### Overview

_ExpressYeaself_  is an open source scientific software package that aims to quickly and accurately predict the contribution a promoter sequence has on the expression of genes in **_Saccharomyces cerevisiae_** (or '_Brewer's yeast_ '). 

This will allow the costly and time-consuming trial-and-error processes in the development and synthesis of biotherapeutics to be streamlined. Our goal is to use machine learning and data mining to make **recommendations** on which promoter sequences are likely to contribute to high levels of gene expression, and which **are not**.  

For further details on the scientific background of our project and back-end operation of our package, please see our [use cases](https://github.com/yeastpro/ExpressYeaself/blob/master/doc/use_cases.md).

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

1. Clone the _ExpressYeaself_ repository:

	``git clone https://github.com/yeastpro/ExpressYeaself.git`` 

2. Navigate into the repository: ``cd ExpressYeaself``
3. Install our virtual environment: ``conda env create -n environment.yml``
4. Enter the virtual environment: ``conda activate yeast``
5. Download the raw data: ``chmod +x download_data.sh && ./download_data.sh``


#### Getting started
Now you have installed our package and downloaded the raw data, you are ready to start using our features! You can use our interactive notebooks to take you through the process: 

* Navigate into the directory containing our interactive guides:  
	``cd expressyeaself/interaction/``
* To start processing the data, use _jupyter_ to open our first interactive notebook:  
	`` jupyter notebook 1_how_to_process_raw_data.ipynb &``
* Follow the instructions in the notebook, choose your parameters, and process the data. 
* When you're done, save and exit the notebook.
* You can then start to encode your data and train your model:
	`` jupyter notebook 2_how_to_train_model.ipynb &``

----
### Directory Structure

	ExpressYeaself (master)  
    |---doc  
        |---technology_reviews
        	  |--1_sequencing_software_packages.md
        	  |--2_neural_network_packages.md
        |--timeline.md
        |--use_cases.md
    |---example  
        |---Abf1TATA_data
            |--Abf1TATA_scaffold.txt
        |---native_data
            |--native_data.txt
        |---pTpA_data
            |--pTpA_scaffold.txt
        |---processed_data
            |--10000_from_20190610100252461788_homogeneous_deflanked_sequences_inserted_into_Abf1TATA_scaffold_with_exp_levels.txt.gz
            |--10000_from_20190611170757656183_homogeneous_deflanked_sequences_with_exp_levels.txt.gz
            |--10000_from_20190612130111781831_percentiles_els_binarized_homogeneous_deflanked_sequences_with_exp_levels.txt.gz
        |--__init__.py
        |--series_matrix_GSE104878-GPL17143.txt
    |---expressyeaself  
        |---interaction
            |--1_how_to_process_raw_data.ipynb
            |--context.py
        |---models
        	  |---1d_cnn
        	      |--1D_CNN_builder.ipynb
        	      |--context.py
        	  |---1d_loccon
        	      |--1d_locally_connected.ipynb
        	      |--context.py
        	      |--loc_con_1d.py
        	  |---lstm
        	      |--context.py
        	      |--lstm_model_function.py
        |---tests
            |--__init__.py
            |--context.py
            |--test_build_promoter.py
            |--test_encode_sequences.py
            |--test_organize_data.py
            |--test_process_data.py
            |--test_utilities.py
        |--__init__.py
        |--build_promoter.py
        |--construct_neural_net.py
        |--encode_sequences.py
        |--organize_data.py
        |--process_data.py
        |--utilities.py
        |--version.py  
    |--.coveragerc
    |--.gitignore  
    |--.travis.yml
    |--LICENSE  
    |--README.md 
    |--download_data.sh
    |--environment.yml
    |--requirements.txt
    |--runtests.sh 

----
### Contributions

Any contributions to the project are warmly welcomed! If you discover any bugs, please report them in the [issues section](https://github.com/emissible/SPEEDCOM/issues) of this repository and we'll work to sort them out as soon as possible. If you have data that you think will be good to train our model on, please contact one of the authors.

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
