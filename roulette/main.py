from PIL import Image, ImageDraw, ImageFont
import cmath
import math
import random

class Roulette:
    def __init__(self):
        self.amount = 0
        self.space = None
        self.canvas = Image.new('RGBA', (600, 600), (0,0,0,0))
        self.draw = ImageDraw.Draw(self.canvas)
        self.font = ImageFont.truetype("fonts/FreeMonoBold.ttf", 24)  # Font style and size
        self.wheel = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]

    def get_polar(self, r: float, ang: float):

        phi = ang * cmath.pi / 180
        x = r * cmath.cos(phi).real
        y = r * cmath.sin(phi).real

        return (round(x)+300, round(y)+300)

    def get_rotated_text(self, text: str, ang: float):
        text_image = Image.new('RGBA', (30, 20), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), text, fill="white", font=self.font)

        rotated_text_image = text_image.rotate(ang, expand=True)

        rotated_width, rotated_height = rotated_text_image.size

        paste_x = rotated_width // 2
        paste_y = rotated_height // 2

        return rotated_text_image, paste_x, paste_y

    def create_spinner(self):
        self.draw.polygon([self.get_polar(300,i*360/37) for i in range(len(self.wheel))], fill="#7f6b61")
        self.draw.polygon([self.get_polar(280,i*360/37) for i in range(len(self.wheel))], fill="#4b413a")
        self.draw.polygon([self.get_polar(200,i*360/37) for i in range(len(self.wheel))], fill="#8aa63f")
        
        for i, text in enumerate(self.wheel):
            ang = i * 360/37
            ang2 = (i+1) * 360/37

            if text == 0:
                color = "green"
            elif i % 2 == 0:
                color = "red"
            elif i % 2 == 1:
                color = "black"

            self.draw.polygon([self.get_polar(200,ang), self.get_polar(240,ang), self.get_polar(240,ang2), self.get_polar(200,ang2)], fill=color)

            # Borders
            self.draw.line([self.get_polar(200,ang), self.get_polar(240,ang)], fill='black', width=2)
            self.draw.line([self.get_polar(240,ang), self.get_polar(240,ang2)], fill='black', width=2)
            self.draw.line([self.get_polar(200,ang), self.get_polar(200,ang2)], fill='black', width=2)

            # Roll slots
            self.draw.polygon(
                [
                    self.get_polar(160,ang+1), 
                    self.get_polar(192,ang+1), 
                    self.get_polar(192,ang2-1), 
                    self.get_polar(160,ang2-1)
               ], 
                fill="#376f1b"
            )

            #self.draw.line([self.get_polar(180,ang), self.get_polar(180,ang2)], fill='black', width=2)
            #self.draw.line([self.get_polar(180,ang), self.get_polar(200,ang)], fill='black', width=2)

            # Center poly
            #self.draw.line([self.get_polar(180,ang), self.get_polar(0,0)], fill=(0, 64, 9), width=2)

            # Text
            img, offset_x, offset_y = self.get_rotated_text(str(text), 270-ang-5)

            if text < 10:
                ang_offset = -360/37*0.3
            else:
                ang_offset = -360/37*0.5

            pos = list(self.get_polar(220,ang2+ang_offset))
            pos[0] -= offset_x
            pos[1] -= offset_y
            self.canvas.paste(img, pos, img)

        self.draw.ellipse([self.get_polar(-215,45), self.get_polar(215,45)], fill="#4b413a")
        self.draw.ellipse([self.get_polar(-190,45), self.get_polar(190,45)], fill="#7f6b61")
        self.draw.ellipse([self.get_polar(-40,45), self.get_polar(40,45)], fill="#4b413a")
        self.draw.ellipse([self.get_polar(-25,45), self.get_polar(25,45)], fill='#f7b231')

        self.draw.polygon(
            [self.get_polar(-120,41), self.get_polar(120,49),self.get_polar(120,41),  self.get_polar(-120,49)], 
            fill="#f7b231"
        )
        self.draw.polygon(
            [self.get_polar(-120,41+90), self.get_polar(120,49+90),self.get_polar(120,41+90),  self.get_polar(-120,49+90)], 
            fill="#f7b231"
        )


    def create_gif(self):
        duration = 5
        frames_per_second = 20
        total_frames = duration * frames_per_second
        # 360 deg (1x)
        angles = [cmath.sin(2 * i / total_frames + 1.16).real * 5.12 for i in range(total_frames)]

        frames = []
        winner1 = random.randint(0, 36)
        angle = 360/37 * winner1

        for i in range(total_frames):
            angle += angles[i]
            rotated_frame = self.canvas.rotate(angle)
            frames.append(rotated_frame)

        # 810 (2.25x)
        angles = [cmath.sin(2 * i / total_frames + 1.16).real * 11.4999 for i in range(total_frames)]
        lengths = [
            (239.09*x**7 - 899.43*x**6 + 1345.94*x**5 - 1009.46*x**4 + 399.2*x**3 - 80.32*x**2 + 7.31*x - 0.77)*-.41 
            for x in [i/total_frames for i in range(total_frames)]
        ]

        winner2 = random.randint(0, 36)
        angle = 360/37 * winner2

        print(winner1, winner2, winner2*0.25, self.wheel[((winner2+9) + winner1) % len(self.wheel)])
        for i in range(total_frames):
            frame = frames[i]
            draw = ImageDraw.Draw(frame)
            angle += angles[i]

            x, y = self.get_polar(lengths[i]*100 + 230, angle+2)
            cords = [(x+10, y+10), (x-10,y-10)]
            draw.ellipse([min(cords), max(cords)], fill='#ffffff')

        frames[0].save('spinning_circle.gif', save_all=True, append_images=frames[1:], optimize=False, duration=int(1000/frames_per_second))

        return {"num": self.wheel[((winner2+9) + winner1) % len(self.wheel)], }


if __name__ == "__main__":
    table = Roulette()
    table.create_spinner()
    table.create_gif()
