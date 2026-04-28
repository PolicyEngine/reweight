import pytest


def microsimulation_or_skip(microsimulation_class):
    try:
        return microsimulation_class()
    except ValueError as error:
        if "requires an explicit dataset" in str(error):
            pytest.skip(str(error))
        raise


def test_uk_microsimulation():
    from policyengine_uk import Microsimulation

    # Create a Microsimulation instance
    sim = microsimulation_or_skip(Microsimulation)


def test_uk_reweight():
    from policyengine_uk import Microsimulation
    from reweight import reweight
    import torch

    sim = microsimulation_or_skip(Microsimulation)

    data_module = pytest.importorskip("policyengine_uk.data")
    RawFRS_2021_22 = data_module.RawFRS_2021_22

    RawFRS_2021_22().download()

    calibration_module = pytest.importorskip(
        "policyengine_uk.data.datasets.frs.calibration.calibrate"
    )
    generate_model_variables = calibration_module.generate_model_variables

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
