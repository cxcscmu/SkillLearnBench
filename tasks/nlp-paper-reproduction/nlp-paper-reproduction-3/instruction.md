# Final Exam: Natural Language Processing Code Reproduction
Direct Preference Optimization (DPO) is a widely used offline preference optimization algorithm that reparameterizes reward functions in reinforcement learning from human feedback (RLHF), improving both simplicity and training stability. Building on this approach, SimPO is a simpler yet more effective method. Its effectiveness stems from a key design choice: using the average log probability of a sequence as the implicit reward.

In this exam, you will reproduce part of the implementation from an NLP research project based on the official SimPO repository. The goal is to evaluate your ability to read a research paper, understand the core training objective, work with an existing codebase, and reproduce the expected behavior in a controlled environment.

You are given the official SimPO repository, and the paper is located at /root/SimPO/paper.pdf.
---

## Task 1: Implement the SimPO loss
Your first task is to understand the paper and implement the SimPO loss in the `SimPOTrainer` class.

## Task 2: Set up the correct environment for the project
If there are any existing components in the environment that conflict with the project requirements, please resolve or replace them accordingly.

# Evaluation Requirement
After you finish the implementation, run the test script located at `/root/SimPO/unit_test/unit_test_1.py` to generate the loss values for evaluation using fixed input tensors.
Fixed input matrices for the loss function are already provided, and your implementation is expected to produce the correct output matrix.

Save the output to `/root/loss.npz` with the key `losses`.

Please also log the Python version and installed packages by running:
- `python -VV`
- `python -m pip freeze`

Save both outputs to `/root/python_info.txt` so the results can be reproduced.

You must not modify the contents of `unit_test.py`.