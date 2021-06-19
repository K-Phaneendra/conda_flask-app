import os
import numpy as np
import cv2

PATHS = {
  'imagesWithFilters': os.path.join(os.path.dirname(os.path.abspath(__file__)) + '/imagesWithFilters')
}

# removes the edges of the image
def edgePreservingFilter(filename, imgPath, widgetParameters):
  try:
    s = int(widgetParameters['sigma_s'])
    r = float(widgetParameters['sigma_r'])

    img = cv2.imread(imgPath)
    edgeImg = cv2.edgePreservingFilter(img, sigma_s=s, sigma_r=r)
    # # save filtered image
    cv2.imwrite(PATHS['imagesWithFilters']+'/{}'.format(filename), edgeImg)
    return {
      'status': 'success',
      'message': 'Filter applied successfully',
      'predictedImage': PATHS['imagesWithFilters']+'/'+filename,
      'predictedFolderPath': PATHS['imagesWithFilters']
    }
  except Exception as e:
    print('error--on--edgePreservingFilter', e)
    return { 'status': 'failed', 'message': 'Failed to convert an image to oilPaint.' }

def applyFilterOnImageByConversionType(filename, imgPath, convesionType, widgetParameters):
  try:
    return {
      'oilPaint': edgePreservingFilter(filename, imgPath, widgetParameters)
    }.get(convesionType)
  except Exception as e:
    print('error--on--converting image to sketch', e)
    return { 'status': 'failed', 'message': 'Failed to apply filter on an image' }
