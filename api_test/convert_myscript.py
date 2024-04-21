import json

# 读取 collected_data.txt 文件
with open('collected_data.txt', 'r') as f:
    data = [json.loads(line) for line in f]

# 初始化变量
strokes = []
stroke_x = []
stroke_y = []
stroke_t = []
stroke_p = []

# 遍历数据
for point in data:
    if point['pressure'] > 0:
        # 如果 pressure > 0，添加坐标到当前笔画
        stroke_x.append(point['x'])
        stroke_y.append(point['y'])
        stroke_t.append(point['timestamp'])
        stroke_p.append(point['pressure'])
    elif stroke_x and stroke_y:
        # 如果 pressure = 0 并且当前笔画不为空，结束当前笔画并开始一个新的笔画
        strokes.append({
            "x": stroke_x,
            "y": stroke_y,
            "t": stroke_t,
            "p": stroke_p,
            "pointerType": "PEN",
            "pointerId": 0
        })
        stroke_x = []
        stroke_y = []
        stroke_t = []
        stroke_p = []

# 添加最后一个笔画
if stroke_x and stroke_y:
    strokes.append({
        "x": stroke_x,
        "y": stroke_y,
        "t": stroke_t,
        "p": stroke_p,
        "pointerType": "PEN, TOUCH, ERASER",
        "pointerId": 0
    })

output_json = {
    "width": 25000,
    "height": 20000,
    "contentType": "Text",
    "conversionState": "DIGITAL_EDIT",
    "theme": "ink {color: #000000; -myscript-pen-width: 1; -myscript-pen-fill-style: none; -myscript-pen-fill-color: #FFFFFF00;} mycolor {color: #120f51;} .math { font-family: STIXGeneral;} .math-solved {font-family: STIXGeneral; color: #A8A8A8FF;} .text {font-family: Open Sans; font-size: 10;}",
    "strokeGroups": [
        {
            "strokes": strokes,
            "penStyle": "color: #120f51;↵-myscript-pen-width: 2;",
            "penStyleClasses": "ink mycolor"
        }
    ],
    "configuration": {
        "alwaysConnected": True,
        "lang": "en_US",
        "math": {
            "solver": {
                "enable": True,
                "fractional-part-digits": 3,
                "decimal-separator": ".",
                "rounding-mode": "half up",
                "angle-unit": "deg",
                "fraction-mode": "decimal",
                "options": "algebraic"
            },
            "margin": {
                "top": 10,
                "left": 15,
                "right": 15,
                "bottom": 10
            },
            "undo-redo": {
                "mode": "stroke"
            },
            "session-time": 750,
            "eraser": {
                "erase-precisely": False
            },
            "recognition-timeout": 30
        },
        "text": {
            "margin": {
                "top": 10,
                "left": 15,
                "right": 15,
                "bottom": 10
            },
            "guides": {
                "enable": True
            },
            "configuration": {
                "customResources": [
                ],
                "customLexicon": [
                    "word1",
                    "word2"
                ],
                "addLKText": True
            },
            "eraser": {
                "erase-precisely": False
            }
        },
        "export": {
            "image": {
                "guides": True,
                "viewport": {
                    "x": 0,
                    "y": 0,
                    "width": 0,
                    "height": 0
                }
            },
            "jiix": {
                "strokes": True,
                "style": False,
                "bounding-box": False,
                "text": {
                    "chars": False,
                    "words": True
                }
            },
            "mathml": {
                "flavor": "standard"
            },
            "image-resolution": 300
        },
        "diagram": {
            "text": {
                "customResources": [
                ],
                "customLexicon": [
                    "word1",
                    "word2"
                ],
                "addLKText": True
            },
            "convert": {
                "edge": True,
                "node": True,
                "text": True,
                "matchTextSize": True
            },
            "sessiontime": 750,
            "enable-sub-blocks": True,
            "eraser": {
                "erase-precisely": False
            }
        },
        "gesture": {
            "enable": True,
            "disabled-gestures": [
            ],
            "underlines": {
                "behavior": "string"
            }
        },
        "raw-content": {
            "recognition": {
                "text": True,
                "shape": True
            },
            "text": {
                "customResources": [
                ],
                "customLexicon": [
                    "word1",
                    "word2"
                ],
                "addLKText": True
            },
            "sessiontime": 750,
            "eraser": {
                "erase-precisely": False
            }
        },
        "stroke-max-point-count": 3000
    },
    "xDPI": 96,
    "yDPI": 96
}


with open('coordinates_myscript.json', 'w') as f:
    json.dump(output_json, f, indent=4)