#!/bin/bash

py.test #-s --pyargs expressyeaself --cov-report term-missing --cov=expressyeaself --cov-config .coveragerc
#rm expressyeaself/tests/__pycache__/*

