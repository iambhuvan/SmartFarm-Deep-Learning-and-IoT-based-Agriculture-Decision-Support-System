from tensorflow.keras.models import load_model
import cv2
from PIL import Image
import numpy as np

IMAGE_SIZE = (224, 224)  # Remove the third dimension as it is inferred from the model
CATEGORIES = ['Broken', 'Discolored', 'Pure', 'Silkcut']

model = load_model("files/chest_xray_resnet_50_v2_model.h5")

def detection(imgpath):
    img = cv2.imread(imgpath)
    img = cv2.resize(img, (IMAGE_SIZE[0], IMAGE_SIZE[1]))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img, 'RGB')

    image = np.array(img)
    image = image.astype(np.float32)
    image /= 255

    # Add an extra dimension for batch_size
    image = np.expand_dims(image, axis=0)

    pred = model.predict(image)
    pred_class = np.argmax(pred, axis=1)[0]

    print("Final Output:", CATEGORIES[pred_class])
    return CATEGORIES[pred_class]


if __name__=="__main__":
    print(detection(r"test images/img.png"))
    print()
    print(detection(r"test images/img2.png"))
    print()
    print(detection(r"test images/img1.png"))