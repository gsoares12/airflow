# airflow

Projeto de Engenharia de Dados que usa o **Apache Airflow 3** como orquestrador de tarefas. Ele roda localmente com Docker Compose (CeleryExecutor + PostgreSQL + Redis). O deploy das DAGs é contínuo, feito por um **GitHub Actions self-hosted runner**.

## Stack

| Componente | Versão / Imagem |
|---|---|
| Apache Airflow | `apache/airflow:3.3.2` |
| Executor | CeleryExecutor |
| Banco de metadados | PostgreSQL 16 |
| Broker | Redis 7.2 |
| CI/CD | GitHub Actions (runner self-hosted) |

## Estrutura

```
.
├── .github/workflows/deploy.yml   # Pipeline de deploy das DAGs
├── dags/                          # DAGs do Airflow
│   ├── pipeline_teste.py
│   └── pipeline_email.py
├── plugins/                       # Plugins customizados (vazio por enquanto)
├── config/                        # airflow.cfg (gerado, não versionado)
├── logs/                          # Logs de execução (não versionado)
├── docker-compose.yaml            # Definição do ambiente Airflow
└── .env                           # Variáveis de ambiente (não versionado)
```

## DAGs

| DAG | Arquivo | Agendamento | Descrição |
|---|---|---|---|
| `pipeline_teste` | [dags/pipeline_teste.py](dags/pipeline_teste.py) | `@daily` | Pipeline simples `inicio >> executar_funcao_python >> fim`, usada para validar o ambiente e o CI/CD. |
| `dag_teste_smtp_email` | [dags/pipeline_email.py](dags/pipeline_email.py) | Manual | Envia um e-mail de notificação via SMTP com o `EmailOperator`. O destinatário vem da Variable `EMAIL_SEND`. |

> As DAGs são criadas **pausadas** (`DAGS_ARE_PAUSED_AT_CREATION=true`). Ative-as pela interface web.

## Pré-requisitos

- Docker e Docker Compose v2
- No mínimo 4 GB de RAM, 2 CPUs e 10 GB de disco livres para o Docker

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
AIRFLOW_UID=1000              # saída de `id -u`

# Chave de criptografia das connections/variables
FERNET_KEY=

# SMTP (porta 587 com STARTTLS)
SMTP_HOST=smtp.exemplo.com
SMTP_USER=usuario@exemplo.com
SMTP_PASSWORD=
SMTP_PORT=587
SMTP_MAIL_FROM=usuario@exemplo.com

# Variables do Airflow (expostas como AIRFLOW_VAR_<NOME>)
AIRFLOW_VAR_EMAIL_SEND=destinatario@exemplo.com
```

Para gerar uma `FERNET_KEY`:

```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

O `docker-compose.yaml` usa essas variáveis de SMTP para montar a connection `smtp_default`, que é a usada pelo `EmailOperator` no Airflow 3.

> A DAG `dag_teste_smtp_email` lê `EMAIL_SEND` quando o arquivo é carregado. Se a variável não existir, a DAG aparece com erro de importação na interface.

## Executando

```bash
# Inicializa o banco e cria o usuário admin (apenas na primeira vez)
docker compose up airflow-init

# Sobe todos os serviços
docker compose up -d
```

Acesse a interface em **http://localhost:8080**. O login padrão é `airflow` / `airflow`; para trocar, defina `_AIRFLOW_WWW_USER_USERNAME` e `_AIRFLOW_WWW_USER_PASSWORD` no `.env`.

Comandos úteis:

```bash
docker compose ps                         # status dos serviços
docker compose logs -f airflow-scheduler  # logs do scheduler
docker compose --profile flower up -d     # Flower (monitor do Celery) em http://localhost:5555
docker compose down                       # para o ambiente
docker compose down -v                    # para e remove o volume do Postgres
```

## CI/CD

O workflow [.github/workflows/deploy.yml](.github/workflows/deploy.yml) roda a cada push na branch `main`, em um runner **self-hosted** instalado no próprio servidor. Ele faz checkout do repositório e sincroniza a pasta `dags/` com o diretório montado pelo Docker Compose:

```bash
rsync -av --delete dags/ /home/debian-server/airflow/dags/
```

O dag-processor do Airflow detecta as alterações automaticamente, sem precisar reiniciar os containers.

### Configurando o runner

1. No GitHub, acesse **Settings → Actions → Runners → New self-hosted runner** e siga as instruções para Linux x64.
2. Instale o runner em `actions-runner/` (a pasta é ignorada pelo Git).
3. Para rodar o runner como serviço:
   ```bash
   cd actions-runner
   sudo ./svc.sh install
   sudo ./svc.sh start
   ```

> O caminho de destino do `rsync` está fixo no workflow. Se o projeto estiver em outro diretório, ajuste o `deploy.yml`.

## Aviso

Este `docker-compose.yaml` é baseado na configuração oficial do Airflow para **desenvolvimento local** e não é indicado para produção.
