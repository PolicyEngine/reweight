import pandas as pd
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter


def reweight(
    initial_weights,
    estimate_matrix,
    target_names,
    target_values,
    epochs=1000,
    epoch_step=100,
):
    """
    Main reweighting function, suitable for PolicyEngine UK use (PolicyEngine US use and testing TK)

    To avoid the need for equivalisation factors, use relative error:
    |predicted - actual|/actual

    Parameters:
    household_weights (torch.Tensor): The initial weights given to survey data, which are to be
    adjusted by this function.
    estimate_matrix (torch.Tensor): A large matrix of estimates, obtained from e.g. a PolicyEngine
    Microsimulation instance.
    target_names (iterable): The names of a set of target statistics treated as ground truth.
    target_values (torch.Tensor): The values of these target statistics.
    epochs: The number of iterations that the optimization loop should run for.
    epoch_step: The interval at which to print the loss during the optimization loop.

    Returns:
    final_weights: a reweighted set of household weights, obtained through an optimization process
    over mean squared errors with respect to the target values.
    """
    # Initialize a TensorBoard writer
    writer = SummaryWriter()

    # Create a Torch tensor of log weights
    log_weights = torch.log(initial_weights)
    log_weights.requires_grad_()

    # estimate_matrix (cross) exp(log_weights) = target_values

    optimizer = torch.optim.Adam([log_weights])

    # Report the initial loss:
    targets_estimate = torch.exp(log_weights) @ estimate_matrix
    # Calculate the loss
    loss = torch.mean(
        ((targets_estimate - target_values) / target_values) ** 2
    )
    print(f"Initial loss: {loss.item()}")

    # Training loop
    for epoch in range(epochs):

        # Estimate the targets
        targets_estimate = torch.exp(log_weights) @ estimate_matrix
        # Calculate the loss
        loss = torch.mean(
            ((targets_estimate - target_values) / target_values) ** 2
        )

        writer.add_scalar("Loss/train", loss, epoch)

        optimizer.zero_grad()

        # Perform backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        # Print loss whenever the epoch number, when one-indexed, is divisible by epoch_step
        if (epoch + 1) % epoch_step == 0:
            print(f"Epoch {epoch+1}, Loss: {loss.item()}")

    writer.flush()

    return torch.exp(log_weights.detach())
