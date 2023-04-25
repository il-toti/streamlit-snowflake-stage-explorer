[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://il-toti-sf-stage-explorer.streamlit.app/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?logo=Streamlit&logoColor=white&style=flat)](https://www.streamlit.io/)
[![Snowflake](https://img.shields.io/badge/-Snowflake-29B5E8?logo=snowflake&logoColor=white)](https://www.snowflake.com/)

# Snowflake Stage Inspector
Stage Inspector helps you to analyse your Snowflake internal and external stages.
You have two pages:
### Explorer
- Surf through your stages, check parameters
- Get a list of the files on your stages
- Even you can manage your stage files: upload, download or remove them (only internal stages)

### Usage
- Overall size of your internal stages
- Getting familiar your biggest files


## Installation
How can you run this app?
This app based on the excellent [Streamlit framework](https://streamlit.io/).
The best option is to run it on the [Streamlit Cloud](https://streamlit.io/cloud).

If you rather choose to run it locally here is your guide.

### Create the virtual environment and install the packages
So, first create your favorite virtual env and download the necessary packages. Streamlit will install among the other packages in the requirement.txt.
```sh
pip install -r requirements.txt
```
### Snowflake connection
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

### Run your Streamlit locally
And now you can simply run your Streamlit application:
```
streamlit run Home.py
```

## License
The content of this site is licensed under the [Apache 2.0](https://choosealicense.com/licenses/apache-2.0/) License.

## About Infinite Lambda
Infinite Lambda is a cloud and data consultancy. We build strategies, help organisations implement them and pass on the expertise to look after the infrastructure.

We are an Elite Snowflake Partner, a Platinum dbt Partner and two-times Fivetran Innovation Partner of the Year for EMEA.

Naturally, we love exploring innovative solutions and sharing knowledge, so go ahead and:

🔧 Take a look around our [Git](https://github.com/infinitelambda) </br>
✏️ Browse our [tech blog](https://infinitelambda.com/category/tech-blog/)

We are also chatty, so:</br>
#️⃣ Follow us on [LinkedIn](https://www.linkedin.com/company/infinite-lambda/) </br>
👋🏼 Or just [get in touch](https://infinitelambda.com/contacts/)

[<img src="https://raw.githubusercontent.com/infinitelambda/cdn/main/general/images/GitHub-About-Section-1080x1080.png" alt="About IL" width="500" height="500">](https://infinitelambda.com/)
