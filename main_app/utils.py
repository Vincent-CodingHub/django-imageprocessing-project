from django.core.files.storage import FileSystemStorage
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
from tensorflow import Graph
from PIL import Image
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('./models/VGG19.h5')

def get_prediction(fileObj):
  fs=FileSystemStorage()
  filePathName = fs.save(fileObj.name,fileObj)
  filePathName = fs.url(filePathName)
  image_directory='.'+filePathName

  my_image = image.load_img(image_directory, target_size=(224,224))
  my_image_arr = image.img_to_array(my_image)
  my_image_arr = my_image_arr/127.5-1
  my_image_arr = np.expand_dims(my_image_arr, axis=0)

  with model_graph.as_default():
    with tf_session.as_default():
      predictions = model.predict(my_image_arr)

  label = np.argmax(predictions)
  label_dict = {0:'algaeleafspot',1:'bunchrot',2:'charcoalrot', 3:'orangespotting', 4:'sootymold', 5:'stemwetrot'}
  labels = np.array(list(label_dict.values()))
  chart = get_plot(predictions[0], labels)

  context={'filePathName':filePathName,'predictedLabel':label_dict[label], 'chart':chart}
  return context

def get_graph():
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)
  image_png = buffer.getvalue()
  print(image_png)
  graph = base64.b64encode(image_png)
  print(graph)
  graph = graph.decode('utf-8')
  print(graph)
  buffer.close()
  return graph

def get_plot(prediction, labels):
  plt.switch_backend('AGG')
  fig, ax = plt.subplots(figsize =(8, 7))
  x_axis = labels
  y_axis = [float("{:.1f}".format(i*100)) for i in prediction]

  ax.bar(x_axis, y_axis, color=['#5ec576', '#ffcb03', '#ff585f', 'cyan', 'orange', '#066a2d'], edgecolor=['black', 'black', 'black', 'black', 'black', 'black'])

  for index, value in enumerate(y_axis):
    plt.text(index-0.1, value, str(value)+"%")

  plt.xlabel('Palm tree diseases', fontweight='bold', fontsize=15)
  plt.ylabel('Probabilites', fontweight='bold', fontsize=15)
  plt.title('Result of the classification', fontweight='bold', fontsize=15)
  graph = get_graph()
  return graph
