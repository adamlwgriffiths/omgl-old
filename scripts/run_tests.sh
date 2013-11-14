#!/bin/bash

# top level is omgl, tests are in omgl/tests
python -m unittest discover -t omgl -s omgl/tests
