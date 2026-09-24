from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

# Função de teste que será executada por uma task
def minha_funcao_teste():
    print("Olá! Esta é uma execução de teste no Airflow.")
    return "Sucesso"

# Argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definição da DAG
with DAG(
    dag_id='pipeline_teste',
    default_args=default_args,
    description='Uma pipeline simples de teste',
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['teste', 'exemplo'],
) as dag:

    # Tarefa de início (vazia)
    inicio = EmptyOperator(task_id='inicio')

    # Tarefa que executa a função Python criada acima
    tarefa_python = PythonOperator(
        task_id='executar_funcao_python',
        python_callable=minha_funcao_teste,
    )

    # Tarefa de fim (vazia)
    fim = EmptyOperator(task_id='fim')

    # Definindo a ordem de execução das tarefas
    inicio >> tarefa_python >> fim
