# use eventlet for concurrency
import eventlet
eventlet.monkey_patch()

import os
import sys
from flask import Flask, send_file, request
import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from loguru import logger

# default output to stderr; only change the format here
# ref: https://github.com/Delgan/loguru/issues/109#issuecomment-507814421
fmt = "[<green>{time:YYYY-MM-DD HH:mm:ss.SSS ZZ}</green>] [{process}] [<level>{level}</level>] <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
logger.configure(handlers=[{"sink": sys.stderr, "format": fmt}])

# load env parameters form file named .env
load_dotenv(find_dotenv())
# server settings
HOST = os.getenv("HOST", '')
PORT = int(os.getenv("PORT"))

app = Flask(__name__)

@app.route('/upload_record', methods=['POST'])
def upload_file():
    """
    接收用户发来的文件，每一个用户对应一个文件夹存储
    存储位置为: ./upload_files/{name}/{date}/{file}
    """
    if 'files[]' not in request.files:
        print('No file part in the request')
        return 'No file part in the request', 400
    files = request.files.getlist('files[]')
    name = request.form.get('name', default='nobody')
    print(f"File received from {name}")
    day_str = datetime.now().strftime('%Y-%m-%d')
    save_dir = os.path.join('./upload_files', name, day_str)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    for file in files:
        if file.filename == '' or not file:
            print('No selected file')
            return "No selected file", 400
        file.save(os.path.join(save_dir, file.filename))
        print(f'File [{file.filename}] saved successfully')

    return "Files successfully uploaded", 200
    
@app.route('/get_image_list', methods=['GET'])
def get_image_list():
    # 获取本地图片列表
    image_list = os.listdir('./images')
    image_list = [image.split('.')[0] for image in image_list]
    image_list.sort()
    return image_list

@app.route('/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
    # 定义可能的图片格式
    extensions = ['png', 'jpg', 'jpeg', 'gif']
    image_path = None
    for ext in extensions:
        temp_path = os.path.join('./images', f'{image_id}.{ext}')
        if os.path.exists(temp_path):
            image_path = temp_path
            break
    if not image_path:
        return 'Image not found', 404
    return send_file(image_path, mimetype='image/jpeg')

@app.route('/', methods=['GET'])
def ping_pong():
    name = request.args.get('name', default='nobody')
    logger.info(f"Ping received from {name}")
    return 'pong', 200

if __name__ == '__main__':
    # app.run(host=HOST, port=PORT, debug=True)
    logger.info(f"Starting eventlet server at {HOST}:{PORT}")
    logger.warning(f"For production, use gunicorn instead.")
    from eventlet import wsgi
    wsgi.server(eventlet.listen((HOST, PORT)), app)
