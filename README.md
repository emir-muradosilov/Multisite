# Multisite
CMS-платформа на Django с динамической мультигородской (SaaS/Multitenancy) SEO-архитектурой для продвижения строительных услуг по всей России. Проект полностью упакован в Docker и развернут на боевом сервере.
**Демо сайта:** https://diamond-rezka.ru
## SEO Architecture

## 🚀 Ключевые фичи и бизнес-логика
* **Динамический мульти-чекаут (SEO Architecture):** Шаблонная генерация посадочных страниц (`ServiceTemplate` -> `ServicePage`) для сотен городов. Позволяет динамически подставлять топонимы, цены и контакты под выбранный регион без дублирования кода и раздувания БД.
* **Кастомная лидогенерация:** Модуль заявок с валидацией, обработкой персональных данных и сохранением контекста (город/услуга), откуда пришел пользователь.
* **Многоуровневая структура:** Разделение логики на изолированные приложения (`cities`, `districts`, `leads`, `pages`, `seo`, `tenants`) для поддержки чистоты архитектуры (High Cohesion / Low Coupling).

## 🛠 Стек технологий
* **Backend:** Python 3.11+, Django, Django ORM
* **Database:** PostgreSQL
* **DevOps & Infra:** Docker, Docker Compose, Nginx (как reverse-proxy), Gunicorn, Linux (Ubuntu/Debian)
* **Frontend:** HTML5, CSS3, JavaScript (интеграция готовых шаблонов через Django Templates)

## 🐳 Архитектура развертывания (DevOps)
Проект развернут на VPS и полностью изолирован в Docker-контейнерах:
* `web` — Django-приложение, запущенное через WSGI-сервер Gunicorn.
* `nginx` — раздача статики/медиа и проксирование запросов к Django.

The project uses template-based SEO page generation.

Structure:

ServiceTemplate
→ generate_pages command
→ ServicePage

Advantages:

- scalable multi-city SEO
- centralized SEO management
- automatic page generation
- support for hundreds of cities
- easy regeneration of SEO content
