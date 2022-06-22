from datetime import datetime, timedelta


class NotPolite(Exception):
    def __init__(self, message, next_run: datetime = None):
        if next_run:
            message = f"{message} and next run is {next_run}"
        super().__init__(message)
        self.next_run = next_run


class Scheduler:
    def __init__(self, politeness_dict: dict):
        self._data = {key: {'next_run': datetime.utcnow(), 'interval': val} for key, val in
                      politeness_dict.items()}

    def is_polite(self, func_name):
        if func_name not in self._data:
            return True
        if self._data[func_name]['next_run'] < datetime.utcnow():
            self._data[func_name]['next_run'] = datetime.utcnow() + self._data[func_name]['interval']
            return True
        else:
            return False

    def update_politeness(self, politeness_dict):
        for func_name in politeness_dict:
            if func_name not in self._data:
                self._data[func_name] = {'next_run': datetime.utcnow(), 'interval': politeness_dict[func_name]}
            else:
                self._data[func_name]['interval'] = politeness_dict[func_name]


def politeness_checker(scheduler: Scheduler):
    def decorator(func):

        def wrapper(*args, **kwargs):
            if scheduler.is_polite(func.__name__):
                return func(*args, **kwargs)
            else:
                raise NotPolite(f"{func.__name__} is not polite")

        return wrapper

        # return functools.update_wrapper(wrapper, func)

    return decorator


if __name__ == '__main__':
    pass
