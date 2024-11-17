import asyncio
import sys
import logging
import service.queueService as qs
from bootstrap import bootstrap, BootstrapArgs
from service.queueService.common.task.ActivationTask.UsernamePasswordActivationTask import BBAEActivationTask

TASK_HANDLER_REGISTRY = {}


def register_handler(task_class):
    def decorator(func):
        TASK_HANDLER_REGISTRY[task_class] = func
        return func

    return decorator


@register_handler(qs.common.task.TaskType.Deactivation)
def handle_deactivation_task(task: BBAEActivationTask) -> None:
    logger.debug("Handling ActivationTask")
    logger.debug(f"Task: {task}")


@register_handler(qs.common.task.TaskType.Activation)
def handle_activation_task(task: BBAEActivationTask) -> None:
    logger.debug("Handling ActivationTask")
    logger.debug(f"Task: {task}")


logger = logging.getLogger("Trading-Automation")
logger.setLevel(logging.DEBUG)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)
errHandler = logging.FileHandler("error.log")

stdoutHandler.setLevel(logging.DEBUG)
errHandler.setLevel(logging.ERROR)

fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)
stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)

logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)


def handler(task: qs.common.task.BaseTask, ack: qs.common.types.AckFunction) -> None:
    logger.debug("Processing task...")
    logger.debug(f"Task type: {task.task_type}, Id: {task.task_id}")

    handler_function = TASK_HANDLER_REGISTRY.get(task.task_type)

    if not handler_function:
        logger.error("Unknown task type. No specific handler available.")
        return

    handler_function(task)
    logger.info(f"Task id: {task.task_id} done successfully")
    ack()


if __name__ == '__main__':
    asyncio.run(bootstrap(BootstrapArgs(host="localhost", port=5672, handler_function=handler, logger=logger)))