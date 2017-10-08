'''
Recieve image_path, call for prediction
'''
import resize
import tf_vision

def predict():
    # outputs [glass,metal,plastic,organic] confidence

    #image must be of form ./input/foo.jpg
    image_resized=resize.rpi_resize()

    output=tf_vision.vision_pred('./input_resized/resized_input.jpg')

    keys=output.keys()
    keys.sort()
    # [glass,metal,plastic,organic]

    vision_features=[]

    for i in keys:
        vision_features.append(output[i])

    return vision_features
