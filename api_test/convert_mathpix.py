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

            # 初始化变量
            strokes_x = []
            strokes_y = []
            stroke_x = []
            stroke_y = []

            # 遍历数据
            for point in data:
                if point['pressure'] > 0:
                    # 如果 pressure > 0，添加坐标到当前笔画
                    stroke_x.append(point['y'])
                    stroke_y.append(29000 - point['x'])
                elif stroke_x and stroke_y:
                    # 如果 pressure = 0 并且当前笔画不为空，结束当前笔画并开始一个新的笔画
                    strokes_x.append(stroke_x)
                    strokes_y.append(stroke_y)
                    stroke_x = []
                    stroke_y = []

            # 添加最后一个笔画
            if stroke_x and stroke_y:
                strokes_x.append(stroke_x)
                strokes_y.append(stroke_y)

            # 写入 xxx_mathpix.json 文件
            with open(f'{dir_path}{file_name}_mathpix.json', 'w') as f:
                json.dump({"strokes": {"x": strokes_x, "y": strokes_y}}, f)
                print(f'File {file_name}_mathpix.json saved!')
