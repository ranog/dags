import json
import logging
import pathlib

import pendulum
import requests
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

logger = logging.getLogger(__name__)


def _get_pictures():
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                logger.info(f"Downloaded {image_url} to {target_file}")
            except requests.exceptions.MissingSchema as e:
                logger.error(f"Failed to download {image_url}: {e}")
            except requests.exceptions.ConnectionError as e:
                logger.error(f"Failed to download {image_url}: {e}")


with DAG(
    dag_id="01_download_rocket_launches",
    start_date=pendulum.today("UTC").add(days=-14),
    schedule=None,
):
    download_launches = BashOperator(
        task_id="download_launches",
        bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    )
    get_pictures = PythonOperator(
        task_id="get_pictures",
        python_callable=_get_pictures,
    )
    notify = BashOperator(
        task_id="notify",
        bash_command="echo There are now $(ls /tmp/images | wc -l) images in /tmp/images",
    )


download_launches >> get_pictures >> notify
