import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("拖动二维码至普通图片")

        # 创建画布
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        # 按钮：选择普通图片
        self.btn_select_img = tk.Button(root, text="选择普通图片", command=self.load_imgPutong)
        self.btn_select_img.pack(side=tk.LEFT, padx=10)

        # 按钮：选择二维码图片
        self.btn_select_qr = tk.Button(root, text="选择二维码图片", command=self.load_imgBarcode)
        self.btn_select_qr.pack(side=tk.LEFT, padx=10)

        # 按钮：保存图片
        self.btn_save = tk.Button(root, text="保存合成图片", command=self.save_image)
        self.btn_save.pack(side=tk.RIGHT, padx=10)

        self.imgPutong = None
        self.imgBarcode = None
        self.imgPutongTk = None
        self.imgBarcodeTk = None
        self.qr_x = 0
        self.qr_y = 0

        self.qr_moving = False

    def load_imgPutong(self):
        file_path = filedialog.askopenfilename(title="选择普通图片")
        if file_path:
            self.imgPutong = Image.open(file_path).convert("RGBA")  # 确保转换为RGBA模式
            self.imgPutongTk = ImageTk.PhotoImage(self.imgPutong)
            self.canvas.config(width=self.imgPutong.width, height=self.imgPutong.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgPutongTk)

    def load_imgBarcode(self):
        file_path = filedialog.askopenfilename(title="选择二维码图片")
        if file_path:
            self.imgBarcode = Image.open(file_path).convert("RGBA")
            self.imgBarcodeTk = ImageTk.PhotoImage(self.imgBarcode)
            self.qr_x, self.qr_y = (self.imgPutong.width - self.imgBarcode.width) // 2, (
                        self.imgPutong.height - self.imgBarcode.height) // 2
            self.qr_id = self.canvas.create_image(self.qr_x, self.qr_y, anchor=tk.NW, image=self.imgBarcodeTk)

            # 绑定鼠标事件
            self.canvas.tag_bind(self.qr_id, "<ButtonPress-1>", self.on_qr_press)
            self.canvas.tag_bind(self.qr_id, "<B1-Motion>", self.on_qr_move)

    def on_qr_press(self, event):
        self.qr_moving = True
        self.qr_offset_x = event.x - self.qr_x
        self.qr_offset_y = event.y - self.qr_y

    def on_qr_move(self, event):
        if self.qr_moving:
            self.qr_x = event.x - self.qr_offset_x
            self.qr_y = event.y - self.qr_offset_y
            self.canvas.coords(self.qr_id, self.qr_x, self.qr_y)

    def save_image(self):
        if self.imgPutong and self.imgBarcode:
            # 创建与普通图片相同大小的背景
            imgMix = Image.new("RGBA", (self.imgPutong.width, self.imgPutong.height))

            # 获取二维码在白色背景上的位置并应用你的自定义透明处理逻辑
            for w in range(imgMix.width):
                for h in range(imgMix.height):
                    pxlPutong = self.imgPutong.getpixel((w, h))
                    if self.qr_x <= w < self.qr_x + self.imgBarcode.width and self.qr_y <= h < self.qr_y + self.imgBarcode.height:
                        pxlBarcode = self.imgBarcode.getpixel((w - self.qr_x, h - self.qr_y))

                        if pxlBarcode[0] > 200:
                            imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))
                        else:
                            alpha = 150  # 透明度
                            imgMix.putpixel((w, h), (
                                int((pxlPutong[0] - (255 - alpha)) / alpha * 255),
                                int((pxlPutong[1] - (255 - alpha)) / alpha * 255),
                                int((pxlPutong[2] - (255 - alpha)) / alpha * 255),
                                alpha
                            ))
                    else:
                        imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))

            # 保存最终图片
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                imgMix.save(save_path)
                print(f"图片已保存至：{save_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()