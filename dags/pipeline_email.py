from datetime import datetime
from airflow import DAG
from airflow.operators.email import EmailOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'guilherme',
    'start_date': datetime(2026, 1, 1),
    'retries': 0
}

with DAG(
    'dag_teste_smtp_email',
    default_args=default_args,
    schedule_interval=None, # Disparo apenas manual na interface web
    catchup=False,
) as dag:

    enviar_email = EmailOperator(
        task_id='enviar_notificacao',
        to='gsoaress@gmail.com',
        subject='Alerta do Airflow: {{ dag.dag_id }}',
        html_content='<h3>O fluxo executou com sucesso!</h3>',
    )
