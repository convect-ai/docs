
## Dataset Types Supported

Convect™ Forecast supports the following types of datasets:

* Target time series
* Related time series 
* Item meta information 

**Target time series** data is the only dataset type needed to build a forecasting model. The dataset records the time series values for an entity at different historical timestamps. For example, for an retailer, the data captures the unit sold for each product at different dates.

**Related time series** data captures time-varying values that are not direct targets to be forecasted associated with entities. For example, the data may record the price of a product on each date. 

**Item meta information** provides additional information static across time about the entity to be forecasted. For example, the data may contain categorical information such as brands, categories, and vendors of entities.

## Data Formats

All 3 types of datasets require one or multiple columns that indicate the identifiers of entities. For example, for an retailer, these columns may include a *SKU* plus a *store* id that uniquely define the identity of an entity to be forecasted.

### Target time series

The dataset requires at least 3 columns:

* 1 or more columns that serve as the key column(s) mentioned above
* 1 timestamp column that marks when the observation was recorded
* 1 value column that stores the actual value of the time series

For example

model      |week       |qty    
-----------|-----------|-------
1163704	   |2017-01-01 |267    
1163704	   |2017-01-08 |229    
5998369    |2017-01-01 |1689   
5998369    |2017-01-08 |1322   

where `model` is the key column of the entity; `week` is the timestamp column; `qty` stores the actual time series value.

### Related time series 

Similarly to target time series data, the dataset requires at least 3 columns: 

* 1 or more columns that serve as the key column(s) mentioned above
* 1 timestamp column that marks when the observation was recorded
* 1 or more value columns that store the actual values of the related time series values

For example

model      |week       |price    |    temperature
-----------|-----------|---------|---------------
1163704	   |2017-01-01 |12.5     |  20.5
1163704	   |2017-01-08 |12.3     |  22.3
5998369    |2017-01-01 |5.6      |  20.5
5998369    |2017-01-08 |4.5      |  22.3

where `model` is the key column of the entity; `week` is the timestamp column; `price` and `temperature` store two related time series values about the entity.

### Item meta information

Item meta information requires at least 2 columns:

* 1 or more columns that serve as the key column(s) mentioned above
* 1 or more value columns that store some meta information about the entity

For example

model      |brand     |category    
-----------|----------|-------
1163704	   |XXX       |Food    
5998369    |YYY       |Pet

where `model` is the key column of the entity; `brand` and `category` are the meta information associated to each entity.

!!! note
    Item meta information dataset does not require a timestamp column as target and related time series datasets.

## Calling Datagroup APIs

Once you have the datasets prepared in the described formats, the first step toward building a model on top is to declare those datasets by calling the `datagroup` APIs.

### Upload the datasets

Before calling the APIs, it's better to make datasets available as remote urls. To do so, there are multiple options:

* Upload to an Object Storage such as S3, Google Cloud Storage and make the file available to be read (by either making it public or pre-signing it)
* Upload to a share drive such as Dropbox, Google Drive and generate a sharing url
* Self host it at a file server (e.g, samba)

### Declare Datasets Using API

**Step1**. Create a `datagroup`

`datagroups` serves as the container to host multiple datasets that are related. You can give it whatever name that makes sense to you.

=== "python"
    ```python
    {!> forecast-quickstart.py [ln:1-25] !}
    ```

=== "curl"
    ```bash
    {!> forecast-quickstart.sh [ln:1-36] !}
    ```

**Step2**. Declare target time series `datasets` under a `datagroup`

The next step is to associate individual `dataset` object to a `datagroup`. When declaring the `dataset`, users also need to provide the schema about the dataset, i.e., names of the columns and their roles. For example, below code associate a target time series `dataset` to a `datagroup`.

=== "python"
    ```python
    {!> forecast-quickstart.py [ln:27-47] !}
    ```

=== "curl"
    ```python
    {!> forecast-quickstart.sh [ln:38-57] !}
    ```

* `dataset_type` specifies the type of the dataset. Available options are `TARGET_TIME_SERIES`, `RELATED_TIME_SERIES`, and `ITEM_META`.
* `path` points to the remote url of the file uploaded. Here we use S3 as the file storage.
* `frequency` specifies the frequency the time series was recorded.
* `schemas` is a list of dict. Each entry contains `name` of the column, `col_type` specifies the type and role of the column.

**Step3**. (Optional) Declare more dataset types under the data group.

Similarly, you can declare more individual datasets, such as related time series and item meta information. Below is an example of declaring an item meta information

```python
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
```


