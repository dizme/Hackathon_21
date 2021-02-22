from datetime import datetime, timezone
import binascii

YYYY_MM_DD_FORMAT = "%Y-%m-%d"
DD_MM_YYYY_FORMAT = "%d-%m-%Y"


def datetime_now() -> datetime:
    """Timestamp in UTC."""
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def convert_date(input_date: str, from_format: str, to_format: str):
    try:
        if input_date:
            date_time_obj = datetime.strptime(input_date, from_format)
            return date_time_obj.strftime(to_format)
        else:
            return "N/A"
    except ValueError as ve:
        return "N/A"


def convert_binary_image_to_base64_string(content_data):
    content_data_base64 = str(binascii.b2a_base64(content_data).decode("utf-8"))
    if content_data_base64.endswith('\n'):
        content_data_base64 = content_data_base64[:-1]

    return content_data_base64


def is_filled(field):
    return field is not None and field != "" and field != "N/A"

