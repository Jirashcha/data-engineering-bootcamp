from airflow.utils import timezone

from cosmos import DbtDag, ProjectConfig, ProfileConfig
from cosmos.profiles import GoogleCloudServiceAccountDictProfileMapping

"""
#### Connections
1. **bigquery_dbt**
    [
        conn_type=`Google Cloud`,
        keyfile_json=`YOUR_SERVICE_ACCOUNT_JSON`,
        project_id=`YOUR_PROJECT_ID`
    ]
"""

profile_config = ProfileConfig(
    profile_name="greenery_dbt_project",
    target_name="dev",
    profile_mapping=GoogleCloudServiceAccountDictProfileMapping(
        conn_id="example_bigquery",
        profile_args={"schema": "dbt_jirashcha",
                      "location": "asia-southeast1"},
    ),
)

example_dbt_project = DbtDag(
    dag_id="greenery_dbt_dag",
    schedule_interval="@daily",
    start_date=timezone.datetime(2023, 3, 17),
    catchup=False,
    project_config=ProjectConfig("/opt/airflow/dbt/greenery"),
    profile_config=profile_config,
    tags=["DEB", "Skooldio"],

    concurrency=1,
)