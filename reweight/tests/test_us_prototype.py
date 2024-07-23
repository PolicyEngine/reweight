def test_us_prototype():
    from policyengine_us import Microsimulation, Simulation
    import numpy as np
    import torch
    from torch.utils.tensorboard import SummaryWriter

    # Initialize a TensorBoard writer
    writer = SummaryWriter()

    # Create a Microsimulation instance
    sim = Microsimulation()

    # Compute income and payroll taxes. These are MicroSeries objects from the microdf library
    income_tax_microseries = sim.calculate(
        "income_tax", 2023, map_to="household"
    )
    payroll_tax_microseries = sim.calculate(
        "employee_payroll_tax", 2023, map_to="household"
    )

    # Convert them into usable NumPy arrays
    sim_income_tax = np.array(income_tax_microseries)
    sim_payroll_tax = np.array(payroll_tax_microseries)
    sim_weights = np.array(income_tax_microseries.weights)

    log_weights = np.log(sim_weights)

    # Initialize usable ground truth income and payroll tax values
    targets = np.array([2_176_000_000_000, 1_614_454_000_000])
    target_names = np.array(["income tax revenue", "payroll tax revenue"])

    sim_matrix = np.array([sim_income_tax, sim_payroll_tax])

    # sim_matrix (cross) exp(log_weights) = targets
    log_weights = torch.tensor(
        log_weights, dtype=torch.float32, requires_grad=True
    )
    sim_matrix = torch.tensor(sim_matrix, dtype=torch.float32)
    targets = torch.tensor(targets, dtype=torch.float32)

    optimizer = torch.optim.Adam([log_weights])

    # Training loop
    num_epochs = 20000
    for epoch in range(num_epochs):

        # Estimate the targets
        targets_estimate = sim_matrix @ torch.exp(log_weights)
        # Calculate the loss
        loss = torch.mean((targets_estimate - targets) ** 2)

        writer.add_scalar("Loss/train", loss, epoch)

        optimizer.zero_grad()

        # Perform backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        # Print loss for every 1000 epochs
        if epoch % 1000 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item()}")

    writer.flush()

    final_weights = np.exp(log_weights.detach().numpy())
    final_estimates = (
        np.array([sim_income_tax, sim_payroll_tax]) @ final_weights
    )
    true_values = targets
    print("Final weights:", final_weights)
    print("Final estimates:", final_estimates)
    print("True values:", true_values)


def test_us_microsimulation():
    from policyengine_us import Microsimulation

    # Create a Microsimulation instance
    sim = Microsimulation()


def test_us_reweight():
    from policyengine_us import Microsimulation
    from reweight import reweight
    import torch

    sim = Microsimulation()

    from policyengine_us.data.datasets.cps.enhanced_cps.loss import (
        generate_model_variables,
    )

    (
        household_weights,
        weight_adjustment,
        values_df,
        targets,
        targets_array,
        equivalisation_factors_array,
    ) = generate_model_variables("cps_2021", 2025)

    sim_matrix = torch.tensor(values_df.to_numpy(), dtype=torch.float32)
    weights_tensor = torch.tensor(household_weights, dtype=torch.float32)
    targets_tensor = torch.tensor(targets_array, dtype=torch.float32)
    reweight(weights_tensor, sim_matrix, targets, targets_tensor)
