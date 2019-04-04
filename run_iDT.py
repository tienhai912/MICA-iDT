import os
import subprocess
import zipfile
from datetime import datetime

def list_all_folders_in_a_directory(directory):
    folder_list = (folder_name for folder_name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder_name)))
    return folder_list
    pass

if __name__ == '__main__':
  input_video_name = 'video.avi'
  output_video_name = 'trajectories.avi'
  features_output_name = 'out.features'
  out_features_name = 'out_features.txt'
  run_file_path = '/home/dangmanhtruong95/NTHai/improved_trajectory_release/release/DenseTrackStab'
  output_root_folder = '/home/dangmanhtruong95/NTHai/iDT_output/'
  input_root_folder = '/media/data2/users/dangmanhtruong95/12gestures_videos'
  trajectories_video_path = '/home/dangmanhtruong95/NTHai/improved_trajectory_release/trajectories.avi'
  out_points_path = '/home/dangmanhtruong95/NTHai/improved_trajectory_release/out_points.txt'
  out_features_path = '/home/dangmanhtruong95/NTHai/improved_trajectory_release/out_features.txt'
  output_zip = '/home/dangmanhtruong95/NTHai/improved_trajectory_release/output.zip'
  # people = ['Giang', 'Hai', 'Long', 'Minh', 'Thuan', 'Thuy', 'Tuyen']
  kinects = ['Kinect_1', 'Kinect_2', 'Kinect_3', 'Kinect_4', 'Kinect_5']

  people = ['Thuy', 'Tuyen']
  # kinects = ['Kinect_1']

  start = datetime.now()

  for person in people:
    for kinect in kinects:
      file_list = list_all_folders_in_a_directory(os.path.join(input_root_folder, person, kinect))
      # file_list = ['10_1']
      for file in file_list:
        file_video_start = datetime.now()
        input_video_path = os.path.join(input_root_folder, person, kinect, file, input_video_name)
        output_path = os.path.join(output_root_folder, person, kinect, file)
        print('Running at: ' + input_video_path + ' from ' + str(file_video_start))
        output_feature_path = os.path.join(output_path, features_output_name)
        # Run
        subprocess.run([run_file_path, input_video_path])
        # Check output directory existance
        if not os.path.exists(os.path.dirname(output_feature_path)):
          try:
            os.makedirs(os.path.dirname(output_feature_path))
          except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
              raise

        zip = zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED)
        zip.write(out_features_path, arcname=out_features_name)
        zip.close()
        # Write out.features file
        # with open(output_feature_path, 'w+') as f:
        #   f.write(result.stdout.decode('utf-8'))
        # Move output zip from code folder to output folder
        subprocess.run(['mv', output_zip, output_path])
        # Move output point from code folder to output folder
        subprocess.run(['mv', out_points_path, output_path])
        # Move video from code folder to output folder
        # subprocess.run(['mv', trajectories_video_path, output_path])
        print('Finished ' + input_video_path + ' at ' + str(datetime.now()) + ' in ' + str(datetime.now() - file_video_start))
