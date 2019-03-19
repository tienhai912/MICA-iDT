import numpy as np
import os
import zipfile
# import cv2

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

def draw_image(image, row, index):
  for j in range(index - 1):
    x = row[j * 2]
    y = row[j * 2 + 1]

    cv2.line(image, (row[j * 2], row[j * 2  + 1]), (row[j * 2  + 2], row[j * 2  + 3]), (0, 255.0*(j+1.0)/(index+1), 0), 2, 8, 0)

  circle(image, (row[index * 2 - 2], row[index * 2  - 1]), 2, Scalar(0,0,255), -1, 8, 0);
  return image

def test_draw(video):
  cap = cv2.VideoCapture(video)
  fourcc = cap.get(CV_CAP_PROP_FOURCC)
  fps = cap.get(CV_CAP_PROP_FPS)
  width = cap.get(CV_CAP_PROP_FRAME_WIDTH)
  height = cap.get(CV_CAP_PROP_FRAME_HEIGHT)
  out = cv2.VideoWriter('out_video.avi', fourcc, fps, (width, height))

  success, image = cap.read()
  count = 0
  while success:
    success, image = cap.read()


    # Todo
    # if count = matrix_frame_num:
    #   image = draw_image(image, )

    count += 1


  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  TEST_FOLDER = 'C:/Users/TienHai/Desktop/iDT/run_iDT/7_1'
  out_features_name = 'out_features.txt'
  out_points_name = 'out_points.txt'
  zip_file_name = 'output.zip'
  input_video = 'video.avi'

  # test_content = read_features_out(TEST_FILE)
  # print(test_content[-1][-1])
  # print(type(test_content[0]))
  unzip_file(os.path.join(TEST_FOLDER, zip_file_name), TEST_FOLDER)

  feature_matrix = read_features_out(os.path.join(TEST_FOLDER, out_features_name))
  point_matrix = read_features_out(os.path.join(TEST_FOLDER, out_points_name))

  merge_matrix = merge_two_matrices_row_by_row(feature_matrix, point_matrix)

  # print(matrix[0][1]+matrix[0][0])
  # print(type(matrix))

  test_matrix = merge_matrix[0:10]
  test_matrix = sort_matrix_by_column_desc(test_matrix, 5)
  test_matrix = test_matrix[0:10]
  print(test_matrix[0:1,439:469])
  print(test_matrix[0:1,-1])

  # print([i for i in range(10,40,2)])
  # print('Length: ' + str(matrix[0, 5]))
  # ava_x = np.sum([matrix[0, i] for i in range(10,40,2)])
  # ava_y = np.sum([matrix[0, i] for i in range(11,40,2)])
  # print(ava_x)
  # print(ava_y)
  # print('Ava displacement: ' + str(matrix[0, 5]))



  # save_out(TEST_FOLDER + 'out.features__2', matrix)
  # a = a[np.argsort( a[:,1] )]

  os.remove(os.path.join(TEST_FOLDER, out_features_name))
