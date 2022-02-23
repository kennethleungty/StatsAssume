# ==========================
# Module: Enums - Task Type
# Author: Kenneth Leung
# Last Modified: 02 Jan 2022
# ==========================
import enum


class TaskType(enum.IntEnum):
    linear_regression = 1
    binary_logistic_regression = 2
    multinomial_logistic_regression = 3

    @staticmethod
    def from_str(task_type: str):
        if task_type == 'linear regression':
            return TaskType.linear_regression
        elif task_type == 'binary logistic regression':
            return TaskType.binary_logistic_regression
        elif task_type == 'multinomial logistic regression':
            return TaskType.multinomial_logistic_regression
        else:
            raise ValueError(f'Specified task type of {task_type} is invalid')

    @staticmethod
    def list_str():
        return ['linear regression', 'binary logistic regression', 'multinomial logistic regression']
