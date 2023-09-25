from celery.schedules import crontab  # type: ignore


broker_url = "pyamqp://admin:admin@localhost"
result_backend = "rpc://"
result_expires = 3600
include = ["app.tasks.tasks"]
timezone = "Europe/Berlin"
beat_schedule = {
    "mock-user-activities": {
        "task": "app.tasks.tasks.task_mock_user_activities",
        "schedule": crontab(minute="*/15"),
    },
    "update-subscription-status": {
        "task": "app.tasks.tasks.task_update_subscription_active_status",
        "schedule": crontab(minute="*/5"),
    },
    "update-proxy-list-to-cache": {
        "task": "app.tasks.tasks.task_update_proxy_list_to_cache",
        "schedule": crontab(minute="*/10"),
    }
}


# "log-traffic": {
#     "task": "app.tasks.tasks.task_log_traffic",
#     "schedule": crontab(minute=0, hour=0),
# },
