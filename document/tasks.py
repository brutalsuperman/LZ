from celery.decorators import task
from celery.utils.log import get_task_logger
import json


logger = get_task_logger(__name__)


@task(name="download_selected_documents")
def download_selected_documents_task(data):
    print('start')
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    print('end')
