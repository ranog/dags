import datetime
import pathlib

import pandas as pd
import pendulum
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator


def _calculate_stats(input_path, output_path):
    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()
    pathlib.Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)


with DAG(
    dag_id="02_unscheduled",
    schedule=datetime.timedelta(days=3),
    start_date=pendulum.datetime(2025, 6, 4),
    end_date=pendulum.datetime(2025, 12, 4),
):
    fetch_events = BashOperator(
        task_id="fetch_events",
        bash_command=(
            "mkdir -p /tmp/data && curl -o /tmp/data/events.json http://events-api:8081/events/latest"
        ),
    )
    calculate_stats = PythonOperator(
        task_id="calculate_stats",
        python_callable=_calculate_stats,
        op_kwargs={
            "input_path": "/tmp/data/events.json",
            "output_path": "/tmp/data/event_stats.csv",
        },
    )


fetch_events >> calculate_stats
