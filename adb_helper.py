import re
from adbutils import adb,AdbClient


class adb_helper:
    def __init__(self):
        self.__adb = AdbClient(host="127.0.0.1", port=5037)
        self.__adb_log='daemon not running; starting now at tcp:5037'

    def adb_connect(self,ip):
        if not ip:
            self.__adb = AdbClient(host="127.0.0.1", port=5037)
            self.__adb_log = 'daemon not running; starting now at tcp:5037'
            try:
                adb.wait_for(timeout=10)
            except:
                self.__adb_log="Device not connected"

        elif ip:
            ip_addr = self.__find_ip_regex(ip)
            if ip_addr:
                self.__adb_log=adb.connect(ip_addr.group(0))
            else:
                self.__adb_log = 'Invalid ip address'
        return self.adb_get_device()

    def adb_disconnect_all(self):
        self.__adb_log=adb.server_kill()

    def adb_disconnect_ip(self,ip):
        if self.__find_ip_regex(ip):
            self.__adb_log = adb.disconnect(ip)
        else:
            self.__adb_log = "Cannot disconnect device connected with cabel"

    def __find_ip_regex(self,ip):
        pat = re.compile("[0-9]+(?:\.[0-9]+){3}(:[0-9]+)?")
        ip_addr = pat.search(ip)
        return ip_addr

    def adb_get_device(self):
        if adb.device_list():
            device_id = [device_id.get_serialno() for device_id in adb.device_list()]
            return device_id

    def start_server(self):
        adb.server_version()

    def get_status(self):
        return self.__adb_log
    def set_one_device(self):
        return adb.must_one_device