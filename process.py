import re
import numpy as np

MEAS_FILE = 'sensor.txt'
POINTS_FILE = 'org_v1.txt'
FINAL_FILE = 'output.txt'

# number of point to use to extract base
BASE_POINTS = 45

def process():
    with open(MEAS_FILE, 'r') as f:
        all_txt = f.read()
        # print(all_txt)

        processed = []
        i = 0

        points = all_txt.split('new')
        for point in points:
            processed_point = []
            nums = point.split("\n")
            measures = 0
            total = 0
            for num in nums:
                if num != 'end':
                    new_num = re.sub('[^0-9.]', '', num)
                    if new_num != '':
                        # print(num)
                        # print(new_num)
                        # print(float(new_num))
                        # print('\n')

                        processed_point.append(float(new_num))

                        # total += float(new_num)
                        # measures += 1

            if len(processed_point) != 0:
                # remove outliers from processed point
                pp_arr = np.array(processed_point)
                q75,q25 = np.percentile(pp_arr,[75,25])
                intr_qr = q75-q25

                max = q75+(1.5*intr_qr)
                min = q25-(1.5*intr_qr)

                pp_arr[pp_arr < min] = np.nan
                pp_arr[pp_arr > max] = np.nan
                pp_arr = pp_arr[~np.isnan(pp_arr)]

                processed_point = pp_arr.tolist()

                out_min = pp_arr[pp_arr < min]
                out_max = pp_arr[pp_arr > max]

                processed.append(sum(processed_point)/len(processed_point))
                print(processed[i])
                # i += 1

    base_count = 0
    base = 0
    for i in range(0, BASE_POINTS):
        base += processed[i]

    base = base/BASE_POINTS

    # rolloing bandpass filter
    from gcode_gen import beam_size
    from gcode_gen import x_grid
    smallest_feature = 4  # smallest part feature size in mm
    points = int((beam_size/x_grid)*smallest_feature)

    # for i in range(0, len(processed)-points):




    with open(POINTS_FILE, 'r') as f:
        all_txt = f.read()

        final_points = ''
        points = all_txt.split('\n')
        for i, point in enumerate(points):
            if i < len(processed):
                final_points += point + "," + str(base - processed[i]) + '\n'

    with open(FINAL_FILE, 'w') as f:
        f.write(final_points)


if __name__ == "__main__":
    process()