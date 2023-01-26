"""
    将股票数据按年份合并对买点进行映射
"""
import pandas as pd
import os

def data_processing(data_path, year, output_path):

    # collect path of all datafile in folder <data_path/year>
    def get_list(path):
        return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.csv')]
    csv_path = get_list(os.path.join(data_path, str(year)))
    print("csv_path:",csv_path)

    # filter all non-trading data points
    result = pd.DataFrame()
    for path in csv_path:
        data = pd.read_csv(path)
        filter_df = data.loc[data.action_duo != 0].reset_index(drop=True)
        # map_dic = {1:0, 2:0, 3:1, 4:1, 5:1, 6:1} # 映射关系
        filter_df["label_tfm"] = filter_df.label.map(lambda x: -1 if x==0 else 1 if x>=3 else 0)
        if filter_df.shape[0]%2:
            filter_df.drop(filter_df.tail(1).index,inplace=True)
        result = result.append(filter_df)


    # save trading points in <output_path/${year}processed_data>
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    result.to_csv(\
        os.path.join(output_path, str(year)+"processed_data.csv"), \
        encoding="utf_8_sig", index=False)

if __name__ == "__main__":
    data_path = "./data/"
    output_path = "./result/"
    data_processing(data_path, 2020, output_path)
