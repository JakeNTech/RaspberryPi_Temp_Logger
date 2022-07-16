from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def all_time_temp(csv_file):
    df = pd.read_csv(csv_file)
    df_time = list(range(0,len(df["Date/Time"])))

    plt.rcParams["figure.figsize"] = (20,10)
    plt.plot(df_time,df["Temperature(S1)"],label="Sensor_1")
    plt.plot(df_time,df["Temperature(S2)"],label="Sensor_2")
    plt.plot(df_time,df["Average_Temp"],label="Average")

    # for i in range(0,5):
    #     poly = np.poly1d(np.polyfit(df_time,df["Bytes"],i))
    #     new_x = np.linspace(df_time[0],df_time[-1])
    #     new_y = poly(new_x)
    #     plt.plot(new_x, new_y,label="Polynomial %i" %i)
    # print(f"The error is: {error_calc(poly,df_time,df['Bytes'])} for {i}")

    plt.title("Temprature over time")
    plt.xlabel("Date/Time")
    plt.grid(True)
    plt.ylabel("Temperature")
    plt.legend()
    plt.savefig("./static/assets/temp_storage/all_time_temp.png")
    #plt.savefig("./output.png")
    plt.close()

if __name__ == "__main__":
    all_time_temp("../test_data/test_2.csv")