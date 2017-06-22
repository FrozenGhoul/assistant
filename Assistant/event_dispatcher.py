from pydispatch import dispatcher


class EventDispatcher:
    def __init__(self):
        self.sleep_status = False
        self.should_quit = False

    def close(self):
        return self.sleep_status

    def sleep(self, sender):
        self.sleep_status = True
        print("The virtual assistant is going to sleep by %s method" % sender)
        return self

    def quit(self, sender):
        self.should_quit = True
        print("The virtual assistant is being quit by %s method" % sender)

    def add(self, handle_name):
        handle_event = getattr(self, handle_name)
        dispatcher.connect(handle_event, signal=handle_name, sender=dispatcher.Any)
        return self

    def trigger(self, handle):
        dispatcher.send(signal=handle, sender=handle)
