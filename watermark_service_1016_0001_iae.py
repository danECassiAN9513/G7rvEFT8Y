# 代码生成时间: 2025-10-16 00:01:12
import os
import base64
from PIL import Image
from io import BytesIO
import tornado.web
import tornado.ioloop
import numpy as np

"""
数字水印服务，使用Tornado框架实现。
"""

class WatermarkServiceHandler(tornado.web.RequestHandler):
    """
    处理加水印请求的Handler。
    """
    def post(self):
        # 从请求中获取图片文件
        image_file = self.request.files['image'][0]
        image_data = image_file.body
        
        try:
            # 将图片文件转换为PIL Image对象
            image = Image.open(BytesIO(image_data))
            
            # 添加水印
            watermarked_image = self.add_watermark(image)
            
            # 将水印图片输出到byte流
            output = BytesIO()
            watermarked_image.save(output, format='PNG')
            output.seek(0)
            
            # 设置响应类型和内容
            self.set_header('Content-Type', 'image/png')
            self.write(output.read())
        except Exception as e:
            # 错误处理
            self.set_status(400)
            self.write({'error': str(e)})
        finally:
            # 关闭文件
            image_file.close()

    def add_watermark(self, image):
        """
        在图片上添加水印。
        :param image: PIL Image对象
        :return: 添加水印后的图片
        """
        # 创建水印文本
        watermark_text = "Watermark"
        font = Image.font.load_default()
        watermark_image = Image.new('RGB', image.size)
        
        # 设置水印颜色和位置
        draw = watermark_image.draw
        text_width, text_height = draw.textsize(watermark_text, font=font)
        x = image.size[0] - text_width - 10
        y = image.size[1] - text_height - 10
        
        # 添加水印
        draw.text((x, y), watermark_text, fill=(255, 255, 255), font=font)
        
        # 将水印和原图合并
        watermarked_image = Image.alpha_composite(image.convert('RGBA'), watermark_image)
        
        return watermarked_image.convert('RGB')

# 设置路由和启动服务器
def make_app():
    return tornado.web.Application(
        handlers=[(r'/watermark', WatermarkServiceHandler)],
        debug=True,
    )

if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    print('Watermark service is running on http://localhost:8888/watermark')
    tornado.ioloop.IOLoop.current().start()