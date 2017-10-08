import os
import time
import tensorflow as tf
import shutil
import subprocess
import constants

RPI_IP,MAC_IP=constants.read_IP()

PORT_OP='~/Documents/Academics/IIT\ M/Projects/Smart\ DB/mac_interface/ssh_output/'
PORT_RPI='pi@'+RPI_IP+':~/Desktop/raspberry/ssh_output/'
with tf.Session() as persisted_sess:
    # Load Graph
    with tf.gfile.FastGFile("./retrained_graph.pb",'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        persisted_sess.graph.as_default()
        tf.import_graph_def(graph_def, name='')

softmax_tensor = tf.Session().graph.get_tensor_by_name('final_result:0')

while (True):
    if os.path.isfile('./ssh_input/resized_input.jpg'):
        time.sleep(0.1)
        image_path = '/resized_input.jpg'
        # Read in the image_data
        image_path='./ssh_input/'+image_path
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        label_lines = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]

        output={}

        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            #softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor, \
                     {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                print('%s (score = %.5f)' % (human_string, score))
                output[human_string]=score


        #Sort output
        keys=output.keys()
        keys.sort()
        vision_features=[]

        for i in keys:
            vision_features.append(str(output[i])+'\n')

        with open('./ssh_output/ssh_output.txt','w+') as file:
            file.writelines(vision_features)

        shutil.rmtree('./ssh_input')
        os.mkdir('./ssh_input')

        print PORT_RPI
        print RPI_IP

        subprocess.call(['sshpass','-p','raspberry','rsync','./ssh_output/ssh_output.txt',PORT_RPI])
    else:
        time.sleep(0.01)
        continue
