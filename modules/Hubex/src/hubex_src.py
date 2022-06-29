from datetime import datetime
from typing import Any

from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF


def get_GoogleLogRegistrationPF(task: dict[str, Any]) -> GoogleLogRegistrationPF:
    assigned = task['assignedTo']
    d = (assigned['lastName'],
         assigned['firstName'][0] + "." if assigned['firstName'] else "",
         assigned['middleName'][0] + "." if assigned['middleName'] else "")

    object_name = task['asset'].get('host', {}).get('name')
    if not object_name:
        object_name = task['asset']["name"].splitlines()[0]

    return GoogleLogRegistrationPF(
        pf_number=str(task['number']),
        object_name=object_name,
        tech_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        factory_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        registration_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        location=task['location']['address'],
        customer_name=task['company']['name'],
        date_registration=datetime.fromisoformat(task['timesheet']['created']).strftime("%d.%m.%Y"),
        full_name=" ".join(d)
    )
