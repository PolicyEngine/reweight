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
    generate_model_variables,
)

from reweight import reweight

# UK dataframe generation.
sim = Microsimulation()

RawFRS_2021_22().download()

uk_weights_df = pd.DataFrame()

for year in range(2024, 2029):
    (
        household_weights,
        weight_adjustment,
        values_df,
        targets,
        targets_array,
        equivalisation_factors_array,
    ) = generate_model_variables("frs_2021", year)
    sim_matrix = torch.tensor(values_df.to_numpy(), dtype=torch.float32)
    uk_final_weights = reweight(
        household_weights, sim_matrix, targets, targets_array, epochs=1_000
    )
    uk_weight_series = pd.Series(uk_final_weights.numpy())
    uk_weights_df[str(year)] = uk_weight_series


csv_filename = "updated_uk_weights.csv"
uk_weights_df.to_csv(csv_filename)


# US dataframe generation.

import policyengine_us
from policyengine_us.data.datasets.cps.enhanced_cps.loss import (
    generate_model_variables,
)

us_weights_df = pd.DataFrame()

for year in range(2024, 2029):
    (
        household_weights,
        weight_adjustment,
        values_df,
        targets,
        targets_array,
        equivalisation_factors_array,
    ) = generate_model_variables("cps_2021", year)
    sim_matrix = torch.tensor(values_df.to_numpy(), dtype=torch.float32)
    initial_weights = torch.tensor(household_weights, dtype=torch.float32)
    targets_tensor = torch.tensor(targets_array, dtype=torch.float32)
    us_final_weights = reweight(
        initial_weights, sim_matrix, targets, targets_tensor, epochs=1_000
    )
    us_weight_series = pd.Series(us_final_weights.numpy())
    us_weights_df[str(year)] = us_weight_series

# Now, for testing, save these dataframes as CSV.

csv_filename = "updated_us_weights.csv"
us_weights_df.to_csv(csv_filename)

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
