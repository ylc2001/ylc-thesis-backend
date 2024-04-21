# classroom-observer-backend
智能课堂感知 后端部分



## 环境配置

```sh
# 创建虚拟环境
python -m venv .venv
# 开启虚拟环境
. .venv/bin/activate
# 安装依赖
pip install -r requirements.txt
# 复制.env并配置服务器设置
cp .env.template .env
```



## 运行服务

不要直接运行脚本`app.py`，而是通过如下方式启动后台服务和日志记录：

```sh
# 通过gunicorn启动后台服务，同时启动log rotation（内部配置日志切换大小）
./start_server.sh

# 检查 server 和 log rotation 运行状态
./status_server.sh

# 停止后台服务
./stop_server.sh
```


## Myscript api 测试流程

先运行 `convert_myscript.py`, 把 pad 上笔的数据（xxx.txt）转换成 json 格式，得到 `coordinates_myscript.json`，然后运行 `myscript_api.py`

`coordinates_myscript.json` 一些可以手动改的参数：
比较靠前的 `"contentType": "Math"`, 这里一共可以有这四种: Text, Diagram, Math, Raw Content
最后的 `"stroke-max-point-count": 3000`，别太小，不然笔画超过这个数会报错

其他的参考链接：

https://developer.myscript.com/docs/interactive-ink/2.3/web/rest/architecture/#stroke

https://swaggerui.myscript.com/#/Batch%20mode/batch