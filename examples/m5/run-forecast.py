import pandas as pd
import requests
import os.path

"""
Upload files to s3

!aws s3 sync data/by_store/ s3://convect-data/m5/by_store/
"""

stores = [
    "ca_1",
    "ca_2",
    "ca_3",
    "ca_4",
    "tx_1",
    "tx_2",
    "tx_3",
    "wi_1",
    "wi_2",
    "wi_3",
]
endpoint = "https://forecast.convect.ai/api/"

# helper functions
def get_ts_path(store_id):
    return f"s3://convect-data/m5/by_store/{store_id.lower()}_target_time_series.csv.gz"


def get_meta_path():
    return f"s3://convect-data/m5/by_store/m5_item_meta.csv"


def create_data_group(store_id):
    url = os.path.join(endpoint, "data-groups/")

    payload = {"name": f"{store_id}-data-groups"}

    url = os.path.join(endpoint, "data-groups/")

    resp = requests.post(url, json=payload)

    resp_payload = resp.json()

    return resp_payload["id"]


def create_ts_dataset(store_id, data_group_id):
    url = os.path.join(endpoint, "datasets/")

    payload = {
        "name": f"target_time_series_{store_id}",
        "dataset_type": "TARGET_TIME_SERIES",
        "path": get_ts_path(store_id),
        "file_format": "csv",
        "frequency": "D",
        "data_group": data_group_id,
        "schemas": [
            {"name": "id", "col_type": "key"},
            {"name": "date", "col_type": "time"},
            {"name": "sales", "col_type": "num"},
        ],
    }

    resp = requests.post(url, json=payload)
    resp_payload = resp.json()
    print(resp_payload)

    return resp_payload["id"]


def create_meta_dataset(store_id, data_group_id):
    url = os.path.join(endpoint, "datasets/")

    payload = {
        "name": f"item_meta_{store_id}",
        "dataset_type": "ITEM_METADATA",
        "path": get_meta_path(),
        "file_format": "csv",
        "data_group": data_group_id,
        "schemas": [
            {"name": "id", "col_type": "key"},
            {"name": "dept_id", "col_type": "str"},
            {"name": "cat_id", "col_type": "str"},
        ],
    }

    resp = requests.post(url, json=payload)
    resp_payload = resp.json()
    print(resp_payload)

    return resp_payload["id"]


def create_predictor_config(store_id, data_group_id):
    url = os.path.join(endpoint, "predictor-configs/")

    payload = {
        "name": f"validation-forecast-config-{store_id}",
        "result_uri": f"s3://convect-data/test-data/m5-api-result/{store_id}/",
        "horizon": 28,
        "frequency": "D",
        "data_group": data_group_id,
    }

    res = requests.post(url, json=payload)
    resp_payload = res.json()
    print(resp_payload)

    return resp_payload["id"]


def create_predictor(config_id):
    url = os.path.join(endpoint, "predictors/")

    payload = {"predictor_config": config_id}

    res = requests.post(url, json=payload)
    resp_payload = res.json()
    print(resp_payload)

    return resp_payload["id"]


def query_predictor_status(predictor_id):
    url = os.path.join(endpoint, "predictors/")

    res = requests.get(os.path.join(url, str(predictor_id)))

    return res.json()


def start_prediction_by_api(store_id):
    data_group_id = create_data_group(store_id)
    _ = create_ts_dataset(store_id, data_group_id)
    _ = create_meta_dataset(store_id, data_group_id)
    config_id = create_predictor_config(
        store_id, data_group_id
    )
    predictor_id = create_predictor(config_id)
    return query_predictor_status(predictor_id)


# trigger the prediction
for store in stores:
    start_prediction_by_api(store)
