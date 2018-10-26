#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 10:19:37 2018

@author: benoit
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import TruncatedSVD
import time


def get_dataframe(size):
    """function that returns a pandas df from a csv file of the given size """
    df = pd.read_csv('/data/pfe/formated/samples/{}_rows.csv'.format(size))
    return df.sort_values(by='customer_id')[['movie_id', 'customer_id', 'rating']]
    
def create_interaction_matrix(pd_dataframe):
    """function that creates the interaction matrix from the pandas df given.
    It returns the matrix as n-dimensional array (numpy object)"""
    
    # 1. create a matrix full of zeros to the corresponding dimensions
    # users -> rows
    # movies -> columns
    num_users = pd_dataframe['customer_id'].nunique()
    num_movies = pd_dataframe['movie_id'].nunique()
    interaction_matrix = np.zeros((num_users, num_movies))
    
    # 2. create dictionaries with the old and new ids of customers
    # and with the old and new ids of the movies
    # (we need to change the indices to create the matrix)
    old_and_new_customer_ids = {}
    old_and_new_movie_ids = {}
    
    # 3. declare and initialize a variable to follow the number of the line
    # the index is not good because we sorted the values, so the index column
    # is not sorted anymore
    available_line = -1
    available_column = -1
    
    for _, row in pd_dataframe.iterrows():
        customer_id = row['customer_id']
        movie_id = row['movie_id']
        
        if (not (customer_id in old_and_new_customer_ids)) and \
        (not(movie_id in old_and_new_movie_ids)):
            # case where neither the customer_id, neither the movie_id are known
            available_line += 1
            available_column += 1
            old_and_new_customer_ids[customer_id] = available_line
            old_and_new_movie_ids[movie_id] = available_column
            
        elif (customer_id in old_and_new_customer_ids) and \
        (not(movie_id in old_and_new_movie_ids)):
            available_column += 1
            old_and_new_movie_ids[movie_id] = available_column

        elif (not (customer_id in old_and_new_customer_ids)) and\
        (movie_id in old_and_new_movie_ids):
            available_line += 1
            old_and_new_customer_ids[customer_id] = available_line
        
        #print("" + str(old_and_new_customer_ids[customer_id]) + "," + str(old_and_new_movie_ids[movie_id]))
        interaction_matrix[old_and_new_customer_ids[customer_id], \
                           old_and_new_movie_ids[movie_id]] = row['rating']   
    return interaction_matrix
    

def get_computation_time(interaction_matrix):
    start = time.time()
    svd = TruncatedSVD(n_components=2)
    svd.fit(interaction_matrix)
    end = time.time()
    return end - start



sizes = [10 ** i for i in range(1,8)]
computation_times = {}
for size in sizes:
    sample_df = get_dataframe(size)
    print("size:{}".format(size))
    interaction_matrix = create_interaction_matrix(sample_df)
    computation_times[size] = get_computation_time(interaction_matrix)
    
plt.figure()
plt.grid(True, color='gray', linestyle=':', linewidth=0.5)
plt.xscale('log')
plt.scatter(computation_times.keys(), computation_times.values())