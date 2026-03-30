# Telegram Bot Enterprise Boilerplate (aiogram 3.x)

**Production-ready, strictly structured boilerplate** for developing scalable Telegram bots based on `aiogram 3.x`. The architecture follows **Clean Architecture** principles, utilizing the **Unit of Work (UoW)** pattern to encapsulate database transactions. **Zero business logic in handlers** — all logic is isolated in services.

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4+-blue.svg)](https://docs.aiogram.dev/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-green.svg)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)

---

## 🎯 Key Features

- ✅ **Clean Architecture** — strict separation of concerns (handlers → services → repositories)
- ✅ **Unit of Work Pattern** — transactional consistency across database operations
- ✅ **Zero Business Logic in Handlers** — handlers are routing-only, logic resides in services
- ✅ **Async SQLAlchemy 2.0** — modern async ORM with type safety
- ✅ **Background Tasks** — Taskiq integration for long-running operations
- ✅ **Production Docker Setup** — multi-stage builds with health checks
- ✅ **i18n Ready** — Fluent-based localization with validation scripts
- ✅ **Middleware Stack** — Database injection, anti-spam, i18n support
- ✅ **Type Safety** — Pydantic settings and strict typing throughout

---

## 🛠 Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | [aiogram 3.4+](https://docs.aiogram.dev/) |
| **Database** | PostgreSQL 15 + [asyncpg](https://magicstack.github.io/asyncpg/) |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async) |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Cache/Broker** | [Redis 7](https://redis.io/) |
| **Background Worker** | [Taskiq](https://taskiq-python.github.io/) |
| **Configuration** | [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) |
| **Localization** | [Fluent](https://projectfluent.org/) + custom validation scripts |
| **Containerization** | Docker + Docker Compose |

---

## 📂 Project Structure

```text
.
├── alembic/                    # Database migrations
│   └── env.py                  # Async Alembic configuration
├── bot/                        # Main application package
│   ├── core/                   # Configuration and utilities
│   │   ├── config.py           # Pydantic settings (DATABASE_URL, REDIS_URL, etc.)
│   │   └── logger.py           # Logging configuration
│   ├── database/               # Data layer
│   │   ├── base.py             # SQLAlchemy Base
│   │   ├── session.py          # Async session factory
│   │   ├── uow.py              # Unit of Work implementation
│   │   ├── models/             # SQLAlchemy models
│   │   │   └── user.py         # User model example
│   │   └── repositories/       # Repository pattern
│   │       └── user.py         # UserRepository with CRUD operations
│   ├── handlers/               # Telegram handlers (routing only)
│   │   ├── common.py           # /start, /help handlers
│   │   └── errors.py           # Global error handler
│   ├── middlewares/            # Middleware stack
│   │   ├── database.py         # UoW injection middleware
│   │   ├── i18n.py             # Localization middleware
│   │   └── throttling.py       # Anti-spam middleware
│   ├── services/               # Business logic layer
│   │   └── ai_connector.py     # AI integration abstraction (OpenAI, etc.)
│   ├── tasks/                  # Background tasks
│   │   └── broker.py           # Taskiq broker + example task
│   └── main.py                 # Application entry point
├── scripts/                    # Development utilities
│   ├── check_i18n.py           # Validate translation coverage
│   └── auto_fix_i18n.py        # Auto-sync missing translation keys
├── logs/                       # Application logs (git-ignored)
├── .github/                    # CI/CD workflows (optional)
│   └── workflows/
├── alembic.ini                 # Alembic configuration
├── docker-compose.yml          # Development infrastructure
├── Dockerfile                  # Multi-stage production build
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
└── .gitignore                  # Git exclusions
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)
- Redis 7+ (or use Docker)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd telegram-bot-boilerplate
```

### 2. Create Environment File

```bash
cp .env.example .env
```

**Edit `.env` with your credentials:**

```env
# Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bot_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Optional: AI Integration
OPENAI_API_KEY=sk-...
```

### 3. Run with Docker (Recommended)

```bash
# Start all services (bot, worker, postgres, redis)
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop services
docker-compose down
```

### 4. Local Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start the bot
python -m bot.main

# Start the worker (in another terminal)
taskiq worker bot.tasks.broker:broker
```

---

## 🏗 Architecture Principles

### 1. **Clean Architecture Layers**

```
Handlers (Transport)
    ↓
Services (Business Logic)
    ↓
Repositories (Data Access)
    ↓
Models (Database)
```

**Example Flow:**
```python
# ❌ WRONG: Business logic in handler
@router.message(Command("start"))
async def cmd_start(message: Message, uow: SQLAlchemyUoW):
    user = await uow.users.get_by_telegram_id(message.from_user.id)
    if not user:
        user = User(telegram_id=message.from_user.id, ...)
        uow.users.add(user)
        await uow.commit()
    await message.answer("Welcome!")

# ✅ CORRECT: Handler delegates to service
@router.message(Command("start"))
async def cmd_start(message: Message, uow: SQLAlchemyUoW):
    await user_service.register_or_update(message.from_user, uow)
    await message.answer("Welcome!")
```

### 2. **Unit of Work Pattern**

All database operations are wrapped in a **single transaction**:

```python
async with SQLAlchemyUoW(async_session_maker) as uow:
    user = await uow.users.get_by_telegram_id(telegram_id)
    user.balance += 100
    await uow.commit()  # All changes committed atomically
```

### 3. **Dependency Injection**

Middleware automatically injects dependencies into handlers:

```python
@router.message(Command("profile"))
async def show_profile(
    message: Message,
    uow: SQLAlchemyUoW,      # Injected by DatabaseMiddleware
    _get: Callable,           # Injected by I18nMiddleware
    locale: str               # Injected by I18nMiddleware
):
    user = await uow.users.get_by_telegram_id(message.from_user.id)
    await message.answer(_get("profile-greeting", name=user.full_name))
```

---

## 📦 Database Management

### Creating Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add user premium field"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

### Repository Pattern Example

```python
# bot/database/repositories/user.py
class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    def add(self, user: User) -> None:
        self.session.add(user)
```

---

## 🌍 Internationalization (i18n)

### Structure

```
bot/locales/
├── en/
│   └── LC_MESSAGES/
│       └── messages.ftl
├── uk/
│   └── LC_MESSAGES/
│       └── messages.ftl
└── ru/
    └── LC_MESSAGES/
        └── messages.ftl
```

### Translation File Format (Fluent)

```ftl
# bot/locales/en/LC_MESSAGES/messages.ftl
welcome-message = Welcome, {$name}!
balance-info = 
    Your current balance: {$balance} coins.
    Last updated: {$date}
```

### Validation Scripts

```bash
# Check for missing translations
python scripts/check_i18n.py

# Auto-sync missing keys from translations.json
python scripts/auto_fix_i18n.py
```

**Output Example:**
```
❌ Missing translation keys found:
[uk]: welcome-new-user, settings-saved
[ru]: welcome-new-user
```

---

## ⚙️ Background Tasks

### Defining Tasks

```python
# bot/tasks/broker.py
from taskiq_redis import ListQueueBroker
from bot.core.config import settings

broker = ListQueueBroker(url=settings.redis_url)

@broker.task
async def send_newsletter(user_ids: list[int], text: str) -> None:
    # Heavy task logic here
    for user_id in user_ids:
        await bot.send_message(user_id, text)
```

### Triggering Tasks

```python
# From a handler
await send_newsletter.kiq(user_ids=[123, 456], text="News update!")
```

### Running Worker

```bash
# Development
taskiq worker bot.tasks.broker:broker

# Production (Docker)
docker-compose up worker
```

---

## 🐳 Docker Configuration

### Multi-Stage Dockerfile

The project uses a **two-stage build** for optimized image size:

1. **Builder Stage** — compiles dependencies
2. **Runtime Stage** — minimal production image

**Key Features:**
- Non-root user (`appuser`)
- No cache bloat
- Separate volumes for logs
- Health checks for PostgreSQL and Redis

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| `postgres` | 5432 | PostgreSQL 15 with health checks |
| `redis` | 6379 | Redis 7 for caching and broker |
| `bot` | — | Main bot process |
| `worker` | — | Background task worker |

---

## 🔒 Security Best Practices

- ✅ **Environment Variables** — all secrets in `.env` (git-ignored)
- ✅ **Non-Root Container** — Docker runs as `appuser`
- ✅ **Anti-Spam Middleware** — rate limiting to prevent abuse
- ✅ **Input Validation** — Pydantic models for all configs
- ✅ **SQL Injection Protection** — parameterized queries via SQLAlchemy
- ✅ **Error Handling** — global error handler prevents leaking stack traces

---

## 📝 Development Guidelines

### Adding a New Handler

1. **Create handler in** `bot/handlers/`:
```python
# bot/handlers/shop.py
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("shop"))
async def show_shop(message: types.Message, uow: SQLAlchemyUoW):
    # Delegate to service
    items = await shop_service.get_available_items(uow)
    await message.answer(format_shop_items(items))
```

2. **Register router in** `bot/main.py`:
```python
from bot.handlers import common, shop

dp.include_routers(common.router, shop.router)
```

### Adding a New Service

```python
# bot/services/shop_service.py
async def get_available_items(uow: SQLAlchemyUoW) -> list[Item]:
    """Business logic: fetch items with stock > 0."""
    return await uow.items.get_in_stock()
```

### Adding a New Model

```python
# bot/database/models/item.py
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.base import Base

class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]
    stock: Mapped[int] = mapped_column(default=0)
```

**Then create migration:**
```bash
alembic revision --autogenerate -m "Add Item model"
alembic upgrade head
```

---

## 🧪 Testing (TODO)

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=bot tests/
```

---

## 📊 Monitoring & Logging

### Log Configuration

Logs are stored in `logs/` directory:

```python
# bot/core/logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/bot.log"),
        logging.StreamHandler()
    ]
)
```

### Docker Logs

```bash
# Real-time logs
docker-compose logs -f bot

# Last 100 lines
docker-compose logs --tail=100 bot
```

---

## 🚀 Production Deployment

### Environment Variables

Ensure these are set in production `.env`:

```env
BOT_TOKEN=<production_token>
POSTGRES_HOST=postgres
POSTGRES_PASSWORD=<strong_password>
REDIS_HOST=redis
LOG_LEVEL=WARNING
```

### Deployment Checklist

- [ ] Set strong `POSTGRES_PASSWORD`
- [ ] Restrict `ADMIN_IDS` to trusted users
- [ ] Enable Docker restart policies (`restart: always`)
- [ ] Configure log rotation
- [ ] Set up monitoring (optional: Prometheus + Grafana)
- [ ] Run migrations before deployment: `alembic upgrade head`
- [ ] Test rollback procedure: `alembic downgrade -1`

### Zero-Downtime Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Apply migrations (if needed)
docker-compose exec bot alembic upgrade head
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

**Code Style:**
- Follow PEP 8
- Use type hints everywhere
- Add docstrings to public methods
- Keep handlers thin, services fat

---

## 📄 License

This project is licensed under the MIT License. See `LICENSE` file for details.

---

## 🙏 Acknowledgments

- [aiogram](https://github.com/aiogram/aiogram) — modern Telegram Bot API framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — powerful ORM
- [Taskiq](https://github.com/taskiq-python/taskiq) — distributed task queue
- [Fluent](https://projectfluent.org/) — natural-sounding translations

---

**Built with ❤️ using Clean Architecture principles**