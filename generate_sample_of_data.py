#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:57:41 2018

@author: benoit
"""

import pandas as pd
import sys

def create_sample(origin, destination, rows):
    data = pd.read_csv(origin)
    sample = data.sample(n=rows, replace=False)
    sample.to_csv(destination)

if __name__ == '__main__':
    original_file_path = sys.argv[1]
    sample_path = sys.argv[2]
    num_rows = int(sys.argv[3])
    create_sample(original_file_path, sample_path, num_rows)