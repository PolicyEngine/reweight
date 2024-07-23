def test_integrated_prototype():
    import numpy as np
    import torch
    from torch.utils.tensorboard import SummaryWriter

    # Initialize a TensorBoard SummaryWriter instance
    writer = SummaryWriter()

    # Survey of three records

    # Three households surveyed, survey gave them weights of 100, 500, 300
    initial_weights = np.array([100, 500, 300])
    log_weights = np.log(initial_weights)

    # total population, income tax revenue, VAT revenue
    targets = np.array([1e6, 5e9, 6e9])
    target_names = np.array(
        ["total population", "income tax revenue", "VAT revenue"]
    )

    # initial weights (cross) matrix = targets
    matrix = np.array([[1, 1, 1], [300, 500, 250], [100, 200, 300]])

    log_weights = torch.tensor(
        log_weights, dtype=torch.float32, requires_grad=True
    )
    matrix = torch.tensor(matrix, dtype=torch.float32)
    targets = torch.tensor(targets, dtype=torch.float32)

    optimizer = torch.optim.Adam([log_weights])

    # Training loop
    num_epochs = 1_000
    for epoch in range(num_epochs):

        # Estimate the targets
        targets_estimate = matrix @ torch.exp(log_weights)
        # Calculate the loss
        loss = torch.mean((targets_estimate - targets) ** 2)

        writer.add_scalar("Loss/train", loss, epoch)

        optimizer.zero_grad()

        # Perform backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        # Print loss for every 1000 epochs
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    writer.flush()

    # Print final weights
    print("Final weights:", np.exp(log_weights.detach().numpy()))
