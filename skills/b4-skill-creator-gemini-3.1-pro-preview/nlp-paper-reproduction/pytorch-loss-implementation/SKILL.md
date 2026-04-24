---
name: pytorch-loss-implementation
description: How to implement custom loss functions in PyTorch. Use this skill whenever the user asks to implement a loss function, write a custom criterion, or mentions PyTorch tensor operations for backpropagation.
---

# PyTorch Loss Implementation

This skill provides guidelines for implementing custom loss functions in PyTorch. 

## Key Principles

1. **Use PyTorch Primitives:** Always use `torch.*` operations (e.g., `torch.log`, `torch.exp`, `torch.sum`, `F.log_softmax`) to ensure operations are differentiable and can be tracked by autograd.
2. **Numerical Stability:** Be careful with operations like log and exp. Use numerically stable functions like `F.log_softmax` instead of taking the log of a softmax, and `F.binary_cross_entropy_with_logits` instead of applying sigmoid then BCE.
3. **Handling Padding and Masks:** When working with NLP or sequence data, always apply attention masks or ignore_index appropriately to prevent padded tokens from contributing to the loss.
4. **Batch Reductions:** By default, loss functions should support different reduction methods ('mean', 'sum', 'none'). Be explicit about how reductions are applied across batch and sequence dimensions.

## Example Pattern

```python
import torch
import torch.nn.functional as F

def custom_loss(logits, targets, mask=None, reduction='mean'):
    # Apply operations
    loss = F.cross_entropy(logits, targets, reduction='none')
    
    # Apply mask if provided
    if mask is not None:
        loss = loss * mask
        if reduction == 'mean':
            return loss.sum() / mask.sum()
        elif reduction == 'sum':
            return loss.sum()
        return loss
        
    if reduction == 'mean':
        return loss.mean()
    elif reduction == 'sum':
        return loss.sum()
    return loss
```
