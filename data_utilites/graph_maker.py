import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def create_base_graph(csv_file):
    df = pd.read_csv(csv_file)
    plt.plot(df["Date/Time"],df["Temperature"])

    # for i in range(0,5):
    #     poly = np.poly1d(np.polyfit(df_time,df["Bytes"],i))
    #     new_x = np.linspace(df_time[0],df_time[-1])
    #     new_y = poly(new_x)
    #     plt.plot(new_x, new_y,label="Polynomial %i" %i)
    # print(f"The error is: {error_calc(poly,df_time,df['Bytes'])} for {i}")

    plt.title("Temprature over time")
    plt.xlabel("Date/Time")
    plt.ylabel("Temperature")
    plt.savefig("./Output.png")
    plt.close()

create_base_graph("../Output.csv")