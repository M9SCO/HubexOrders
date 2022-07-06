from datetime import datetime
from typing import Any

from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF


def get_GoogleLogRegistrationPF(task: dict[str, Any], task_id: int, asset: str) -> GoogleLogRegistrationPF:
    assigned = task['assignedTo']
    d = (assigned['lastName'],
         assigned['firstName'][0] + "." if assigned['firstName'] else "",
         assigned['middleName'][0] + "." if assigned['middleName'] else "")

    erp_id = asset.get('erpID')
    if not erp_id:
        erp_id = "б/н"

    return GoogleLogRegistrationPF(
        pf_number=str(task['number']),
        task_id=task_id,
        erp_id=erp_id,
        object_name=task['asset']["name"].splitlines()[0],
        tech_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        factory_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        registration_object_number="б/н",  # ToDo Поправить эту хуйню. не всегда статика б/н
        location=task['location']['address'],
        customer_name=task['company']['name'],
        date_registration=datetime.fromisoformat(task['timesheet']['created']).strftime("%d.%m.%Y"),
        full_name=" ".join(d)
    )
