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

def get_stats(start_date,end_date):
    df = data_reader()
    # if dates have been selected:
    #   filter DataFrame for those dates
    # else:
    #   use whole data frame
    if start_date and end_date != "":
        # https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
        mask = (df["Date/Time"] > start_date) & (df["Date/Time"] <= end_date)
        df = df.loc[mask]
    
    # Average Statistics
    avg_indoor_temp = df["Temperature(Indoor)"].mean()
    avg_outdoor_temp = df["Temperature(Outdoor)"].mean()
    avg_indoor_humid = df["Humidity(Indoor)(%)"].mean()
    avg_outdoor_humid = df["Humidity(Outdoor)(%)"].mean()
    # Maximum values
    max_indoor_temp = df["Temperature(Indoor)"].max()
    max_outdoor_temp = df["Temperature(Outdoor)"].max()
    max_indoor_humid = df["Humidity(Indoor)(%)"].max()
    max_outdoor_humid = df["Humidity(Outdoor)(%)"].max()
    # Minimum Values
    min_indoor_temp = df["Temperature(Indoor)"].min()
    min_outdoor_temp = df["Temperature(Outdoor)"].min()
    min_indoor_humid = df["Humidity(Indoor)(%)"].min()
    min_outdoor_humid = df["Humidity(Outdoor)(%)"].min()
    # Format nicely
    json = {
        "Indoor":{
            "average_temp":avg_indoor_temp,
            "average_humid":avg_indoor_humid,
            "max_temp":max_indoor_temp,
            "min_temp":min_indoor_temp,
            "max_humid":max_indoor_humid,
            "min_humid":min_indoor_humid
        },
        "Outdoor":{
            "average_temp":avg_outdoor_temp,
            "average_humid":avg_outdoor_humid,
            "max_temp":max_outdoor_temp,
            "min_temp":min_outdoor_temp,
            "max_humid":max_outdoor_humid,
            "min_humid":min_outdoor_humid
        }
    }
    return json

def custom_line_graph(sensors,axis,start_date,end_date):
    print("I am a cat")

if __name__ == "__main__":
    temp_humid_line_graph()
