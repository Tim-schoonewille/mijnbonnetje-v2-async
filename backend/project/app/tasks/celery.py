from celery import Celery  # type: ignore


def create_celery_application(task_module: str) -> Celery:
    application = Celery(task_module)
    application.config_from_object("app.tasks.celeryconfig")
    return application


celery_app = create_celery_application("app.tasks.tasks")


@celery_app.task
def add(x: int, y: int) -> int:
    return x + y


if __name__ == "__main__":
    celery_app.start()
