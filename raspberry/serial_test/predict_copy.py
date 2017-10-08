'''
Recieve image_path, call for prediction
'''
import resize
import tf_vision_faster

def predict(saved=None, softmax_tensor2=None):
    # outputs [glass,metal,plastic,organic] confidence

    #image must be of form ./input/foo.jpg
    image_resized=resize.rpi_resize()

    if not saved:
        output=tf_vision_faster.vision_pred('./input_resized/resized_input.jpg')

    else:
        output=tf_vision_faster.vision_pred('./input_resized/resized_input.jpg',saved,softmax_tensor2)

    keys=output.keys()
    keys.sort()
    # [glass,metal,plastic,organic]

    vision_features=[]

    for i in keys:
        vision_features.append(output[i])

    return vision_features
