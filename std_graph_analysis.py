from pathlib import Path

from handyllm import hprompt

from handyllm import OpenAIClient
from handyllm import PromptConverter, stream_chat
import os
import json
import yaml
import textwrap
import time
import copy
import re

cur_dir = Path(__file__).parent
input_folder = "input_data_yaml"
input_filename = "1ZhuAoxing"
prompt1_file = "check_node_correctness.hprompt"
prompt2_file = "check_node_errors.hprompt"
problem_file = "0506_problem.txt"

# 学生的笔迹和 think aloud
input_path = os.path.join(os.getcwd(), input_folder, input_filename+".yaml")
with open(input_path, 'r', encoding='utf-8') as file:
	student_input_data = yaml.safe_load(file)

print(">>> Parameters <<<")
print(f"input_dir: {input_folder}/{input_filename}.yaml")

with open(cur_dir / 'prompts/substitute_text' / problem_file, 'r', encoding='utf-8') as file:
    content = file.read()
    blocks = re.split(r'%\w+%', content)
    std_graph_text = blocks[-1]
    std_graph_json = json.loads(std_graph_text)

# load hprompt
prompt1: hprompt.ChatPrompt = hprompt.load_from(cur_dir / 'prompts' / prompt1_file)
prompt2: hprompt.ChatPrompt = hprompt.load_from(cur_dir / 'prompts' / prompt2_file)
# print(prompt.data)
# print(prompt)
# print(repr(prompt))


prompt1.chat[-1]["content"] = prompt1.chat[-1]["content"].replace("%audio_text%", student_input_data["audio_text"])
prompt1.chat[-1]["content"] = prompt1.chat[-1]["content"].replace("%written_text%", student_input_data["written_text"])
result_list = []
for item in std_graph_json['nodes']:
	if item['id'] < 1000 and item['id'] > 0:
		prompt1_copy = copy.deepcopy(prompt1)
		print(f">>> 1 节点 {item['id']} 判断 & 分析 <<<")
		print("---------------------------------------")
		prompt1_copy.chat[-1]["content"] = prompt1_copy.chat[-1]["content"].replace("%node_id%", f"{item['id']}")
		prompt1_copy.chat[-1]["content"] = prompt1_copy.chat[-1]["content"].replace("%node_content%", f"{item['content']}")

		result_prompt = prompt1_copy.run()
		result_prompt.chat[-1]["content"] = result_prompt.chat[-1]["content"].replace("```json", f"")
		result_prompt.chat[-1]["content"] = result_prompt.chat[-1]["content"].replace("```", f"")
		print(result_prompt.result_str)
		try:
			result_list.append(json.loads(result_prompt.result_str))
		except Exception as e:
			print(e)
			print("Error in json.loads")
			result_list.append(result_prompt.result_str)

updated_result_list = copy.deepcopy(result_list)

# current_time_str = time.strftime("%m%d_%H%M%S", time.localtime())
# with open(os.path.join(os.getcwd(), "results", current_time_str + "_" + input_filename+"_result1.json"), 'w') as file:
# 	json.dump(result_list, file, ensure_ascii=False, indent=4)
# 	print(f"Saved result to result1.json")

prompt2.chat[-1]["content"] = prompt2.chat[-1]["content"].replace("%student_graph%", json.dumps(result_list, ensure_ascii=False, indent=4))
for i, item in enumerate(result_list):
	if item['correctness'] == "incorrect":
		prompt2_copy = copy.deepcopy(prompt2)
		print(f">>> 2 节点 {item['id']} 错误检查 <<<")
		print("---------------------------------------")

		prompt2_copy.chat[-1]["content"] = prompt2_copy.chat[-1]["content"].replace("%node_id%", f"{item['id']}")
		dependency_str = "["
		for dep in item['dependency']:
			try:
				for node in result_list:
					if node['id'] == dep and node['id'] < 1000:
						dependency_str += "{"
						dependency_str += f"id: {dep}, student_result: {node['student_result']}, "
						dependency_str += f"correctness: {node['correctness']}, "
						dependency_str += "}, "
						break
				for node in std_graph_json['nodes']:
					if node['id'] == dep and node['id'] > 1000:
						dependency_str += "{"
						dependency_str += f"id: {dep}, from: {node['from']}, content: {node['content']}, "
						dependency_str += "}, "
						break
			except Exception as e:
				print(e)
				print(f"Error in dependency_str, dep: {dep}")
		dependency_str += "]"
		prompt2_copy.chat[-1]["content"] = prompt2_copy.chat[-1]["content"].replace("%node_dependency%", dependency_str)


		result_prompt = prompt2_copy.run()
		result_prompt.chat[-1]["content"] = result_prompt.chat[-1]["content"].replace("```json", f"")
		result_prompt.chat[-1]["content"] = result_prompt.chat[-1]["content"].replace("```", f"")
		print(result_prompt.result_str)
		try: 
			updated_result = json.loads(result_prompt.result_str)
			updated_result_list[i] = updated_result
		except Exception as e:
			print(e)
			print("Error in json.loads")
			updated_result_list[i] = result_prompt.result_str

		


# save reuslt list
current_time_str = time.strftime("%m%d_%H%M%S", time.localtime())
save_filename = current_time_str + "_" + input_filename+"_result.json"
with open(os.path.join(os.getcwd(), "results", save_filename), 'w', encoding='utf-8') as file:
	json.dump(updated_result_list, file, ensure_ascii=False, indent=4)
	print(f"Saved result to {save_filename}")


# # chain result hprompt
# prompt += result_prompt
# # chain another hprompt
# prompt += hprompt.load_from(cur_dir / './assets/magic.hprompt')
# # run again
# result2 = prompt.run()