import numpy as np
import os
import zipfile
from datetime import datetime
# import cv2

def list_all_folders_in_a_directory(directory):
  folder_list = (folder_name for folder_name in os.listdir(directory)
    if os.path.isdir(os.path.join(directory, folder_name)))
  return folder_list
  pass

def unzip_file(zip_file, unzip_folder):
  with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(unzip_folder)

def read_features_out(file_path):
  with open(file_path, 'r') as f:
    content = f.readlines()

def draw_image(image, row, index):
  for j in range(index):
    x = row[j * 2]
    y = row[j * 2 + 1]

    cv2.line(image, (row[j * 2], row[j * 2  + 1]), (row[j * 2  + 2], row[j * 2  + 3]), (0, 255.0*(j+1.0)/(index+1), 0), 2, 8, 0)

  cv2.circle(image, (row[index * 2 - 2], row[index * 2  - 1]), 2, (0,0,255), -1, 8, 0);
  return image

def draw_video(video, sorted_features_matrix, points_matrix):
  for i in range(200):
    row_num = sorted_features_matrix[i, 0]
    frame_num = sorted_features_matrix[i, 1]
    draw_image(video[frame_num], points_matrix[row_num, 3:-1], points_matrix[row_num, 1])

def get_draw_video(input_features_folder, input_video_folder):
  sorted_zip_file_name = 'out_features_sorted_by_length.zip'
  sorted_out_features_name = 'out_features_sorted_by_length.txt'
  out_points_name = 'out_points.txt'
  input_video = 'video.avi'
  output_video = 'out_video.avi'

  cap = cv2.VideoCapture(os.path.join(input_video_folder, input_video))
  fourcc = cap.get(CV_CAP_PROP_FOURCC)
  fps = cap.get(CV_CAP_PROP_FPS)
  width = cap.get(CV_CAP_PROP_FRAME_WIDTH)
  height = cap.get(CV_CAP_PROP_FRAME_HEIGHT)
  out = cv2.VideoWriter(os.path.join(input_features_folder, output_video), fourcc, fps, (width, height))

  unzip_file(os.path.join(input_features_folder, sorted_zip_file_name), input_features_folder)

  sorted_features_matrix = read_features_out(os.path.join(input_features_folder, sorted_out_features_name))

  points_matrix = read_features_out(os.path.join(input_features_folder, out_points_name))

  video = []
  success, image = cap.read()

  while success:
    video.append(image)
    success, image = cap.read()

  draw_video(video, sorted_features_matrix, points_matrix)

  for frame in video:
    out.write(frame)

  cap.release()
  out.release()
  cv2.destroyAllWindows()

def run_draw_video():
  start = datetime.now()
  input_root_folder = '/home/dangmanhtruong95/NTHai/iDT_output/'
  input_root_video_folder = '/media/data2/users/dangmanhtruong95/12gestures_videos/'

  # people = ['Giang', 'Hai', 'Long', 'Minh', 'Thuan', 'Thuy', 'Tuyen']
  # kinects = ['Kinect_1', 'Kinect_2', 'Kinect_3', 'Kinect_4', 'Kinect_5']

  people = ['Giang']
  kinects = ['Kinect_1']

  for person in people:
    for kinect in kinects:
      # file_list = list_all_folders_in_a_directory(os.path.join(input_root_folder, person, kinect))
      file_list = ['10_1', '10_2']
      for file in file_list:
        temp_start = datetime.now()

        input_features_folder = os.path.join(input_root_folder, person, kinect, file)
        input_video_folder = os.path.join(input_root_video_folder, person, kinect, file)
        get_draw_video(input_features_folder, input_video_folder)

        print('Finished ' + input_features_folder + ' at ' + str(datetime.now()) + ' in ' + str(datetime.now() - temp_start))

  print('Finished all at ' + str(datetime.now()) + ' in ' + str(datetime.now() - start))


# void DrawTrack(const std::vector<Point2f>& point, const int index, const float scale, Mat& image)
# {
#   Point2f point0 = point[0];
#   point0 *= scale;

#   for (int j = 1; j <= index; j++) {
#     Point2f point1 = point[j];
#     point1 *= scale;

#     line(image, point0, point1, Scalar(0,cvFloor(255.0*(j+1.0)/float(index+1.0)),0), 2, 8, 0);
#     point0 = point1;
#   }
#   circle(image, point0, 2, Scalar(0,0,255), -1, 8, 0);
# }

if __name__ == '__main__':
  run_draw_video()