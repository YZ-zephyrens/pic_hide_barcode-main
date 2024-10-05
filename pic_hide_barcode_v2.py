from PIL import Image

# 打开两张图片，确保路径正确
imgPutong = Image.open(r"普通图片.jpg")  # 普通图片
imgBarcode = Image.open(r"二维码.png")  # 二维码图片

# 确保二维码图片是RGBA模式，如果不是则进行转换
if imgBarcode.mode != "RGBA":
    imgBarcode = imgBarcode.convert("RGBA")

# 创建一个与普通图片尺寸相同的白色背景
imgBarcodeWithWhiteBg = Image.new("RGBA", (imgPutong.width, imgPutong.height), (255, 255, 255, 255))

# 调整二维码在白色背景中的位置，指定左上角位置
qr_x = (imgPutong.width - imgBarcode.width) // 2  # X方向居中
qr_y = (imgPutong.height - imgBarcode.height) // 2  # Y方向居中

qr_y =1
qr_x = 2
# 将二维码粘贴到白色背景上，指定位置
imgBarcodeWithWhiteBg.paste(imgBarcode, (qr_x, qr_y), imgBarcode)

# 创建新图片，使用RGBA模式
imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height))

# 填充新图片上的每一个像素
for w in range(imgMix.width):
    for h in range(imgMix.height):
        pxlPutong = imgPutong.getpixel((w, h))
        pxlBarcode = imgBarcodeWithWhiteBg.getpixel((w, h))

        # 判断二维码背景是否为白色
        if pxlBarcode[0] > 200 and pxlBarcode[1] > 200 and pxlBarcode[2] > 200:
            # 复制普通图片的像素值，透明度设为255（不透明）
            imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))
        else:
            # 根据公式计算新的rgb值
            alpha = 150  # 透明度
            r = max(0, min(255, int((pxlPutong[0] - (255 - alpha)) / alpha * 255)))
            g = max(0, min(255, int((pxlPutong[1] - (255 - alpha)) / alpha * 255)))
            b = max(0, min(255, int((pxlPutong[2] - (255 - alpha)) / alpha * 255)))
            imgMix.putpixel((w, h), (r, g, b, alpha))

# 保存合成的新图片
imgMix.save(r"./合成图片1.png")
print("生成完毕，快去群里浪吧")
