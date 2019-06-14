#!/bin/bash

py.test -k 'not construct_neural_net and not __init__ and not version' -s --pyargs expressyeaself --cov-report term-missing --cov=expressyeaself --cov-config .coveragerc 
rm -f expressyeaself/tests/__pycache__/*
rm -f ./trial_*
