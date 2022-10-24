from flask_sse import sse


def signal_new_log_entry(log_level: str, log_message: str, logger_name: str, date: str, payload: dict):
    sse.publish(
        {
            "log_level_name": log_level,
            "log_message": log_message,
            "logger_name": logger_name,
            "created": date,
            "payload": { k: v for k, v in payload.items() if k != "_id" }
        },
        type="new_log_entry"
    )
