[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://il-toti-sf-stage-explorer.streamlit.app/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=Streamlit&logoColor=white&style=flat)](https://www.streamlit.io/)
[![Snowflake](https://img.shields.io/badge/-Snowflake-29B5E8?logo=snowflake&logoColor=white)](https://www.snowflake.com/)

# Snowflake Stage Inspector
Stage Inspector helps you to analyse your Snowflake internal and external stages.

### Explorer
- Surf through your stages, check the parameters
- Get a list of files on your stages
- Even you can manage your stage files: upload, download or remove them

### Usage
- Overall size of your internal stages
- Getting familiar your biggest files
# Run this app
This app based on the excellent Streamlit framework. 
You can run it on the Streamlit Cloud 

## Create the virtual environment and install the packages
So, first create your favorite virtual env and download the necessary packages. Streamlit will install among the other packages in the requirement.txt.
```sh
pip install -r requirements.txt
```
## Snowflake connection
This app connects to a Snowflake account so you need to [create a trial Snowflake account](https://signup.snowflake.com/) if you want to test and don't have one yet.

You need to create a special file for your secrets. You can put it under your home directory:
```sh
~/.streamlit/secrets.toml
```
or create a folder/file in this project:
```sh
./.streamlit/secrets.toml
```

The content should be something like this:
```toml
[snowflake]
user = "_your_snowflake_username_"
password = "_your_snowflake_password_"
account = "_your_snowflake_account_identifier_"
role = "_your_snowflake_role_"
warehouse = "_your_snowflake_warehouse_"
database = "_your_snowflake_database_"
schema = "public"
```

You can find more explanation in the [Streamlit documentation](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management).

## Run your Streamlit locally
And now you can simply run your Streamlit application:
```
streamlit run Home.py
```


# About
We are [Infinite Lambda](https://infinitelambda.com/). 
We are happy to help you, feel free to contact us!.
Author: Gabor Toth.
