import os
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import cv2
import pickle # save the structured data frame in pickle format. output will be a .pickle file
import sklearn

PATHS = {
  'haarPath': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/haarcascades', 'haarcascade_frontalface_default.xml'),
  'meanOfAllImagesPath': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/MODEL_predict_gender', 'mean_preprocess.pickle'),
  'modelSVM': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/MODEL_predict_gender', 'model_svm.pickle'),
  'pca_100': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/MODEL_predict_gender', 'pca_100.pickle'),
  'predictedImages': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/predictedImages')
}

haarPath = os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/haarcascades', 'haarcascade_frontalface_default.xml')

# apply haar cascade classifier
haar = cv2.CascadeClassifier(PATHS['haarPath'])
# pickle files
meanOfAllImages = pickle.load(open(PATHS['meanOfAllImagesPath'], 'rb'))
MODEL_SVM = pickle.load(open(PATHS['modelSVM'], 'rb'))
MODEL_PCA = pickle.load(open(PATHS['pca_100'], 'rb'))

print('Model loaded successfully')

# settings
gender_pre = ["Male", "Female"]
font = cv2.FONT_HERSHEY_SIMPLEX

# crop image
def crop_image(img, x, y, w, h):
  cropped_img = img[y:y+h, x:x+w]
  return cropped_img

# detect face on image
def face_detect_and_crop(img, grayImg):
  faces = haar.detectMultiScale(grayImg, 1.5, 3)
  croppedFaces = []
  # if faces are detected
  if len(faces) > 0:
    # draw green rectangle on the detected faces
    for face in faces:
      xPosition = face[0]
      yPosition = face[1]
      width = face[2]
      height = face[3]

      greenColor = (0, 255, 0)
      cv2.rectangle(img, (xPosition, yPosition), (xPosition + width, yPosition + height), greenColor, 3)
      dimensions = {
        'x': xPosition,
        'y': yPosition,
        'w': width,
        'h': height
      }
      imgObj = {
        'img': crop_image(grayImg, **dimensions),
        'dimensions': dimensions
      }
      croppedFaces.append(imgObj)

  return croppedFaces

def predict_gender_from_image(imgPath, color, filename):
  try:
    img = cv2.imread(imgPath)
    # convert into gray scale
    if color == 'bgr':
      grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
      grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    croppedImages = face_detect_and_crop(img, grayImg)

    for croppedImgObj in croppedImages:
      croppedImg = croppedImgObj['img']
      dimensions = croppedImgObj['dimensions']
      # Normalization (0 - 1)
      croppedImg = croppedImg / 255.0
      # Resize images (100, 100)
      width = croppedImg.shape[0] # by using [0], we get width of the image

      croppedImg_resized = None # initalize variable

      if width >= 100: # shrink
        croppedImg_resized = cv2.resize(croppedImg, (100, 100), cv2.INTER_AREA) # SHRINK IMAGE
      else: # enlarge
        croppedImg_resized = cv2.resize(croppedImg, (100, 100), cv2.INTER_CUBIC) # ENLARGE IMAGE
      
      # step - 6: flatten image (1 x 10000) i.e. 1 by 10000 columns
      flattenedImage = croppedImg_resized.reshape(1, -1) # 1, -1
      # step - 7: Subtract with mean
      flattenedImage_mean = flattenedImage - meanOfAllImages
      # flattenedImage_mean = flattenedImage - meanOfAllImages

      print(flattenedImage_mean.shape, 'flattenedImage_mean-------')
      # step - 8: Get Eigen image
      eigen_image = MODEL_PCA.transform(flattenedImage_mean)

      # step - 9: pass to ML model (SVM)
      # print('eigen_image', eigen_image)
      results = MODEL_SVM.predict_proba(eigen_image)[0]

      # step - 10: get predicted values
      predict = results.argmax() # we receive 0 or 1
      # where 0 = male and 1 = female
      score = results[predict]

      # step - 11: write text on the image and save it
      text = "%s : %0.2f"%(gender_pre[predict], score*100)
      cv2.putText(img, text+'%', (dimensions['x'], dimensions['y']-5), font, 1, (0, 255, 0), 2)
      # save predicted image
      cv2.imwrite(PATHS['predictedImages']+'/{}'.format(filename), img)
      
    return {
        'status': 'success', 'message': 'Gender prediction completed', 'predictedImage': PATHS['predictedImages']+'/'+filename,
        'predictedFolderPath': PATHS['predictedImages']
      }
  except Exception as e:
    print('error--on--predicting gender from image', e)
    return { 'status': 'failed', 'message': 'Failed to predict gender from image.' }
