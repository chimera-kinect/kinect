import cv2
import numpy as np
import os

def view(frames, fps):
  while True:
    for frame in frames:
      cv2.imshow('frame', frame)
      key = cv2.waitKey(1000 // fps)
      if key != -1:
        cv2.destroyAllWindows()
        return

def main():
  os.chdir(os.path.dirname(os.path.abspath(__file__))) # cd to the directory of this file
  
  recordings = []
  print('What file should I load?')

  # check utilities/recordings folder and list npy files with their index
  for file in os.listdir('recordings'):
    if file.endswith('.npy'):
      recordings.append(file)
      print(f'{len(recordings)}. {file}')

  fileIndex = int(input()) - 1
  while fileIndex not in range(len(recordings)):
    print('Invalid input, try again.')
    fileIndex = int(input()) - 1
  loaded_frames = np.load(f'recordings/{recordings[fileIndex]}')
  print(f'\nLoaded {len(loaded_frames)} frames from {recordings[fileIndex]}.')

  print('How many frames/s?')
  print('1. 15')
  print('2. 30')
  fps = int(input())
  while fps not in [1, 2]:
      print('Invalid input, try again.')
      fps = int(input())
  fps = 15 if fps == 1 else 30

  view(loaded_frames, fps)

if __name__ == "__main__":
    main()