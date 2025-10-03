# 代码生成时间: 2025-10-04 02:26:24
import tornado.ioloop
import tornado.web
import json

# IoT Device Manager Class
class IoTDeviceManager:
    def __init__(self):
        self.devices = {}

    def add_device(self, device_id, device_info):
        """Add a new device to the manager."""
        if device_id in self.devices:
            raise ValueError(f"Device with ID {device_id} already exists.")
        self.devices[device_id] = device_info

    def remove_device(self, device_id):
        """Remove a device from the manager."""
        if device_id not in self.devices:
            raise ValueError(f"Device with ID {device_id} not found.")
        del self.devices[device_id]

    def get_device_info(self, device_id):
        """Get device information by device ID."""
        return self.devices.get(device_id, None)

    def update_device_info(self, device_id, device_info):
        """Update device information."""
        if device_id not in self.devices:
            raise ValueError(f"Device with ID {device_id} not found.")
        self.devices[device_id] = device_info

# Tornado Request Handler for Device Management
class DeviceHandler(tornado.web.RequestHandler):
    def initialize(self, device_manager):
        self.device_manager = device_manager

    def post(self):
        """Handle POST requests to add a new device."""
        try:
            device_data = json.loads(self.request.body)
            device_id = device_data.get('id')
            device_info = device_data.get('info')
            self.device_manager.add_device(device_id, device_info)
            self.write({'status': 'success', 'message': 'Device added successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)

    def delete(self, device_id):
        """Handle DELETE requests to remove a device."""
        try:
            self.device_manager.remove_device(device_id)
            self.write({'status': 'success', 'message': 'Device removed successfully'})
        except Exception as e:
            self.write({'status': 'error', 'message': str(e)})
            self.set_status(400)

    def get(self, device_id=None):
        """Handle GET requests to get device info."""
        if device_id:
            device_info = self.device_manager.get_device_info(device_id)
            if device_info:
                self.write({'status': 'success', 'message': device_info})
            else:
                self.write({'status': 'error', 'message': 'Device not found'})
                self.set_status(404)
        else:
            self.write({'status': 'error', 'message': 'No device ID provided'})
            self.set_status(400)

# Main Application Setup
def make_app():
    return tornado.web.Application(
        handlers=[
            (r"/", DeviceHandler),  # Index handler
            (r"/device/(\w+)", DeviceHandler),  # Device specific handler
        ],
        device_manager=IoTDeviceManager()  # Initialize the device manager
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("IoT Gateway Manager is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()