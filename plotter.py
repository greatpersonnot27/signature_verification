import matplotlib.pyplot as plt
import numpy as np

def plot_signature(x_values, y_values):
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(x_values, y_values)  # Plot some data on the axes.
    plt.show()

def plot_scatter_signature(x_values, y_values):
    fig, ax = plt.subplots()
    ax.scatter(x_values, y_values)
    plt.show()