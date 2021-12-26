import re

RC3_SCHEDULE_REGEX = re.compile(r"https?:\/\/(rc3.world\/[0-9]{4}\/public_fahrplan|fahrplan\.events\.ccc\.de/rc3/[0-9]{4}/Fahrplan/)#(\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b)")


def message_is_rc3_schedule_link(message: str) -> bool:
    return bool(RC3_SCHEDULE_REGEX.match(message))
