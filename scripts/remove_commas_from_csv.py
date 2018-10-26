#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:11:35 2018

@author: benoit
"""
import csv
import sys

def get_line_without_commas_in_title_column(line):
    split_line = line.split(',')
    first_column = split_line[0]
    second_column = split_line[1]
    third_column = ''.join(split_line[2:]).replace(',', '').strip('\n')
    return [first_column, second_column, third_column]
    
    

def create_csv_file_from_csv_without_commas(path_original_file, path_destination_file):
    with open(path_original_file, 'r', encoding = "ISO-8859-1") as original_file, \
        open(path_destination_file, 'w') as destination_file:
        lines = original_file.readlines()
        writer = csv.writer(destination_file, delimiter=',')
        writer.writerow(['id', 'date', 'title'])
        for line in lines[1:]:
            final_line = get_line_without_commas_in_title_column(line)
            writer.writerow(final_line)

if __name__ == '__main__':
    path_origin_file = sys.argv[1]
    path_target_file = sys.argv[2]
    create_csv_file_from_csv_without_commas(path_origin_file, path_target_file)