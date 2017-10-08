'''
Socket for obtaining predictions from preloaded model.

Transfer retrained Inception v3 [OpenImage edition]
'''
import tensorflow as tf
import sys
import time
import json as pickle

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('warmup_runs', 10,
                            "Number of times to run Session before starting test")

def vision_pred(image_path='./input_resized'):
    #call as vision_pred()

    #ouput is a label-score dictionary
    output={}

    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
    # Unpersists graph from file
    '''with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')'''

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]

            output[human_string]=score
            #print('%s (score = %.5f)' % (human_string, score))

def main():
    # change this as you see fit
    image_path = sys.argv[1]
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
    # Unpersists graph from file
    with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))

def main2(saved = None,softmax_tensor2=None):
    # change this as you see fit
    image_path = sys.argv[1]
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()
    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line in tf.gfile.GFile("./retrained_labels.txt")]
    # Unpersists graph from file

    if not saved:
        with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    else:
        softmax_tensor=softmax_tensor2
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


def create_and_persist_graph():
    with tf.Session() as persisted_sess:
        # Load Graph
        with tf.gfile.FastGFile("./retrained_graph.pb",'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            persisted_sess.graph.as_default()
            tf.import_graph_def(graph_def, name='')
        return persisted_sess.graph

if __name__=='__main__':
    start=time.clock()
    main2()
    stop1=time.clock()
    print start-stop1, "With overheads"


    '''with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')'''

    create_and_persist_graph()

    softmax_tensor = tf.Session().graph.get_tensor_by_name('final_result:0')

    image_path = sys.argv[1]
    # Read in the image_data
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    for i in range(FLAGS.warmup_runs):
      predictions = tf.Session().run(softmax_tensor,
                             {'DecodeJpeg/contents:0': image_data})

    L=[]
    for i in range(30):
        stop2=time.clock()
        main2(True,softmax_tensor)
        stop3=time.clock()
        print "\n", stop3-stop2, "ith iteration \t",i
        L.append(i)

    print sum(L)/30
