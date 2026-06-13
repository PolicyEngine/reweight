import pandas as pd
import numpy as np
import torch
from torch.utils.tensorboard import SummaryWriter
import os
import requests
import base64

import policyengine_uk
from policyengine_uk import Microsimulation
from policyengine_uk.data import RawFRS_2021_22
from policyengine_uk.data.datasets.frs.calibration.calibrate import (
    generate_model_variables as uk_generate,
)

import policyengine_us
from policyengine_us.data.datasets.cps.enhanced_cps.loss import (
    generate_model_variables as us_generate,
)

from reweight import reweight


def generate_country_weights(year, data_source, generate_func):
    """
    Parameters:
    year (int): The year for which these country values are generated.
    data_source (str): The name of the data source for that country.
    generate_func (function): The function used to generate the initial values.

    Returns:
    final_weights (torch.Tensor): a PyTorch tensor of final reweighted weights.
    """
    (
        household_weights,
        weight_adjustment,
        values_df,
        targets,
        targets_array,
        equivalisation_factors_array,
    ) = generate_func(data_source, year)
    sim_matrix = torch.tensor(values_df.to_numpy(), dtype=torch.float32)
    initial_weights = torch.tensor(household_weights, dtype=torch.float32)
    targets_tensor = torch.tensor(targets_array, dtype=torch.float32)
    final_weights = reweight(
        initial_weights, sim_matrix, targets, targets_tensor, epochs=1_000
    )
    return final_weights


def generate_country_csv(
    start_year, end_year, data_source, generate_func, csv_filename
):
    """
    Parameters:
    start_year (int): The year for which these country values start generating (inclusive).
    end_year (int): The year for which these country values stop generating (non-inclusive).
    data_source (str): The name of the data source for that country.
    generate_func (function): The function used to generate the initial values.
    csv_filename (str): The name of the file which the generated data are saved under.

    Returns:
    None. Generates and saves a CSV file of reweighted weights.
    """
    weights_df = pd.DataFrame()
    for year in range(start_year, end_year):
        final_weights = generate_country_weights(
            year, data_source, generate_func
        )
        weight_series = pd.Series(final_weights.numpy())
        weights_df[str(year)] = weight_series
    weights_df.to_csv(csv_filename)


RawFRS_2021_22().download()
generate_country_csv(
    2024, 2029, "frs_2021", uk_generate, "updated_uk_weights.csv"
)
generate_country_csv(
    2024, 2029, "cps_2021", us_generate, "updated_us_weights.csv"
)

# Now, create a GitHub release

api_url = "https://api.github.com/repos/PolicyEngine/reweight/releases"

owner = "pmberg"
repo = "reweight"
token = os.environ.get("API_GITHUB_TOKEN")

# Create release
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json",
}
release_data = {
    "tag_name": f'v{pd.Timestamp.now().strftime("%Y.%m.%d.%H.%M.%S")}',
    "name": f'Data Release {pd.Timestamp.now().strftime("%Y.%m.%d.%H.%M.%S")}',
    "body": "Automated data release with updated weights",
}
response = requests.post(
    api_url.format(owner=owner, repo=repo), headers=headers, json=release_data
)
release = response.json()
print(release)
# Upload assets
upload_url = release["upload_url"].split("{")[0]


def upload_file(file_name):
    with open(file_name, "rb") as file:
        content = file.read()
    headers["Content-Type"] = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    params = {"name": os.path.basename(file_name)}
    response = requests.post(
        upload_url, headers=headers, params=params, data=content
    )
    if response.status_code == 201:
        print(f"File added successfully: {release['html_url']}")
    else:
        print(f"Failed to add file: {response.content}")


for file_name in ["updated_uk_weights.csv", "updated_us_weights.csv"]:
    upload_file(file_name)
