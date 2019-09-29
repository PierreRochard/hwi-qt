from hwi_qt.logging import log


class Device(object):
    def __init__(self, device_data: dict):
        self.type = device_data.pop('type', None)
        self.model = device_data.pop('model', None)
        self.fingerprint = device_data.pop('fingerprint', None)
        self.needs_passphrase = device_data.pop('needs_passphrase', None) or device_data.pop('needs_passphrase_sent', None)
        self.needs_pin = device_data.pop('needs_pin_sent', None)
        self.path = device_data.pop('path')
        self.error = device_data.pop('error', None)
        self.code = device_data.pop('code', None)

        if device_data:
            log.warning('Not all device data was used', unused_device_data=device_data)
