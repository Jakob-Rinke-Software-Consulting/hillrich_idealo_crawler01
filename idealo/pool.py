import threading
	
def synchronized(func):
    func.__lock__ = threading.Lock()
    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func

class SyncedIdealoPool:

    def __init__(self, categories):
        self.categories = categories

    @synchronized
    def next(self, driver):
        if not self.categories or len(self.categories) == 0:
            return None

        # get the next crawler
        return self.categories.pop(0)
        

