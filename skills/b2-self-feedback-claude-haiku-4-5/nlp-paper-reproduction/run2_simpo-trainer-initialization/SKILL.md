---
name: run2_simpo-trainer-initialization
description: Proper initialization of SimPOTrainer with model loading and args setup
---

# SimPOTrainer Initialization and Setup

## Critical Initialization Requirements

The SimPOTrainer extends HuggingFace's Trainer and requires proper initialization to function:

### 1. Parent Class Initialization (MUST UNCOMMENT)
```python
super().__init__(
    model=model,
    args=args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    model_init=model_init,
    compute_metrics=compute_metrics,
    callbacks=callbacks,
    optimizers=optimizers,
    preprocess_logits_for_metrics=preprocess_logits_for_metrics,
)
```
**Why Critical**: Sets up `self.args` which is required by all loss functions and training logic.

### 2. Model Handling
If `model` is a string (model ID), it must be loaded before passing to parent:
```python
if isinstance(model, str):
    model_init_kwargs = args.model_init_kwargs or {}
    model = AutoModelForCausalLM.from_pretrained(model, **model_init_kwargs)
```
**Why**: The parent Trainer class expects a loaded model instance, not a string ID.

### 3. Required Arguments (SimPOConfig)
The `args` parameter must be a `SimPOConfig` instance with at minimum:
```python
args = SimPOConfig(
    output_dir="./simpo_output",  # REQUIRED
    beta=2.0,                      # Reward scaling (default: 2.0)
    gamma_beta_ratio=0.25,         # Margin ratio (default: 0.25)
)
```

## Initialization Checklist

- [ ] Create `SimPOConfig` with `output_dir`
- [ ] Load model if passing string ID
- [ ] Call `super().__init__()` with all required parameters
- [ ] Verify `self.args` is accessible after init
- [ ] Verify `self.model` is on correct device

## Common Initialization Errors

### Error 1: AttributeError: 'SimPOTrainer' object has no attribute 'args'
**Cause**: `super().__init__()` not called
**Fix**: Uncomment the super().__init__() block in __init__

### Error 2: AttributeError: 'str' object has no attribute 'to'
**Cause**: Passing string model ID without loading it first
**Fix**: Uncomment the model loading logic that converts string to loaded model

### Error 3: TypeError: tokenizer must be specified
**Cause**: tokenizer parameter is None
**Fix**: Pass a valid PreTrainedTokenizerBase instance (or handle gracefully)

## Testing Initialization

```python
import torch
from scripts.simpo_trainer import SimPOTrainer
from scripts.simpo_config import SimPOConfig

# Create minimal config
config = SimPOConfig(output_dir="./test_output")

# Initialize trainer with model ID
trainer = SimPOTrainer(
    model="sshleifer/tiny-gpt2",  # Will auto-load
    args=config
)

# Verify initialization
assert hasattr(trainer, 'args'), "args not set"
assert hasattr(trainer, 'model'), "model not set"
assert trainer.args.beta == 2.0, "default beta not set"
print("Initialization successful!")
```

## Access to Config Values in Methods

Once properly initialized, any method can access config values:
```python
def some_method(self):
    beta = self.args.beta                    # Get beta parameter
    gamma_ratio = self.args.gamma_beta_ratio # Get gamma ratio
    device = self.args.device                # Get device
    lr = self.args.learning_rate             # Get learning rate
```

This is essential for the `simpo_loss()` method to compute gamma correctly.
