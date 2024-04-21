import json
import os
from pyvis.network import Network

# 说明：设置好输入 json 文件和输出的 html 文件名称

file_name = "example.json"
dir_name = "prompts"
file_path = os.path.join(os.getcwd(), dir_name, file_name)
output_name = "visualization_example.html"

# 读取并解析json文件
with open(file_path, 'r') as file:
    data = json.load(file)


net = Network(height='1000px', width='95%', directed=True)

# 格式、样式规定
for item in data['known']:
    if item['type'] == '[intent]': 
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='ellipse',
            color='#FAF3DD',
            )
    elif item['type'] == '[assert]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            color='#FAF3DD',
            )
    elif item['type'] == '[fact]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            color='#FAF3DD',
            )
    elif item['type'] == '[knowledge]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            color='red',
            )

for item in data['solution']:
    if item['type'] == '[intent]': 
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='ellipse',
            color='#F5F5F5',
            )
    elif item['type'] == '[assert]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            color='#F5F5F5',
            )
    elif item['type'] == '[fact]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            color='#D0D0D0',
            )
    elif item['type'] == '[knowledge]':
        net.add_node(
            item['id'], 
            label=f"[{item['id']}]{item['content']}",
            shape='box',
            )

# 遍历解决方案中的每个元素，如果类型不是'reference'，则遍历其依赖项，并添加边
for item in data['solution']:
    if item['type'] != '[reference]':
        for dependency in item.get('dependency', []):
            net.add_edge(dependency, item['id'])

net.show_buttons(filter_=['physics'])
net.show(output_name, notebook=False)