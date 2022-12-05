import tensorflow as tf

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model("mnist_nn") # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model.
with open('model_nn.tflite', 'wb') as f:
  f.write(tflite_model)