import pandas as pd
import numpy as np
from xgboost import XGBClassifier


class trading_point_selection_xgboost():
    def __init__(self, model_path, params_path):
        self.model_path = model_path
        self.xgb_model = XGBClassifier()
        self.xgb_model.load_model(self.model_path)
        normalization_params = pd.read_csv(params_path)
        self.mean = normalization_params['mean'].to_numpy()
        self.std = normalization_params['std'].to_numpy()
    """
    Input:
        data: np.array shape=(1,10), i.e.
              [[E30, E90, E240, E600, E1500,
               E3600, E7200, E14400, E72000, E144000]]
    Output:
        True: selected trading point
        False: eliminated trading point
    """
    def predict(self, data):
        data = (data - self.mean)/self.std
        y_pred = self.xgb_model.predict(pd.DataFrame(data))
        return not y_pred

if __name__ == "__main__":
    model_path = "./trading_point_selection_xgboost_v1.json"
    params_path = "./normalization_params.csv"
    xgb_model = trading_point_selection_xgboost(model_path, params_path)
    y_pred = xgb_model.predict(np.array([[0,0,0,0,0,0,0,0,0,0]]))
    print(y_pred)
