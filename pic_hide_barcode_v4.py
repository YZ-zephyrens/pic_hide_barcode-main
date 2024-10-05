import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("拖动二维码至普通图片")

        # 设置最大窗口大小
        self.max_width = 800
        self.max_height = 600

        # 创建画布
        self.canvas = tk.Canvas(root, width=self.max_width, height=self.max_height)
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
        self.scale_ratio = 1  # 缩放比例
        self.qr_moving = False

    def load_imgPutong(self):
        file_path = filedialog.askopenfilename(title="选择图片")
        if file_path:
            self.imgPutong = Image.open(file_path).convert("RGBA")

            # 检查图片尺寸，是否需要缩放
            self.scale_ratio = min(self.max_width / self.imgPutong.width, self.max_height / self.imgPutong.height, 1)
            new_width = int(self.imgPutong.width * self.scale_ratio)
            new_height = int(self.imgPutong.height * self.scale_ratio)
            resized_imgPutong = self.imgPutong.resize((new_width, new_height), Image.Resampling.LANCZOS)

            self.imgPutongTk = ImageTk.PhotoImage(resized_imgPutong)
            self.canvas.config(width=new_width, height=new_height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgPutongTk)

    def load_imgBarcode(self):
        file_path = filedialog.askopenfilename(title="选择二维码图片")
        if file_path:
            self.imgBarcode = Image.open(file_path).convert("RGBA")

            # 缩放二维码图片与背景图相同的比例
            qr_width = int(self.imgBarcode.width * self.scale_ratio)
            qr_height = int(self.imgBarcode.height * self.scale_ratio)
            resized_imgBarcode = self.imgBarcode.resize((qr_width, qr_height), Image.Resampling.LANCZOS)

            self.imgBarcodeTk = ImageTk.PhotoImage(resized_imgBarcode)
            self.qr_x, self.qr_y = (self.canvas.winfo_width() - qr_width) // 2, (
                        self.canvas.winfo_height() - qr_height) // 2
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
            # 将缩放后的二维码位置还原到原始图片的位置
            qr_x_original = int(self.qr_x / self.scale_ratio)
            qr_y_original = int(self.qr_y / self.scale_ratio)

            # 创建与普通图片相同大小的背景
            imgMix = Image.new("RGBA", (self.imgPutong.width, self.imgPutong.height))

            # 获取二维码在白色背景上的位置并应用自定义透明处理逻辑
            for w in range(imgMix.width):
                for h in range(imgMix.height):
                    pxlPutong = self.imgPutong.getpixel((w, h))
                    if qr_x_original <= w < qr_x_original + self.imgBarcode.width and qr_y_original <= h < qr_y_original + self.imgBarcode.height:
                        pxlBarcode = self.imgBarcode.getpixel((w - qr_x_original, h - qr_y_original))

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
