from pydantic import BaseModel
import joblib


# 2. Class which describes a single flower measurements
class Delay(BaseModel):
    QUARTER : int
    MONTH : int
    DAY_OF_MONTH : int
    DAY_OF_WEEK : int
    CRS_DEP_TIME : int
    DEP_DELAY : float
    CRS_ARR_TIME : int
    DISTANCE : float


# 3. Class for training the model and making predictions
class PlaneModel:
    # 6. Class constructor, loads the dataset and loads the model
    #    if exists. If not, calls the _train_model method and
    #    saves the model
    def __init__(self):
        self.model_fname_ = 'model.pkl'
        self.model = joblib.load(self.model_fname_)

    # 5. Make a prediction based on the user-entered data
    #    Returns the predicted species with its respective probability
    def lateplane(self, QUARTER, MONTH, DAY_OF_MONTH, DAY_OF_WEEK, CRS_DEP_TIME, DEP_DELAY, CRS_ARR_DELAY, DISTANCE):
        data_in = [[QUARTER, MONTH, DAY_OF_MONTH, DAY_OF_WEEK, CRS_DEP_TIME, DEP_DELAY, CRS_ARR_DELAY, DISTANCE]]
        prediction = self.model.predict(data_in)
        probability = self.model.predict_proba(data_in).max()
        return prediction[0].item(), probability.item()