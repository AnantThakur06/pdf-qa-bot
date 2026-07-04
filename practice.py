import time
import torch
from sentence_transformers import util

# Warm-up call (throwaway) so the first real measurement is fair
_ = util.cos_sim(torch.rand(1, 384), torch.rand(10, 384))

for num_chunks in [1000, 50000, 200000, 1000000]:
    fake_chunks = torch.rand(num_chunks, 384)
    fake_question = torch.rand(1, 384)

    start = time.time()
    scores = util.cos_sim(fake_question, fake_chunks)[0]
    best = scores.argmax()
    end = time.time()

    print(f"{num_chunks:>8} chunks  ->  {(end - start) * 1000:.2f} ms")