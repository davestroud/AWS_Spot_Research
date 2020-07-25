## for pytorch
import torch
import torch.nn as nn

# for graphics
import seaborn as sns
import matplotlib.pyplot as plt

# for data
import numpy as np
import pandas as pd

# for data normalization
from sklearn.preprocessing import MinMaxScaler

"""
    The create_inout_sequences function will accept
    raw input data and return a list of tuples.
    In each tuple, the first element will contain
    a list of 12 items corresponding to the number 
    of passengers traveling in 12 months. The second
    tuple element will contain one item; ie, 
    the number of passengers inthe 12+1st month.

"""
def create_inout_sequences(input_data, tw):
    inout_seq = []
    for i in range(L-tw):
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        input_seq.append((train_seq, train_label))
    return inout_seq
    