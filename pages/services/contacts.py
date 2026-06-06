def get_city_contacts(city):

    tenant = getattr(
        city,
        'tenant_profile',
        None
    )

    if tenant and tenant.is_active:

        return {
            'company_name': tenant.company_name,
            'address': tenant.address,
            'phone': tenant.phone,
            'phone_secondary': tenant.phone_secondary,
            'working_hours': tenant.working_hours,
            'email': tenant.email,
        }

    return {
        'company_name': city.name,
        'address': city.address,
        'phone': city.phone,
        'phone_secondary': '',
        'working_hours': 'Пн-Пт: 09:00 — 18:00',
        'email': '',
    }