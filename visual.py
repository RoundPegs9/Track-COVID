### Plots the data collected from Confirmed_case.csv and saves it in Visualizations folder

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def graph(dataframe, index):
    df = dataframe
    Y = list(df.iloc[index, 1:])
    plt.plot(np.arange(df.shape[1] - 1), Y)
    plt.ylabel(df.iloc[index,0] + " cases")
    plt.xlabel("10 minute interval count since (3/18/2020 18:53)")
    plt.title(df.iloc[index,0] + " cases over time")
    plt.savefig("Visualizations/" + df.iloc[index, 0] + ".png")
    plt.close()


    
    
def main():
    df = pd.read_csv("Confirmed_case.csv")

    for x in range(df.shape[0]):
        graph(df, x)
    print("Successfully updated graphs")
        
if __name__ == "__main__":
    main()