import pandas as pd

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


# combine the resuls
base_out_path = "s3://convect-data/test-data/m5-api-result/by_store/{}/data"


dfs = []
for store in stores:
    dfs.append(pd.read_csv(base_out_path.format(store)))
df_pred = pd.concat(dfs, axis=0).drop(
    ["Unnamed: 0"], axis=1
)

df_pred["dt_label"] = pd.to_datetime(
    df_pred["predict_start_date"]
) - pd.to_datetime("2016-04-24")
df_pred["dt_label"] = "F" + df_pred[
    "dt_label"
].dt.days.astype(str)
df_pred["id"] = df_pred["id"].map(
    lambda x: x + "_" + "evaluation"
)

# long to wide format
df_wide = df_pred[["id", "predict_sum", "dt_label"]].pivot(
    index="id", columns="dt_label", values="predict_sum"
)

# reorder the columns
cols = list(map(lambda x: f"F{x}", range(1, 29)))
df_wide = df_wide[cols]
df_wide.to_csv("submission.csv")
