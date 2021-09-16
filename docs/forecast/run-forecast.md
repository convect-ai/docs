
## Forecast Configuration

Once you finish declaring all the `datasets` associated with a `datagroup`, you can proceed to set up a forecast configuration.

The configuration defines the forecast task, e.g., how long should the forecast horizon be, what metrics to use when evaluating models, and if uncertainty interval should be included in the results, where to write the result files.

For example, code below sets up a task that outputs the consecutive 14-week predicted value starting from the last date in the dataset.

=== "python"
    ```python
    {!> forecast-quickstart.py [ln:48-62] !}
    ```

=== "curl"
    ```bash
    {!> forecast-quickstart.sh [ln:35-49] !}
    ```

## Trigger Forecast

Once a config is set up, we can trigger the actual forecast run by calling `POST` endpoint `predictors/` by providing the id of the config.

=== "python"
    ```python
    {!> forecast-quickstart.py [ln:65-69] !}
    ```

=== "curl"
    ```bash
    {!> forecast-quickstart.sh [ln:52-55] !}
    ```

## Retrieve Result

Once a run is triggered, query the status of the run by calling `GET` endpoint `predictors/{id}`.

=== "python"
    ```python
    {!> forecast-quickstart.py [ln:72-77] !}
    ```

=== "curl"
    ```bash
    {!> forecast-quickstart.sh [ln:59-61] !}
    ```

Once the returned `status` is indicated as `Succeeded`, you can read the result from the output path specified when setting up the forecast config.

Below is an example of the result file

key|sku|predict_sum|predict_start_date|predict_horizon
---|---|---------|----------------|----------
11000015|11000015|1.000000027104373|2021-08-31|7
11000016|11000016|3.000000027104373|2021-08-31|7
11000017|11000017|1.000000027104373|2021-08-31|7
11000018|11000018|1.0577409169104601|2021-08-31|7
11000019|11000019|0.998951528482072|2021-08-31|7
11000020|11000020|1.0051190404354284|2021-08-31|7
11000021|11000021|0.9999988959151295|2021-08-31|7



