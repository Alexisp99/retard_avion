# 1. Library imports
import uvicorn
from fastapi import FastAPI
from model import PlaneModel, Delay

# 2. Create app and model objects
app = FastAPI()
model = PlaneModel()

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted flower species with the confidence
@app.get('/predict')

def predict_lateplane(iris: Delay):
    data = iris.dict()
    prediction, probability = model.lateplane(
        data['QUARTER'], data['MONTH'], data['DAY_OF_MONTH'], data['DAY_OF_WEEK'], data['CRS_DEP_TIME'],
         data['DEP_DELAY'], data['CRS_ARR_TIME'], data['DISTANCE']
    )
    return {
        'prediction': prediction,
        'probability': probability
    }




# 4. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)