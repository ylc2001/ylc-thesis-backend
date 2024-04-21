import json
import os
from pyvis.network import Network

# 说明：设置好输入 json 文件和输出的 html 文件名称

file_name = "computation_graph.json"
file_path = os.path.join(os.getcwd(), file_name)
output_name = "计算图.html"

# 读取并解析json文件
with open(file_path, 'r') as file:
    data = json.load(file)
print(json.dumps(data, indent=4, ensure_ascii=False))

net = Network(height='1000px', width='95%', directed=True)
for item in data['nodes']:
    if item['type'] == 'Question': 
        net.add_node(
            item['id'],
            label=f"[{item['id']}]  {item['content']}",
            shape='box',
        )
    elif item['type'] == 'AND': 
        net.add_node(
            item['id'],
            label=f"[{item['id']}]  {item['content']}",
            shape='box',
            color='#FAF3DD',
        )
    elif item['type'] == 'OR':
        net.add_node(
            item['id'],
            label=f"[{item['id']}]  {item['content']}",
            shape='box',
            color='#FAF3DD',
        )
    elif item['type'] == 'End':
        net.add_node(
            item['id'],
            label=f"[{item['id']}]  {item['content']}",
            shape='box',
            color='red',
        )

for item in data['nodes']:
    for dependency in item.get('dependency', []):
        net.add_edge(dependency, item['id'])

net.show_buttons(filter_=['physics'])
net.show(output_name, notebook=False)