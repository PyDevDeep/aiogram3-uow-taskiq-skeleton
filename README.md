# Telegram Bot Enterprise Boilerplate (aiogram 3.x)

This is a strictly structured, production-ready boilerplate for developing scalable Telegram bots based on `aiogram 3.x`. The architecture follows Clean Architecture principles, utilizing the Unit of Work (UoW) pattern to encapsulate database transactions. There is zero business logic in the transport layer (handlers).

## 🛠 Tech Stack

* **Framework:** [aiogram 3.x](https://docs.aiogram.dev/)
* **Database:** PostgreSQL + [asyncpg](https://magicstack.github.io/asyncpg/current/)
* **ORM & Migrations:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async) + [Alembic](https://alembic.sqlalchemy.org/)
* **Cache & Broker:** [Redis](https://redis.io/)
* **Background Worker:** [Taskiq](https://taskiq-python.github.io/)
* **Containerization:** Docker & Docker Compose
* **Localization (i18n):** Project-specific scripts + Fluent (ready)

## 📂 Project Structure

```text
.
├── alembic/                # Alembic configuration and migration scripts
├── bot/                    # Root application package
│   ├── core/               # Configuration (pydantic-settings), logging
│   ├── database/           # Models, Repositories, UoW, DB connection
│   ├── handlers/           # Telegram handlers (routing only, no business logic)
│   ├── middlewares/        # AntiSpam, Database/UoW Injector, i18n
│   ├── services/           # Business logic (e.g., AI connectors)
│   ├── tasks/              # Background tasks (Taskiq)
│   └── main.py             # Entry point, bot and dispatcher initialization
├── scripts/                # Utilities (deploy, i18n validation)
├── logs/                   # Directory for logs (git-ignored)
├── alembic.ini             # Alembic config
├── docker-compose.yml      # Base infrastructure (dev)
├── docker-compose.prod.yml # Production overrides
├── Dockerfile              # Multi-stage build for bot and worker
└── requirements.txt        # Project dependencies