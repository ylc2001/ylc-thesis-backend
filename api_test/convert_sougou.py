import json
import os

dir_path = './test_data/'

for root, dirs, files in os.walk(dir_path):
    for file in files:
        # 检查文件是否为txt文件
        if file.endswith('.txt'):
            # 获取文件的完整路径
            file_path = os.path.join(root, file)
            # get file name (without extension)
            file_name = file.split('.')[0]

            # 读取 xxx.txt 文件
            with open(file_path, 'r') as f:
                data = [json.loads(line) for line in f]

            # 1、手写轨迹点坐标，按 x1, y1, x2, y2 ... xn, yn 来排列
            # 2、笔划结束时需要在笔划轨迹点后面补充坐标 （-1, 0）
            # 3、本次手写完全结束时需要在末尾补充坐标 （-1, -1）
                
            track_points = []
            stroke_x = []
            stroke_y = []

            skip = True

            for point in data:
                if skip:
                    skip = False
                    continue
                if point['pressure'] > 0:
                    # 如果 pressure > 0，添加坐标到当前笔画
                    track_points.append(point['y'])
                    track_points.append(29000 - point['x'])
                    stroke_x.append(point['y'])
                    stroke_y.append(29000 - point['x'])
                elif stroke_x and stroke_y:
                    # 如果 pressure = 0 并且当前笔画不为空，结束当前笔画并开始一个新的笔画
                    track_points.append(-1)
                    track_points.append(0)
                    stroke_x = []
                    stroke_y = []
                
            # 添加最后一个笔画
            if stroke_x and stroke_y:
                track_points.append(-1)
                track_points.append(0)
            track_points.append(-1)
            track_points.append(-1)

            output_json = {
                "num": 3,
                "track_points": ",".join(map(str, track_points))
            }
            with open(f'{dir_path}{file_name}_sougou.json', 'w') as f:
                json.dump(output_json, f, indent=4)
                print(f'File {file_name}_sougou.json saved!')