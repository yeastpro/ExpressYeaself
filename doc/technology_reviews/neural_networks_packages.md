# Technology Review #2
-----------------------------------------------------------------------------------
## Technology Review of Python open source neural network and deep learning libraries

_The features of the following packages are presented in bullet point format._

#### Keras:
 - High level API capable of running on top of TensorFlow, Microsoft Cognitive Toolkit, Theano, or PlaidML
 - User-friendly, modular, extensible
 - Interface rather than standalone machine-learning framework
 - More intuitive and high level, so easier to develop deep learning models regardless of computational backend
 - Commonly used neural-network building blocks such as layers, objectives, activation functions, optimizers
 - Tools to work with image and text-based data
 - Mainly supports standard neural networks, CNNs, RNNs, Bayesian, RBM/DBNs
 - Supported by major cloud platforms

#### Tensorflow:
 - Used for dataflow and differentiable programming across a range of tasks including machine learning applications such as neural 
networks
 - Responsive construct (possible to view all parts of the graphs (not possible in sklearn))
 - Flexible (has modularity and can make parts standalone)
 - Allows distributed computing
 - Parallel neural network training
 - Feature columns (bridging input data with the model)
 - Statistical distributions
 - Model visualization (using tensorboard)
 - Supports standard neural networks, CNNs, RNNs, Bayesian, RBM/DBNs

#### Theano:
 - Optimizing compiler for manipulating and evaluating mathematical expressions, especially matrix-valued ones
 - Tight integration with NumPy
 - Compatible with GPU
 - Efficient symbolic differentiation (can take in one or many inputs)
 - Speed and stability (optimization of small to large values)
 - Dynamic code generation (faster)
 - Extensive unit-testing and self-verification
 - Key foundational library for deep learning, completely python based
 - Mainly supports standard neural networks, CNNs, RNNs, RBM/DBNs
 - Approachable enough to be used in the classroom for deep/machine learning applications
 
#### Apache MXNet:
 - Used to train, and deploy deep neural networks
 - Scalable, allows for fast model training
 - Supports a flexible programming model and multiple programming languages
 - Lean, flexible, and ultra-scalable deep learning framework that supports state of the art in deep learning models
 - Efficient deployment of a trained model to low-end devices for inference, such as mobile devices
 - Supported by AWS and Azure
 - Multi-GPU training
 - Supports CNNs, RNNs, RBM/DBNs

#### Caffe:
 - Deep learning framework
 - Supports many different types of architectures geared towards image classification and image segmentation
 - Supports CNN, RNN, LSTM and fully connected neural network designs
 - Expressive architecture encourages application and innovation
 - Extensible code fosters active development
 - Speed – can process over 60M images per day
 - Powerful academic community

#### PyTorch:
 - Open-source machine learning library for python (based on torch)
 - Tensor computation (like NumPy) with strong GPU acceleration
 - Deep neural networks built on a tape-based autodiff system
 - Supports various types of tensors
 - Hybrid frontend – seamless transitioning to graph mode – speed, optimization, functionality
 - Supported by major cloud platforms
 - Supports CNNs, RNNs
 
_Based on these features, our group will most likely use Keras. Keras and Tensorflow support the most types of neural networks,
however, Keras is more user-friendly, has higher functionality, is faster and allows for greater manipulation of image and
text-based data. We will use Keras on a Tensorflow backend, as opposed to Theano, because it has additional features
including model visualization, feature columns and allows for parallel network training. Ultimately, it is also more flexible and faster._

