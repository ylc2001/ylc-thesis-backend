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
prompt1_file = "merge1.hprompt"

# load hprompt
prompt1: hprompt.ChatPrompt = hprompt.load_from(cur_dir / 'prompts' / prompt1_file)

student_graph_str = """
{
    "known": [
        { "id": 1001, "from":"given", "content": "$f(x) = ax^2 + b \\\\ln x$"},
        { "id": 1002, "from":"given", "content": "f(x) 在 x=1 处有极值 1/2"},
        { "id": 1003, "from":"knowledge", "content": "ln x 的定义域是 (0, +\\\\infin)"},
        { "id": 1004, "from":"knowledge", "content": "函数极值的概念"},
        { "id": 1005, "from":"knowledge", "content": "初等函数的导数公式"},
        { "id": 1006, "from":"knowledge", "content": "导数与函数单调性的关系"},
        { "id": 1007, "from":"knowledge", "content": "对数函数的计算"}
    ],
    "nodes": [
        { "id": 1, "content": "f'(x)=2ax + \\\\frac{b}{x}", "student_thoughts": "根据导数的计算法则求得 f(x) 的导数", "dependency": [1001, 1005]},
        { "id": 2, "content": "f'(1)=2a+b=\\\\frac{1}{2}", "student_thoughts": "将 x=1 代入 f'(x) 得到方程", "dependency": [1, 1002]},
        { "id": 3, "content": "f(1)=a+b=0", "student_thoughts": "由于 f(x) 在 x=1 处有极值，根据极值的定义，将 x=1 代入 f(x) 得到方程", "dependency": [1001, 1002, 1004]},
        { "id": 4, "content": "a=\\\\frac{1}{2}, b=-\\\\frac{1}{2}", "student_thoughts": "联立方程 2a+b=\\\\frac{1}{2} 和 a+b=0 求解得到 a 和 b 的值", "dependency": [2, 3]},
        { "id": 5, "content": "f(x)=\\\\frac{1}{2}x^2-\\\\frac{1}{2}\\\\ln x", "student_thoughts": "将求得的 a 和 b 的值代入原函数", "dependency": [4, 1001]},
        { "id": 6, "content": "f'(x)=x-\\\\frac{1}{2x}", "student_thoughts": "将求得的 a 和 b 的值代入导数公式", "dependency": [4, 1]},
        { "id": 7, "content": "x=\\\\pm\\\\frac{\\\\sqrt{2}}{2}", "student_thoughts": "令导数 f'(x) 等于 0 求得 x 的值", "dependency": [6]},
        { "id": 8, "content": "(-\\\\infty, -\\\\frac{\\\\sqrt{2}}{2}) 和 (\\\\frac{\\\\sqrt{2}}{2}, +\\\\infty) 上 f(x) 单调递增", "student_thoughts": "根据导数的正负判断函数的单调性", "dependency": [6, 7, 1006]},
        { "id": 9, "content": "(-\\\\frac{\\\\sqrt{2}}{2}, \\\\frac{\\\\sqrt{2}}{2}) 上 f(x) 单调递减", "student_thoughts": "根据导数的正负判断函数的单调性", "dependency": [6, 7, 1006]},
        { "id": 10, "content": "f'(-\\\\frac{\\\\sqrt{2}}{2})=0, f'(\\\\frac{\\\\sqrt{2}}{2})=0", "student_thoughts": "将 x=\\\\pm\\\\frac{\\\\sqrt{2}}{2} 代入导数公式得到极值点", "dependency": [6, 7]},
        { "id": 11, "content": "f(-\\\\frac{\\\\sqrt{2}}{2}) 和 f(\\\\frac{\\\\sqrt{2}}{2}) 是极值", "student_thoughts": "将极值点代入原函数求得极值", "dependency": [5, 10]}
    ]
}
"""
student_graph_json = json.loads(student_graph_str)

prompt1.chat[-1]["content"] = prompt1.chat[-1]["content"].replace("%student_graph%", student_graph_str)

result_list = []
for item in student_graph_json['nodes']:
	# if item['id'] == 6:
	prompt1_copy = copy.deepcopy(prompt1)
	print(f">>> 学生图节点 {item['id']} 判断 & 分析 <<<")
	print("---------------------------------------")
	prompt1_copy.chat[-1]["content"] = prompt1_copy.chat[-1]["content"].replace("%node_id%", f"{item['id']}")
	prompt1_copy.chat[-1]["content"] = prompt1_copy.chat[-1]["content"].replace("%node_content%", f"{item['content']}")
	dependency_str = ""
	for dep in item['dependency']:
		try:
			if dep < 1000:
				dependency_str += f"[id: {dep}, content: {student_graph_json['nodes'][dep-1]['content']}], "
			else:
				dependency_str += f"[id: {dep}, content: {student_graph_json['known'][dep-1001]['content']}], "
		except Exception as e:
			print(e)
			print(f"Error in dependency_str, dep: {dep}")
	prompt1_copy.chat[-1]["content"] = prompt1_copy.chat[-1]["content"].replace("%dependency%", f"{dependency_str}")
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

# save reuslt list
current_time_str = time.strftime("%H%M%S", time.localtime())
with open(os.path.join(os.getcwd(), "results", current_time_str + "_" + "ZXH_result.json"), 'w') as file:
	json.dump(result_list, file, ensure_ascii=False, indent=4)
	print(f"Saved result to json")


# # chain result hprompt
# prompt += result_prompt
# # chain another hprompt
# prompt += hprompt.load_from(cur_dir / './assets/magic.hprompt')
# # run again
# result2 = prompt.run()