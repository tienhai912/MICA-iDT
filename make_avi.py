









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