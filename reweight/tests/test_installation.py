def test_imports():
    try:
        import torch
        import numpy as np
        from torch.utils.tensorboard import SummaryWriter
    except:
        raise AssertionError("Failed to import necessary libraries")

def test_install():
    try:
        import reweight
    except:
        raise AssertionError("Failed to build reweight")