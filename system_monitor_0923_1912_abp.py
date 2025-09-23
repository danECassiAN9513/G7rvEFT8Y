# 代码生成时间: 2025-09-23 19:12:22
import os
import psutil
import tornado.ioloop
import tornado.web


"""
系统性能监控工具使用Tornado框架实现。
该工具提供CPU使用率、内存使用情况、磁盘使用情况和网络状态的实时监控。
"""


class SystemMonitorHandler(tornado.web.RequestHandler):
    """
    系统监控的请求处理器。
    """
    def get(self):
        try:
            # 获取CPU使用率
            cpu_usage = psutil.cpu_percent(interval=1)
            # 获取内存使用情况
            mem = psutil.virtual_memory()
            # 获取磁盘使用情况
            disks = psutil.disk_partitions()
            disks_usage = []
            for disk in disks:
                usage = psutil.disk_usage(disk.mountpoint)
                disks_usage.append({"device": disk.device, "usage": usage.percent})
            # 获取网络状态
            net_io = psutil.net_io_counters()
            # 构建响应数据
            response_data = {
                "cpu": cpu_usage,
                "memory": {
                    "total": mem.total,
                    "used": mem.used,
                    "free": mem.free,
                    "percent": mem.percent
                },
                "disks": disks_usage,
                "net_io": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_recv": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_recv": net_io.packets_recv
                }
            }
            # 返回响应
            self.write(response_data)
        except Exception as e:
            # 错误处理
            self.write({'error': str(e)})


def make_app():
    """
    创建Tornado应用。
    """
    return tornado.web.Application(
        [
            (r"/", SystemMonitorHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("System Monitor is running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()