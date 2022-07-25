import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (20,10)

def data_reader():
    #df = pd.read_csv("./test.csv")
    df = pd.read_csv("./Output.csv")
    # Drop readings that failed
    df = df.dropna()
    # Convert Date time to one that will work with PyPlot
    df["Date/Time"] = pd.to_datetime(df["Date/Time"])

    return df

def temp_humid_line_graph():
    df = data_reader()

    # Plot Graph
    plt.plot(df["Date/Time"],df["Temperature(Outdoor)"], label="Outdoor Temp")
    plt.plot(df["Date/Time"],df["Temperature(Indoor)"], label="Indoor Temp")

    # Make Graph look like a graph
    plt.grid()
    plt.title("Outdoor/Indoor Temperature over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature (C)")
    plt.legend(title="Legend")
    # plt.savefig("./temperature_LG.png")
    plt.savefig("./static/assets/temp_storage/temperature_LG.png")
    plt.close()

    # Plot Graph
    plt.plot(df["Date/Time"],df["Humidity(Outdoor)(%)"], label="Outdoor Temp")
    plt.plot(df["Date/Time"],df["Humidity(Indoor)(%)"], label="Indoor Temp")

    # Make Graph look like a graph
    plt.grid()
    plt.title("Outdoor/Indoor Humidity over Time")
    plt.xlabel("Time")
    plt.ylabel("Humidity (%)")
    plt.legend(title="Legend")
    # plt.savefig("./humidity_LG.png")
    plt.savefig("./static/assets/temp_storage/humidity_LG.png")
    plt.close()
    
if __name__ == "__main__":
    temp_humid_line_graph()
