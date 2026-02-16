import os
import time
from random import randint, seed
from nanovllm import LLM, SamplingParams
# from vllm import LLM, SamplingParams
# 基准的性能测试脚本，用于测试 nano-vllm 的吞吐量。

def main():
    # 1. 初始化配置
    seed(0)
    num_seqs = 256                  # 并发序列数
    max_input_len = 1024            # 最大输入长度
    max_ouput_len = 1024            # 最大输出长度

    path = os.path.expanduser("~/huggingface/Qwen3-0.6B/")          # 模型权重路径
    # 2. 创建 LLM 引擎
    llm = LLM(path, enforce_eager=False, max_model_len=4096)

    # 3. 生成随机测试数据
    # 随机生成256个序列，每个序列100-1024个随机token
    prompt_token_ids = [[randint(0, 10000) for _ in range(randint(100, max_input_len))] for _ in range(num_seqs)]
    sampling_params = [SamplingParams(temperature=0.6, ignore_eos=True, max_tokens=randint(100, max_ouput_len)) for _ in range(num_seqs)]
    # uncomment the following line for vllm
    # prompt_token_ids = [dict(prompt_token_ids=p) for p in prompt_token_ids]

    # 4. Warmup预热-第一次调用用于编译和初始化
    llm.generate(["Benchmark: "], SamplingParams())
    t = time.time()
    # 正式进行性能测试
    llm.generate(prompt_token_ids, sampling_params, use_tqdm=False)
    t = (time.time() - t)
    total_tokens = sum(sp.max_tokens for sp in sampling_params)
    # 计算吞吐量，每秒token数
    throughput = total_tokens / t
    print(f"Total: {total_tokens}tok, Time: {t:.2f}s, Throughput: {throughput:.2f}tok/s")


if __name__ == "__main__":
    main()
