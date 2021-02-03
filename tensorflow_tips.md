### Read image file via tensorflow
```
import tensorflow as tf

# read file as tf.Tensor dtype=string
img_raw = tf.io.read_file(img_path) # ex. img_path = /root/.keras/datasets/flower_photos/tulips/4575963749_2418ff8768.jpg
# Detects whether an image is a BMP, GIF, JPEG, or PNG, and performs the appropriate operation to convert the input bytes string into a Tensor of type dtype.
# Default dtype is tf.dtypes.uint8
img_tensor = tf.image.decode_image(img_raw)
img_tensor.shape
## ex. -> TensorShape([314, 500, 3])

# Or, decode_jpep along with dct_method="INTEGER_ACCURATE") is better if file is jpg ?
img_tensor = tf.image.decode_jpeg(img_raw,dct_method="INTEGER_ACCURATE")

# resize
img_final = tf.image.resize(img_jpeg, [192, 192])
# normalize to [0,1] range
image_final /= 255.0

# concrete method
def load_image_into_numpy_array(path):
  """Load an image from file into a numpy array.

  Puts image into numpy array to feed into tensorflow graph.
  Note that by convention we put it into a numpy array with shape
  (height, width, channels), where channels=3 for RGB.

  Args:
    path: the file path to the image

  Returns:
    uint8 numpy array with shape (img_height, img_width, 3)
  """
  image = None
  if(path.startswith('http')):
    response = urlopen(path)
    image_data = response.read()
    image_data = BytesIO(image_data)
    image = Image.open(image_data)
  else:
    image_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(image_data))

  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (1, im_height, im_width, 3)).astype(np.uint8)
```

### Construct tf.data.Dataset
```
# preparation
import pathlib
data_root_orig = tf.keras.utils.get_file(origin='https://storage.googleapis.com/download.tensorflow.org/example_images/flower_photos.tgz',
                                         fname='flower_photos', untar=True)
data_root = pathlib.Path(data_root_orig)
print(data_root)
## -> /home/kbuilder/.keras/datasets/flower_photos
all_image_paths = list(data_root.glob('*/*'))

# Create Dataset : the easiest way
path_ds = tf.data.Dataset.from_tensor_slices(all_image_paths)
for s in path_ds.take(1):
  print(s)
  ## ex. -> tf.Tensor(b'/root/.keras/datasets/flower_photos/tulips/4575963749_2418ff8768.jpg', shape=(), dtype=string)
  print(s.numpy())
  ## ex. -> b'/root/.keras/datasets/flower_photos/tulips/4575963749_2418ff8768.jpg'

# Apply transformation such as preprocess function to Dataset
## Prepare preprocess function
def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize(image, [192, 192])
  image /= 255.0  # normalize to [0,1] range

  return image

def load_and_preprocess_image(path):
  image = tf.io.read_file(path)
  return preprocess_image(image)

## Then, mapping
image_ds = path_ds.map(load_and_preprocess_image, num_parallel_calls=AUTOTUNE)

## Also, zip
label_ds = tf.data.Dataset.from_tensor_slices(tf.cast(all_image_labels, tf.int64))
ds = tf.data.Dataset.zip((image_ds, label_ds))
ds = ds.apply(
    tf.data.experimental.shuffle_and_repeat(buffer_size=image_count))
BATCH_SIZE = 32
AUTOTUNE = tf.data.experimental.AUTOTUNE
ds=ds.batch(BATCH_SIZE).prefetch(AUTOTUNE)

plt.figure(figsize=(8,8))
for n,record in enumerate(ds.take(3)):
  plt.subplot(1,3,n+1)
  plt.imshow(record[0])
  plt.xlabel(record[1].numpy())
  plt.grid(False)
  plt.xticks([])
plt.show()

## split to train and val
train_ds = ds.take(100)
val_ds = ds.skip(100)
```
