import json
import re
from llama_cpp import Llama

# Step 1: Your placeholder tool
def get_temperature(location: str):
    print(f"[TOOL CALLED] get_temperature")
    print(f"City: {location}")
    return "22.0"  # Simulated temperature

# Step 2: Load your model
meta_llama_3p1_8b_it_q4_k_m = Llama(
    model_path='../models/llama-3.1-8b-it-q4-k-m/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf',
    n_gpu_layers=20,
    n_ctx=4096,
    use_mlock=True,
    use_mmap=True,
    verbose=True
)

# Step 3: Tool schema to inject manually into the prompt
tool_schema = """
You have access to the following tool:

get_temperature(location: str) -> float
- Description: Get the current temperature at a location.
- Arguments:
    - location (str): The location to get the temperature for, in the format "City, Country".

Respond with a JSON object like this:
{
  "tool_calls": [
    {
      "name": "get_temperature",
      "arguments": {
        "location": "Paris, France"
      }
    }
  ]
}
"""

# Step 4: Final prompt to pass to the model
prompt = f"""<s>[INST] {tool_schema}

What is the temperature in Paris right now? [/INST]"""

# Step 5: Call the model
response = meta_llama_3p1_8b_it_q4_k_m(prompt, max_tokens=256, stop=["/INST"])
output_text = response["choices"][0]["text"]
print("\n[MODEL OUTPUT]:\n", output_text)

def extract_first_json_block(text: str):
    brace_stack = []
    json_start = None

    for i, char in enumerate(text):
        if char == '{':
            if not brace_stack:
                json_start = i
            brace_stack.append('{')
        elif char == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack:
                     json_end = i + 1
                     return text[json_start:json_end]
    return None

json_text = extract_first_json_block(output_text)

if json_text:
    try:
        tool_json = json.loads(json_text)
        for tool_call in tool_json["tool_calls"]:
            if tool_call["name"] == "get_temperature":
                location = tool_call["arguments"]["location"]
                result = get_temperature(location)
                print(f"[TOOL RESULT]: {result}")
    except json.JSONDecodeError:
        print("[ERROR] Could not parse tool call JSON.")

else:
    print("[INFO] No valid JSON object found in model output.")

'''
# Step 6: Extract tool call from model output
match = re.search(r'\{.*"tool_calls".*?\}', output_text, re.DOTALL)
if match:
    try:
        tool_json = json.loads(match.group())
        for tool_call in tool_json["tool_calls"]:
            if tool_call["name"] == "get_temperature":
                location = tool_call["arguments"]["location"]
                result = get_temperature(location)
                print(f"[TOOL RESULT]: {result}")
    except json.JSONDecodeError:
        print("[ERROR] Could not parse tool call JSON.")
else:
    print("[INFO] No tool call detected in output.")
'''
