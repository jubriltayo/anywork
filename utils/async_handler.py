from django.conf import settings

def run_task(task, *args, **kwargs):
    if settings.USE_ASYNC_TASKS:
        return task.delay(*args, **kwargs)
    return task(*args, **kwargs)