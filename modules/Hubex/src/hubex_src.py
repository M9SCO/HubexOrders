from datetime import datetime
from typing import Any

from modules.Google.modules.GoogleLogRegistrationPF import GoogleLogRegistrationPF


def full_name(assigned: dict, default: str = "Нет исполнителя") -> str:
    if not assigned:
        return default
    d = (assigned['lastName'],
         assigned['firstName'][0] + "." if assigned['firstName'] else "",
         assigned['middleName'][0] + "." if assigned['middleName'] else "")
    return " ".join(d)


def get_attribute(attributes: dict, attr_name: str, default: str = "б/н"):
    if attributes is None:
        return default
    for attribute in attributes:
        name = attribute.get('attribute', {}).get('name')
        if name == attr_name:
            return attribute.get('value') or default
    return default


def get_GoogleLogRegistrationPF(task: dict[str, Any], task_id: int, asset: dict,
                                attributes: dict) -> GoogleLogRegistrationPF:
    assigned = task.get('assignedTo')
    erp_id = asset.get('erpID') or "б/н"

    return GoogleLogRegistrationPF(
        pf_number=str(task['number']),
        task_id=task_id,
        erp_id=erp_id,
        object_name=task['asset']["name"].splitlines()[0],
        tech_object_number=get_attribute(attributes, "Заводской номер объекта"),
        factory_object_number=get_attribute(attributes, "Технологический номер объекта"),
        registration_object_number=get_attribute(attributes, "Регистрационный номер объекта"),
        location=task['location']['address'],
        customer_name=task['company']['name'],
        date_registration=datetime.fromisoformat(task['timesheet']['created']).strftime("%d.%m.%Y"),
        full_name=full_name(assigned)
    )
