import struct
import gzip

# 映射特征 ID 到名称的字典
feature_id_to_name = {
    0: "_neutral",
    1: "browDownLeft",
    2: "browDownRight",
    3: "browInnerUp",
    4: "browOuterUpLeft",
    5: "browOuterUpRight",
    6: "cheekPuff",
    7: "cheekSquintLeft",
    8: "cheekSquintRight",
    9: "eyeBlinkLeft",
    10: "eyeBlinkRight",
    11: "eyeLookDownLeft",
    12: "eyeLookDownRight",
    13: "eyeLookInLeft",
    14: "eyeLookInRight",
    15: "eyeLookOutLeft",
    16: "eyeLookOutRight",
    17: "eyeLookUpLeft",
    18: "eyeLookUpRight",
    19: "eyeSquintLeft",
    20: "eyeSquintRight",
    21: "eyeWideLeft",
    22: "eyeWideRight",
    23: "jawForward",
    24: "jawLeft",
    25: "jawOpen",
    26: "jawRight",
    27: "mouthClose",
    28: "mouthDimpleLeft",
    29: "mouthDimpleRight",
    30: "mouthFrownLeft",
    31: "mouthFrownRight",
    32: "mouthFunnel",
    33: "mouthLeft",
    34: "mouthLowerDownLeft",
    35: "mouthLowerDownRight",
    36: "mouthPressLeft",
    37: "mouthPressRight",
    38: "mouthPucker",
    39: "mouthRight",
    40: "mouthRollLower",
    41: "mouthRollUpper",
    42: "mouthShrugLower",
    43: "mouthShrugUpper",
    44: "mouthSmileLeft",
    45: "mouthSmileRight",
    46: "mouthStretchLeft",
    47: "mouthStretchRight",
    48: "mouthUpperUpLeft",
    49: "mouthUpperUpRight",
    50: "noseSneerLeft",
    51: "noseSneerRight",
}


class BinaryResultReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_stroke_data_(self):
        '''
        读取手写笔记录的二进制文件数据
        '''
        with open(self.file_path, "rb") as file:
            compressed_data = file.read()

        # 解压缩数据
        decompressed_data = gzip.decompress(compressed_data)

        # 计算每条数据的长度
        data_size = struct.calcsize("iiiq")

        # 解析所有数据
        num_data = len(decompressed_data) // data_size
        data_list = []

        for i in range(num_data):
            data_bytes = decompressed_data[i * data_size : (i + 1) * data_size]

            # 使用 struct.unpack 解析每条数据, 字节序是 Big Endian!
            data = struct.unpack(">iiiq", data_bytes)

            # 构造每条数据的字典
            data_dict = {
                "x": data[0],
                "y": data[1],
                "pressure": data[2],
                "timestamp": data[3]
            }

            data_list.append(data_dict)

        return data_list

    def read_face_blendshapes_result(self):
        with open(self.file_path, "rb") as file:
            compressed_data = file.read()

        # 解压缩数据
        decompressed_data = gzip.decompress(compressed_data)
        # decompressed_data = compressed_data

        # 计算每次识别结果的数据长度
        result_size = struct.calcsize("Q" + "I f" * 52)

        # 解析所有识别结果
        num_results = len(decompressed_data) // result_size
        results = []

        for i in range(num_results):
            result_data = decompressed_data[i * result_size : (i + 1) * result_size]

            # 使用 struct.unpack 解析每次识别结果的数据, 字节序是 Big Endian!
            result = struct.unpack(">Q" + "I f" * 52, result_data)

            # 构造每次识别结果的字典
            result_dict = {
                "timestamp": result[0],
                "blendshapes": {
                    result[j]: result[j + 1] for j in range(1, len(result), 2)
                },
                "blendshape_names": {
                    feature_id: feature_id_to_name.get(
                        feature_id, f"UnknownFeature-{feature_id}"
                    )
                    for feature_id in result[1::2]
                },
            }

            results.append(result_dict)

        return results
