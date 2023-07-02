import tensorflow as tf

# Check if TensorFlow is using GPU
print(tf.config.list_physical_devices('GPU'))