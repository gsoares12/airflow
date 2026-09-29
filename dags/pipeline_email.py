from airflow import DAG
from airflow.operators.email import EmailOperator
from datetime import datetime

default_args = {
    'owner': 'guilherme',
    'start_date': datetime(2026, 1, 1),
    'retries': 0
}

with DAG(
    'dag_teste_smtp_email',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['teste', 'email'],
) as dag:

    enviar_email_teste = EmailOperator(
        task_id='enviar_email_teste',
        to='gsoaressh@gmail.com',
        subject='Airflow funcionando! - Notificação de Teste',
        html_content="""
        <h3>Configuração Concluída com Sucesso!</h3>
        <p>Este e-mail valida que o Airflow está lendo o arquivo <b>.env</b> de forma segura através do Docker Compose.</p>
        <p><b>Data do disparo:</b> {{ ds }}</p>
        """
    )
