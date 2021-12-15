import pandas as pd

def prediction(test_predictions):
	prediction = pd.DataFrame(test_predictions)

	prediction[0] = prediction[0].round().astype(int)
	prediction[1] = prediction[1].round().astype(int)
	prediction[2] = prediction[2].round().astype(int)
	prediction[3] = prediction[3].round().astype(int)
	prediction[4] = prediction[4].round().astype(int)


	def prediction_handle(prediction): #prediction = row
    if (prediction[0] == 1):
        return 0
    elif (prediction[1] == 1):
        return 1
    elif (prediction[2] == 1):
        return 2
    elif (prediction[3] == 1):
        return 3
    elif (prediction[4] == 1):
        return 4
    else:
        return 0

    prediction['prediction'] = prediction.apply (lambda row: prediction_handle(row), axis=1) 


    return prediction['prediction'].values