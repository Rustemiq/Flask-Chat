class _SingletonWrapper:
    def __init__(self, cls):
        self.__wrapped__ = cls  # Оригинальный класс
        self._instance = None   # Здесь будет храниться экземпляр класса

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance

def singleton(cls):
    """
    Декоратор для класса, реализующий синглтон.
    """
    return _SingletonWrapper(cls)