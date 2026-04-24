---
name: reproducing-dl-papers
description: How to reproduce Deep Learning papers. Use this skill whenever the user asks to implement an algorithm, loss function, architecture, or technique based on an academic paper (PDF, Arxiv, etc).
---

# Reproducing Deep Learning Papers

This skill provides guidelines on correctly transcribing Deep Learning methodology into working code.

## Workflow

1. **Understand Key Equations:** Identify the equations governing the process. In NLP, this includes the forward pass, probability distributions (softmax), loss formulation (e.g., negative log-likelihood, ranking loss, KL divergence), and the treatment of reference vs policy models.
2. **Handle Hyperparameters:** Identify all parameters that control behavior (e.g., margins, temperatures, weightings like $\beta$ or $\gamma$). Expose these as function arguments.
3. **Analyze Dimension Semantics:** When implementing tensor operations, ensure dimensions align with the paper's math. For example, if a paper calculates the sum of log probabilities per sequence, the `sum` operation should be over the sequence dimension `dim=-1`.
4. **Compare to Existing Methods:** Most new algorithms contrast themselves with existing methods (like DPO, IPO, or PPO in RLHF). Understanding the baseline can clarify what the new method actually changes.
5. **Verify Inputs:** Check what inputs are provided in the environment/test code and adapt to their shape and type.
