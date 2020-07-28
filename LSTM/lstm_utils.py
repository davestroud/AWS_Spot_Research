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
    the number of passengers in the 12+1st month.

"""
def create_inout_sequences(input_data, tw):
    inout_seq = []
    L = len(input_data)
    for i in range(L-tw):
        train_seq = input_data[i:i+tw]
        train_label = input_data[i+tw:i+tw+1]
        inout_seq.append((train_seq ,train_label))
    return inout_seq

"""
    Create LSTM Model

"""
class LSTM(nn.Module):
    def __init__(self, input_size=1, hidden_layer_size=100, output_size=1):
        super().__init__()
        self.hidden_layer_size = hidden_layer_size

        self.lstm = nn.LSTM(input_size, hidden_layer_size)

        self.linear = nn.Linear(hidden_layer_size, output_size)

        self.hidden_cell = (torch.zeros(1,1,self.hidden_layer_size),
                            torch.zeros(1,1,self.hidden_layer_size))

    def forward(self, input_seq):
        lstm_out, self.hidden_cell = self.lstm(input_seq.view(len(input_seq) ,1, -1), self.hidden_cell)
        predictions = self.linear(lstm_out.view(len(input_seq), -1))
        return predictions[-1]

