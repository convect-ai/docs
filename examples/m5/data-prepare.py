import pandas as pd

# read the data
df_sales = pd.read_csv("data/sales_train_evaluation.csv")
df_cal = pd.read_csv("data/calendar.csv")

store_id_set = df_sales.store_id.unique()

idcols = [
    "id",
    "item_id",
    "dept_id",
    "cat_id",
    "store_id",
    "state_id",
]

# function to split data by store
# and convert wide format to long format


def process_store(
    store_id,
):
    print(store_id, "START")
    df_store = df_sales[df_sales.store_id == store_id]
    df_ts = pd.melt(
        df_store, id_vars=idcols, value_name="sales"
    )
    df_ts = df_ts.merge(
        df_cal[["date", "d"]],
        left_on="variable",
        right_on="d",
        how="left",
    )
    df_ts[["id", "date", "sales"]].to_csv(
        f"data/by_store/{store_id.lower()}_target_time_series.csv.gz",
        index=False,
        compression="gzip",
    )

    print(store_id, "END")


# trigger the processing
from multiprocessing import Pool
from itertools import product

with Pool(processes=6) as p:
    p.starmap(process_store, product(store_id_set))

# process the meta data
df_meta = (
    df_sales[idcols]
    .drop_duplicates()
    .drop(["store_id", "state_id", "item_id"], axis=1)
)
df_meta.to_csv(
    f"data/by_store/m5_item_meta.csv", index=False
)
