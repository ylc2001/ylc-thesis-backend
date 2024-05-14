from pathlib import Path
import json
import re

cur_dir = Path(__file__).parent
result_folder = "results"
problem_file = "0506_problem.txt"

with open(cur_dir / 'prompts/substitute_text' / problem_file, 'r') as file:
    content = file.read()
    blocks = re.split(r'%\w+%', content)
    std_graph_text = blocks[-1]
    std_graph_json = json.loads(std_graph_text)

mistake_list = []
# knowledge set
related_knowledge = set()

for input_file in (cur_dir / result_folder).glob('*.json'):
    with open(input_file, 'r') as file:
        result_json = json.load(file)

    output_filename = input_file.stem + "_output.md"
    with open(cur_dir / result_folder / output_filename, 'w') as output_file:
        print("### Step 1, 每一步的正确性\n", file=output_file)
        correct_node_list = []
        for node in result_json:
            if 'correctness' in node:
                if node['correctness'] == 'correct':
                    print(f"[{node['id']}] 正确 v", file=output_file)
                    correct_node_list.append(node['id'])
                elif node['correctness'] == 'unknown':
                    print(f"[{node['id']}] 步骤缺失 x", file=output_file)
                else:
                    print(f"[{node['id']}] ERROR: value of key 'correctness' is invalid: {node['correctness']}", file=output_file)
            elif 'result_correctness' in node:
                if node['result_correctness'] == True or node['result_correctness'] == "true" or node['result_correctness'] == "True":
                    print(f"[{node['id']}] 正确 v", file=output_file)
                    correct_node_list.append(node['id'])
                elif node['result_correctness'] == False or node['result_correctness'] == "false" or node['result_correctness'] == "False":
                    print(f"[{node['id']}] 错误 x", file=output_file)
                else:
                    print(f"[{node['id']}] ERROR: value of key 'result_correctness' is invalid: {node['result_correctness']}", file=output_file)
        print("\n**正确的步骤:** ", correct_node_list, file=output_file)
        print(f"**正确的步骤数: {len(correct_node_list)}**", file=output_file)
        print(f"**总步骤数: {len(result_json)}**", file=output_file)
        print(f"**正确率: {len(correct_node_list) / len(result_json) * 100:.2f}%**", file=output_file)

        print("\n### Step 2, 分析根本错误点", file=output_file)
        for node in result_json:
            if 'correctness' in node:
                if node['correctness'] == 'unknown':
                    mistake_list.append(node['id'])
                    print(f"\n[{node['id']}] 是一处根本错误\n", file=output_file)
                    print(f"正确结果: {node['content']}", file=output_file)
                    print(f"学生结果: 步骤缺失", file=output_file)
                    print(f"错因分析: {node['analysis']}", file=output_file)
            if 'reasoning_correctness' in node and 'result_correctness' in node:
                if node['reasoning_correctness'] == False or node['reasoning_correctness'] == "false" or node['reasoning_correctness'] == "False":
                    if node['result_correctness'] == False or node['result_correctness'] == "false" or node['result_correctness'] == "False":
                        mistake_list.append(node['id'])
                        print(f"\n[{node['id']}] 是一处根本错误\n", file=output_file)
                        print(f"正确结果: {node['content']}", file=output_file)
                        print(f"学生结果: {node['student_result']}", file=output_file)
                        print(f"错因分析: {node['analysis']}", file=output_file)

        print("\n### Step 3, 学生没有掌握的知识点", file=output_file)
        for node in result_json:
            if node['id'] in mistake_list:
                related_knowledge.update(node['dependency'])
        for knowledge_id in related_knowledge:
            for node in std_graph_json['nodes']:
                if node['id'] == knowledge_id and 'from' in node and node['from'] == "knowledge":
                    print(f"[{knowledge_id}] {node['content']}", file=output_file)