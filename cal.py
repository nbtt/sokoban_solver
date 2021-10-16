# Calculate average values of csv files
import pandas as pd
import os

if __name__ == "__main__":
    file_names = ("all_bfs-mini_cosmos", "all_bfs-micro_cosmos", "all_gbs-mini_cosmos", "all_gbs-micro_cosmos")
    
    for file_name_raw in file_names:
        file_name = os.path.join("stat_saved", file_name_raw + ".csv")
        data = pd.read_csv(file_name)
        count_all = data.shape[0]
        data = data.loc[data["Solution"] != "Not Found"]
        count_remain = data.shape[0]
        print(file_name_raw)
        print(data.mean(axis=0))
        print("Success rate:", count_remain/count_all)