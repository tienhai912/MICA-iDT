import numpy as np
import os
import zipfile
from datetime import datetime
import logging

for handler in logging.root.handlers[:]:
  logging.root.removeHandler(handler)

logging.basicConfig(filename='select_iDT.log', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('Hai')

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

  matrix = np.array([x.strip().split('\t') for x in content], dtype='float64')
  return matrix

def save_out(file_path, data):
  with open(file_path, 'wb') as f:
    np.savetxt(f, data, delimiter='\t')

def sort_matrix_by_column_desc(matrix, column_num):
  return matrix[matrix[:,column_num].argsort()[::-1]]

def merge_two_matrices_row_by_row(matrix1, matrix2):
  return np.concatenate((matrix1, matrix2), axis=1)

def add_row_number_to_matrix(matrix):
  return merge_two_matrices_row_by_row(np.arange(matrix.shape[0]).reshape((-1, 1)), matrix)

def sort_trajectory(file_path, column_num):
  out_features_name = 'out_features.txt'
  zip_file_name = 'output.zip'
  sorted_by_length = 'out_features_sorted_by_length.txt'
  sorted_by_length_zip = 'out_features_sorted_by_length.zip'

  unzip_file(os.path.join(file_path, zip_file_name), file_path)

  feature_matrix = read_features_out(os.path.join(file_path, out_features_name))

  # Add ID (or row number) to the first column
  feature_matrix =  add_row_number_to_matrix(feature_matrix)
  # 6 = length column
  feature_matrix = sort_matrix_by_column_desc(feature_matrix, column_num + 1)
  # Take top 200 features
  save_matrix = feature_matrix[:200]

  with open(os.path.join(file_path, sorted_by_length),'wb') as f:
    np.savetxt(f, save_matrix, fmt='%7f', delimiter='\t')


  with zipfile.ZipFile(os.path.join(file_path, sorted_by_length_zip), 'w', zipfile.ZIP_DEFLATED) as zip:
    zip.write(os.path.join(file_path, sorted_by_length), arcname=sorted_by_length)
    zip.close()

  os.remove(os.path.join(file_path, out_features_name))
  os.remove(os.path.join(file_path, sorted_by_length))

def run_sort_by_length():
  start = datetime.now()
  original_length_column = 5
  input_root_folder = '/home/dangmanhtruong95/NTHai/iDT_output/'

  people = ['Giang', 'Hai', 'Long', 'Minh', 'Thuan', 'Thuy', 'Tuyen']
  kinects = ['Kinect_1', 'Kinect_2', 'Kinect_3', 'Kinect_4', 'Kinect_5']

  # people = ['Giang']
  # kinects = ['Kinect_1']

  for person in people:
    for kinect in kinects:
      folder_list = list_all_folders_in_a_directory(os.path.join(input_root_folder, person, kinect))
      # folder_list = ['10_1', '10_2']
      for folder in folder_list:
        temp_start = datetime.now()

        input_features_folder = os.path.join(input_root_folder, person, kinect, folder)
        sort_trajectory(input_features_folder, original_length_column)

        logger.info('Finished ' + input_features_folder + ' in ' + str(datetime.now() - temp_start))

  logger.info('Finished all in ' + str(datetime.now() - start))

def test_sort():
  TEST_FOLDER = 'C:/Users/TienHai/Desktop/iDT/run_iDT/7_1'
  out_features_name = 'out_features.txt'
  out_points_name = 'out_points.txt'
  zip_file_name = 'output.zip'
  input_video = 'video.avi'
  sorted_out_features_name = 'out_features_sorted_by_length.txt'

  # test_content = read_features_out(TEST_FILE)
  # print(test_content[-1][-1])
  # print(type(test_content[0]))
  unzip_file(os.path.join(TEST_FOLDER, zip_file_name), TEST_FOLDER)

  feature_matrix = read_features_out(os.path.join(TEST_FOLDER, out_features_name))
  point_matrix = read_features_out(os.path.join(TEST_FOLDER, out_points_name))

  # merge_matrix = merge_two_matrices_row_by_row(feature_matrix, point_matrix)

  # merge_matrix =  add_row_number_to_matrix(merge_matrix)

  # print(type(merge_matrix))
  # print(merge_matrix[0:5,0:3])
  # print(merge_matrix.shape[0])

  # test_matrix = merge_matrix[0:10]

  # test_matrix = sort_matrix_by_column_desc(test_matrix, 6)

  # test_matrix = test_matrix[0:10]
  # print(test_matrix[0:1,439:469])
  # print(test_matrix[0:1,439:-1])
  # print(test_matrix[0:1,-1])
  # print(test_matrix[0:10,0:10])


  # print([i for i in range(10,40,2)])
  # print('Length: ' + str(matrix[0, 5]))
  # ava_x = np.sum([matrix[0, i] for i in range(10,40,2)])
  # ava_y = np.sum([matrix[0, i] for i in range(11,40,2)])
  # print(ava_x)
  # print(ava_y)
  # print('Ava displacement: ' + str(matrix[0, 5]))



  # save_out(TEST_FOLDER + 'out.features__2', matrix)
  # a = a[np.argsort( a[:,1] )]

  # sorted_feature_matrix = np.loadtxt(os.path.join(TEST_FOLDER, sorted_out_features_name), delimiter='\t')
  # print(sorted_feature_matrix)
  # print(type(sorted_feature_matrix))
  print(point_matrix)
  print(type(point_matrix))

  os.remove(os.path.join(TEST_FOLDER, out_features_name))


if __name__ == '__main__':
  logger.info('Start')
  run_sort_by_length()
