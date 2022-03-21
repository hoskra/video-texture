from copyreg import constructor
import sys
import os
import numpy as np
import cv2

import part0
import part1
import part2

def markIndexesRed(path, i, j, name):
  img = cv2.imread(path)
  maximum = img.shape[0] - 1
  offset = 2

  for x in range(i-offset, i+offset):
    if x >= 0 and x < maximum:
      for y in range(j-offset, j+offset):
        if y >= 0 and y < maximum:
          img[x, x][2] = 255
          img[y, y][2] = 255
          img[x, y][2] = 255
          img[y, x][2] = 255


  cv2.imwrite(name, img)

def viz_diff(diff):
  return (((diff-diff.min())/(diff.max()-diff.min()))*255).astype(np.uint8)

def run_texture(img_list):
  ''' This function administrates the extraction of a video texture from the given
  frames.'''
  video_volume = part0.video_volume(img_list)

  diff1 = part0.ssd(video_volume)
  diff2 = part1.diff2(diff1)

  alpha = 1.5*10**6
  idxs = part2.find_biggest_loop(diff2, alpha)

  diff3 = np.zeros(diff2.shape, float)

  for i in range(diff2.shape[0]):
    for j in range(diff2.shape[1]):
      diff3[i,j] = alpha*(i-j) - diff2[i,j]

  return viz_diff(diff1), viz_diff(diff2), viz_diff(diff3), idxs

def getVideoVolume(img_list):
  return part0.video_volume(img_list)

if __name__ == "__main__":
  print('Performing unit tests.')
  if not part0.test():
    print('part0 failed. halting')
    sys.exit()

  if not part1.test():
    print('part1 failed. halting')
    sys.exit()

  if not part2.test():
    print('part2 failed. halting')
    sys.exit()

  print('Unit tests passed.')
  sourcefolder = os.path.abspath(os.path.join(os.curdir, 'videos', 'source'))
  outfolder = os.path.abspath(os.path.join(os.curdir, 'videos', 'out'))

  print('Searching for video folders in {} folder'.format(sourcefolder))

  # Extensions recognized by opencv
  exts = ['.bmp', '.pbm', '.pgm', '.ppm', '.sr', '.ras', '.jpeg', '.jpg',
    '.jpe', '.jp2', '.tiff', '.tif', '.png']

  # create folder if not exist
  savedDifferencesFolder = "savedDifferences"
  if not os.path.exists(savedDifferencesFolder):
    os.makedirs(savedDifferencesFolder)

  # For every image in the source directory
  for viddir in os.listdir(sourcefolder):
    print("collecting images from directory {}".format(viddir))
    img_list = []
    filenames = sorted(os.listdir(os.path.join(sourcefolder, viddir)))

    for filename in filenames:
      name, ext = os.path.splitext(filename)
      if ext in exts:
        img_list.append(cv2.imread(os.path.join(sourcefolder, viddir, filename)))

    print("trying to load computed differences.")
    if os.path.exists(os.path.join(savedDifferencesFolder, viddir)):
      diff1 = np.loadtxt(os.path.join(savedDifferencesFolder, viddir, 'diff1.txt'))
      diff2 = np.loadtxt(os.path.join(savedDifferencesFolder, viddir, 'diff2.txt'))
      diff3 = np.loadtxt(os.path.join(savedDifferencesFolder, viddir, 'diff3.txt'))
      idxs = np.loadtxt(os.path.join(savedDifferencesFolder, viddir, 'idxs.txt'))
    else:
      print("extracting video texture frames.")
      diff1, diff2, diff3, idxs = run_texture(img_list)
      os.makedirs(os.path.join(savedDifferencesFolder, viddir))
      np.savetxt(os.path.join(savedDifferencesFolder, viddir, 'diff1.txt'), diff1, fmt="%f")
      np.savetxt(os.path.join(savedDifferencesFolder, viddir, 'diff2.txt'), diff2, fmt="%f")
      np.savetxt(os.path.join(savedDifferencesFolder, viddir, 'diff3.txt'), diff3, fmt="%f")
      np.savetxt(os.path.join(savedDifferencesFolder, viddir, 'idxs.txt'), idxs, fmt="%d")

    video_volume = getVideoVolume(img_list)
    out_list = part2.synthesize_loop(video_volume, int(idxs[0])+2, int(idxs[1])+2)

    cv2.imwrite(os.path.join(outfolder, '{}diff1.png'.format(viddir)), diff1)
    cv2.imwrite(os.path.join(outfolder, '{}diff2.png'.format(viddir)), diff2)
    cv2.imwrite(os.path.join(outfolder, '{}diff3.png'.format(viddir)), diff3)

    markIndexesRed(os.path.join(outfolder, '{}diff1.png'.format(viddir)),int(idxs[0]),int(idxs[1]),'out/'+viddir+'_diff1_color.png')
    markIndexesRed(os.path.join(outfolder, '{}diff2.png'.format(viddir)),int(idxs[0]),int(idxs[1]),'out/'+viddir+'_diff2_color.png')
    markIndexesRed(os.path.join(outfolder, '{}diff3.png'.format(viddir)),int(idxs[0]),int(idxs[1]),'out/'+viddir+'_diff3_color.png')

    print("writing output to {}".format(os.path.join(outfolder, viddir)))
    if not os.path.exists(os.path.join(outfolder, viddir)):
      os.mkdir(os.path.join(outfolder, viddir))

    for idx, image in enumerate(out_list):
      cv2.imwrite(os.path.join(outfolder,viddir,'frame{0:04d}.png'.format(idx)), image)
