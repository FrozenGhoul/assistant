import datetime as dt
from . import BaseModule


class SystemModule(BaseModule):
    def __init__(self, *args):
        super(SystemModule, self).__init__(*args)

    def default(self):
        return "Repeat back your command!."

    def time_right_now(self):
        time = dt.datetime.now().strftime("%I:%M:%p").split(":")
        return "The time is {} {} {}".format(*map(int, time[:2]), time[2])

    def date_today(self):
        return dt.datetime.now().strftime("It's %A, %d %B %Y today!")

    def tell_system_status(self):
        import psutil
        import platform
        import datetime

        os, name, version, _, _, _ = platform.uname()
        version = version.split('-')[0]
        cores = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory()[2]
        disk_percent = psutil.disk_usage('/')[3]
        boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
        running_since = boot_time.strftime("%A %d. %B %Y")
        response = "I am currently running on %s version %s.  " % (os, version)
        response += "This system is named %s and has %s CPU cores.  " % (name, cores)
        response += "Current disk_percent is %s percent.  " % disk_percent
        response += "Current CPU utilization is %s percent.  " % cpu_percent
        response += "Current memory utilization is %s percent. " % memory_percent
        response += "it's running since %s." % running_since
        return response
