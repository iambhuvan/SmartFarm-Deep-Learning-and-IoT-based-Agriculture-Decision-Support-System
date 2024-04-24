from joblib import dump, load
import random as rd
import systemcheck
crops = ['rice',
 'maize',
 'chickpea',
 'kidneybeans',
 'pigeonpeas',
 'mothbeans',
 'mungbean',
 'blackgram',
 'lentil',
 'pomegranate',
 'banana',
 'mango',
 'grapes',
 'watermelon',
 'muskmelon',
 'apple',
 'orange',
 'papaya',
 'coconut',
 'cotton',
 'jute',
 'coffee']


def predict_soil_quality(Input):
    
    loaded_model = load("files/RandomForest.joblib")
    scaler = load("files/scaler.joblib")

    scaled = scaler.transform([Input])
    prediction = loaded_model.predict(scaled)
    print(Input)
    if 0 in Input:
        return 'Inaccurate Soil Information'
    if Input[2] // Input[1] == 2 and Input[1] // Input[0] == 1:
        return "Poor Quality"
    if Input[3] <= 5 or Input[3] > 9:
        return "Poor Quality"
    if Input[0] // Input[2] == 4 and Input[0] // Input[1] == 2 and Input[1] // Input[2] == 2:
        return "Very Good Quality"
    if prediction == [0]:
        return "Average Quality"
    if prediction == [1]:
        return "Good Quality"
    if prediction == [2]:
        return "Very Good Quality"
    
def cropRecom(Data):
    load_model = load("files/CropRandomForest.joblib")
    prediction = load_model.predict([Data])
    crps = [item for item in crops if item != prediction]
    # c1 = rd.choice(crps)
    # return f"{prediction[0]},{c1}"
    return f"{prediction[0]}"

if __name__ == "__main__":
    print(cropRecom([138,8.6,560,7.46,25.616244,80.473146]))
    print(predict_soil_quality([138,8.6,560,7.46,25.616244,80.473146,100.0]))