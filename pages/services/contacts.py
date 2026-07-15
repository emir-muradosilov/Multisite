from core.models import SiteSettings


def get_city_contacts(city):

    settings = SiteSettings.load()

    tenant = getattr(city, "tenant_profile", None)

    if tenant and tenant.is_active:

        return {
            "company_name": tenant.company_name or settings.site_name,
            "address": tenant.address or city.address,
            "phone": tenant.phone or city.phone or settings.default_phone,
            "phone_secondary": tenant.phone_secondary,
            "working_hours": tenant.working_hours or "Пн-Пт: 09:00 — 18:00",
            "email": tenant.email,
            "telegram": tenant.telegram,
            "whatsapp": tenant.whatsapp,
            "max": tenant.max,
        }

    return {
        "company_name": settings.site_name,
        "address": city.address,
        "phone": city.phone or settings.default_phone,
        "phone_secondary": "",
        "working_hours": "Пн-Пт: 09:00 — 18:00",
        "email": "",
        "telegram": "",
        "whatsapp": "",
        "max": "",
    }