def test_uk_microsimulation():
    from policyengine_uk import Microsimulation

    # Create a Microsimulation instance
    sim = Microsimulation()


def test_uk_reweight():
    from policyengine_uk import Microsimulation
    from reweight import reweight
    import torch

    sim = Microsimulation()

    from policyengine_uk.data import RawFRS_2021_22

    RawFRS_2021_22().download()

    from policyengine_uk.data.datasets.frs.calibration.calibrate import (
        generate_model_variables,
    )

    (
        household_weights,
        weight_adjustment,
        values_df,
        targets,
        targets_array,
        equivalisation_factors_array,
    ) = generate_model_variables("frs_2021", 2025)

    sim_matrix = torch.tensor(values_df.to_numpy(), dtype=torch.float32)
    reweight(household_weights, sim_matrix, targets, targets_array)
