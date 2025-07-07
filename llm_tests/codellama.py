from llama_cpp import Llama

meta_codellama_7b_it_q4_k_m = Llama(
    model_path='../models/codellama-7b-instruct-q4-k-m/codellama-7b-instruct.Q4_K_M.gguf',
    n_gpu_layers=20, n_ctx=4096, use_mlock=True, use_mmap=True, verbose=True
)

prompt = """<s>[INST] Write python code to solve the following coding problem that obeys the constraints and passes the example test cases. Please wrap your code answer using ```
Given an integer array nums, return the length of the longest strictly increasing subsequence.

Example 1:

Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
Example 2:

Input: nums = [0,1,0,3,2,3]
Output: 4
Example 3:

Input: nums = [7,7,7,7,7,7,7]
Output: 1
 

Constraints:

1 <= nums.length <= 2500
-10^4 <= nums[i] <= 10^4
[/INST]"""

output = meta_codellama_7b_it_q4_k_m(prompt, max_tokens=256, echo=True)

print(output["choices"][0])
