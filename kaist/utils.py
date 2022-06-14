import threading
import ctypes

def input_yes_no_question(prompt, default=False):
    """Input yes or no question"""
    true_false_to_str = {
        True: 'y',
        False: 'n'
    }
    
    while True:
        print(f"{prompt} (Press ENTER for default: {true_false_to_str[default]}): ", end='')
        answer = input("Answer [y/n]: ").lower()
        if any(answer == f for f in ["yes", 'y', '1', 'ye', 'yep', 'yeah']):
            return True
        elif any(answer == f for f in ['no', 'n', '0', 'nope']):
            return False
        elif answer == '':
            return default
        else: 
            print("Answer with yes or no: ", end='')
            continue


def input_with_default(prompt, default, yes_no_question=False):
    """Input with default"""
    if yes_no_question:
        return input_yes_no_question(prompt, default)
    print(f"{prompt} (Press ENTER for default: {default}): ", end='')
    return input() or default


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ThreadWithException(threading.Thread):
    """Thread class throwing an exception when stopped"""
    def __init__(self, name, target, args):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target
        self.args = args
             
    def run(self):
        self.target(self.args)

    def get_id(self):
 
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
  
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
