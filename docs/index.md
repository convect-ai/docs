
<!-- logo -->
<img src="https://i1.wp.com/convect.ai/wp-content/uploads/2021/08/Color-logo-no-background.png" 
    alt="Logo" width="400" height="100" style="display: block; margin: 0 auto" />

## Introduction

Convect™ AI Decision API is a collection of out-of-box APIs that supports the most common decision problems in Supply Chain Optimization. The goal is to let Convect™ take care of the heavy-lifting part of building and tuning algorithms & allocating computing resources, so you can load light and add intelligence easily when developing supply chain decision applications.

Specifically, Convect™ currently provides APIs to solve two types of problems:

* [Automated forecasting](./forecast/overview.md)
* [Supply-demand planning](./flowopt/overview.md)


## Quickstart

Convect™ implements the [REST](https://blog.hubspot.com/website/what-is-rest-api) style APIs to enable users to activate models that solve decision problems programmatically. For a more comprehensive reference of the available APIs, please see [reference](https://forecast.convect.ai/api/schema/redoc/).


### Obtaining API credentials

1. Register on [Convect Platform](https://forecast.convect.ai/)
2. Go to the account settings page to obtain a pair of API `id` and `secrets`. Or contact [Convect Support](mailto:hi@convect.ai) to obtain a demo key
3. Once you have your `client_id` and `client_secret`, before calling the API, obtain an access token by sending a `POST` request as 

```bash
curl --request POST \
  --url https://forecast.convect.ai/api/auth/tokens \
  --header 'content-type: application/json' \
  --data '{"client_id":"{YOUR_CLIENT_ID}","client_secret":"{YOUR_CLIENT_SECRET}","audience":"https://forecast.convect.ai","grant_type":"client_credentials"}'
```

and get a response

```bash
{
  "access_token": "{RETURNED_TOKEN}",
  "token_type": "Bearer"
}
```

4. Now you can attach the token as specified in `access_token` field in the following API calls.


### Calling the API

* Attach the returned token in every header of the requests you send to a Convect™ API. For example, set `Authorization: Bearer {RETURNED_TOKEN}` in the header.

* Convect™ APIs also accept and return `json` type data, so you can set `Accept: application/json` and `Content-type: application/json` in your header as well.


### Example - Automated Forecasting

Here is an example of training and generating forecasts by calling the automated forecasting APIs.

=== "python"
    ```python
    {!> forecast-quickstart.py !}
    ```

=== "curl"
    ```bash
    {!> forecast-quickstart.sh !}
    ```











