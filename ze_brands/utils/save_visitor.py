# Standard Libraries
import uuid

# Third-party Libraries
import redis as rd
from django.utils import timezone


def get_data(info) -> str:
    return str(
        {
            "accept_language": info.context.META.get(
                "HTTP_ACCEPT_LANGUAGE", ""
            ),
            "user_agent": info.context.META.get("HTTP_USER_AGENT", ""),
            "ip_address": info.context.META.get("REMOTE_ADDR", ""),
            "created_at": timezone.now(),
            "visit_id": str(uuid.uuid4()),
        }
    )


def save_date(info) -> None:
    try:
        redis = rd.Redis(host="0.0.0.0", port=6379, decode_responses=True)
        redis.set("Visit", get_data(info))
    except Exception as exp:
        print(f"An error occurred: {exp}")
