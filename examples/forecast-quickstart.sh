#!/bin/env bash
set -e

# an example of how to use the convect forecast API to trigger a forecast run

# fetch the token 
export CLIENT_ID="<YOUR CLIENT ID HERE>"
export CLIENT_SECRET='<YOUR CLIENT SECRET HERE>'
export BASE_URL='https://forecast.convect.ai/api'

TOKEN=$(curl -s --request POST $BASE_URL/auth/tokens \
    -H 'Content-Type: application/json' \
    --data-binary @- << EOF | jq -r '.access_token'
    {
        "client_id": "${CLIENT_ID}",
        "client_secret": "${CLIENT_SECRET}",
        "audience": "https://forecast.convect.ai",
        "grant_type": "client_credentials"
    }
EOF
)

echo "token: ${TOKEN}"

export AUTH_HEADER="Authorization: Bearer ${TOKEN}"

# create a dataset group
data_group_id=$(curl -s --request POST $BASE_URL/data-groups/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" \
    --data '{"name": "Demo data group"}' | jq '.id')

# information about the dataset group
curl -s --request GET $BASE_URL/data-groups/${data_group_id}/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" | jq

# upload a dataaset
export data_url="https://convect-test-data.s3.us-west-2.amazonaws.com/forecast_test_data/target_ts.csv"
curl -s --request POST $BASE_URL/datasets/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" \
    --data-binary @- << EOF
    {
        "name": "target time series",
        "dataset_type": "TARGET_TIME_SERIES",
        "path": "${data_url}",
        "file_format": "csv",
        "frequency": "W",
        "data_group": ${data_group_id},
        "schemas": [
            {"name": "sku", "col_type": "key"},
            {"name": "week", "col_type": "time"},
            {"name": "qty", "col_type": "num"}
        ]
    }
EOF


# set up a forecat config
export output_path='s3://convect-data/result/demo-run'

config_id=$(curl -s --request POST $BASE_URL/predictor-configs/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" \
    --data-binary @- << EOF | jq '.id'
    {
        "name": "12 week forecast config",
        "result_uri": "${output_path}",
        "horizon": 14,
        "frequency": "W",
        "data_group": ${data_group_id}
    }
EOF
 )

echo "config id: ${config_id}"


# trigger a forecast run
run_id=$(curl -s --request POST $BASE_URL/predictors/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" \
    --data-binary @- << EOF | jq '.id' 
    {
        "predictor_config": ${config_id}
    }
EOF
 )

echo "run id: ${run_id}"


# query the run status until it is done, or failed, or timed out
timeout=600
while [ $timeout -gt 0 ]; do
    job_status=$(curl -s --request GET $BASE_URL/predictors/${run_id}/ \
        -H 'Content-Type: application/json' \
        -H "$AUTH_HEADER" | jq '.status.status')
    echo "status: ${job_status}"
    if [ "$job_status" == '"Succeeded"' ]; then
        break
    elif [ "$job_status" == '"Failed"' ]; then
        break
    fi
    sleep 10
    timeout=$((timeout-10))
done


# retrieve the result
result_uri=$(curl -s --request GET $BASE_URL/predictors/${run_id}/ \
    -H 'Content-Type: application/json' \
    -H "$AUTH_HEADER" | jq -r '.result_uri')

echo "result uri: ${result_uri}"

# download the result as result.csv
curl -fsSL ${result_uri} -o result.csv

# check the result
head -n 10 result.csv
