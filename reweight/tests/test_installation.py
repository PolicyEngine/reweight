def test_imports():
    try:
        import torch
        import numpy as np
        import policyengine_core
        from torch.utils.tensorboard import SummaryWriter
    except:
        raise AssertionError("Failed to import necessary libraries")


def test_install():
    try:
        import reweight
    except:
        raise AssertionError("Failed to build reweight")


def test_secret_usage():
    import os

    token = os.environ["POLICYENGINE_GITHUB_MICRODATA_AUTH_TOKEN"]
    token_not_none = token != None
    assert token_not_none, "Authentication token is None"
