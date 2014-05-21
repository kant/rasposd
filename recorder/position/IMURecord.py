import csv


class IMURecord:

    def __init__(self, path):
        csvfile = open(path, 'rb')
        self.imu_data = csv.reader(csvfile, delimiter='\t', quotechar='"')
        next(self.imu_data, None)  # get header

    def read_all(self):
        return map(float, self.imu_data.next())

