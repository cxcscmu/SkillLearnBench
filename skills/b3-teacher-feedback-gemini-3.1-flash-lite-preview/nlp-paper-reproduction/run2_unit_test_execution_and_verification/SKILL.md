---
name: unit_test_execution_and_verification
description: Creates an orchestration script to run the immutable unit test and capture the output loss values.
---
1. Create a script `/root/run_verification.py` that imports `SimPOTrainer` from `/root/SimPO/scripts/simpo_trainer.py`.
2. Within this script, import the testing logic from `/root/SimPO/unit_test/unit_test_1.py`.
3. Execute the unit test functions while capturing the returned `loss` tensor.
4. Convert the captured tensor to a numpy array, ensuring it is cast to `float32`.
5. Use `numpy.savez('/root/loss.npz', losses=captured_array)` to persist the results for final evaluation.