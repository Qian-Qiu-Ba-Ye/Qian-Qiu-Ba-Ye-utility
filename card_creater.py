from PIL import Image, ImageDraw, ImageFilter, ImageFont
import cairosvg
import os
import json

class Card:

    def __init__(
            self, 
            image_path, 
            name, 
            effect,
            type,
            description,
            color_scheme,
            power=0,
            toughness=0,
            mana_cost="0 0 0 0 0",
            ):
        self.color_path=[
            "template/blue.png",
            "template/yellow.png",
            "template/red.png",
            "template/green.png",
            "template/land.png",
        ]
        self.color_scheme_list=[
            (167,216,251),
            (237,162,84),
            (168,46,56),
            (90,150,102),
            (109,138,138),
        ]
        background = Image.open(self.color_path[color_scheme])
        self.height = int(background.height)
        self.width = int(background.height*63/88)
        self.image_path = image_path
        self.name = name
        self.type = type
        self.effect = effect
        self.description = description
        self.color_scheme = color_scheme
        self.power = power
        self.toughness = toughness
        self.mana_cost = [int(x) for x in mana_cost.split(" ")]
        self.mana_cost_icons=[
            "template/person.png",
            "template/follower.png",
            "template/gold.png",
            "template/stone.png",
            "template/horse.png"
        ]
        self.font_path="ZiHunXianJianQiXiaTi(ShangYongXuShouQuan)-2.ttf"

    def create_background(self):
        background = Image.open(self.color_path[self.color_scheme])
        background=background.resize((self.width,self.height))
        return background
    
    def create_container(self,image):
        
        position_lists=[
            [self.width*0.1, self.height*0.05, self.width*0.9, self.height*0.12],
            
            [self.width*0.1, self.height*0.59, self.width*0.9, self.height*0.66],
            [self.width*0.1, self.height*0.68, self.width*0.9, self.height*0.95],
        ]
        for i in range(len(position_lists)):
            container = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(container)
            rect_x0, rect_y0 = position_lists[i][0], position_lists[i][1]
            rect_x1, rect_y1 = position_lists[i][2], position_lists[i][3]
            radius = 5
            
            draw.rounded_rectangle(
                [(rect_x0, rect_y0), (rect_x1, rect_y1)],
                radius=radius,
                outline=(241,224,161, 255), 
                width=3,
                fill=(*self.color_scheme_list[self.color_scheme], 238)  # White with 50% transparency
            )
            container = container.filter(ImageFilter.GaussianBlur(2))
            image.paste(container, (0, 0), container)
        return image
    
    def add_picture(self,image):
        if not os.path.exists(self.image_path):
            self.image_path="template/test.jpg"
        picture=Image.open(self.image_path)
        original_width, original_height = picture.size
        target_width=original_width
        target_height=original_width*0.57/0.75

        left = (original_width - target_width) / 2
        top = (original_height - target_height) / 2
        right = left + target_width
        bottom = top + target_height
        picture = picture.crop((left, top, right, bottom))
        picture=picture.resize((int(self.width*0.75),int(self.width*0.57)))
        if picture.mode != 'RGBA':
            picture = picture.convert('RGBA')
        border_size = 15  # 边框大小
        radius = 15  # 圆角半径
        bordered_picture = Image.new('RGBA', (picture.width + 2 * border_size, picture.height + 2 * border_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bordered_picture)
        
        draw.rounded_rectangle(
            [(0, 0), (bordered_picture.width, bordered_picture.height)],
            radius=radius,
            outline=(241,224,161, 255),  # 黑色边框
            width=border_size
        )
        
        # 将原图粘贴到带边框的图像上
        bordered_picture.paste(picture, (border_size, border_size), picture)
        
        image.paste(bordered_picture, (int(self.width*0.125)-border_size, int(self.height*0.15)-border_size), bordered_picture)
        return image
    
    def add_text_title(self,image):
        draw = ImageDraw.Draw(image)
    
        # 加载字体
        try:
            font = ImageFont.truetype(self.font_path, 60)  # 确保字体文件存在
        except IOError:
            font = ImageFont.load_default()  # 如果字体文件不存在，使用默认字体
        bbox = draw.textbbox((0, 0), self.name, font=font)
        text_width = bbox[2] - bbox[0]
        # 绘制文本
        draw.text((self.width*0.88-text_width, self.height*0.05), self.name, fill=(0, 0, 0), font=font)
        
        return image
    
    def add_mana_cost(self,image):
        if sum(self.mana_cost) == 0:
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(self.font_path, 45)  # 确保字体文件存在
            bbox = draw.textbbox((0, 0), "0", font=font)
            draw.text((self.width*0.12, self.height*0.06), "0", fill=(0, 0, 0), font=font)
            return image
        else:
            position=0
            
            for i in range(len(self.mana_cost)):
                if self.mana_cost[i] != 0:
                    svg_image = Image.open(self.mana_cost_icons[i])
                    svg_image = svg_image.resize((40, 40))
                    
                    mana_cost_str = str(self.mana_cost[i])
                    draw = ImageDraw.Draw(image)
                    font = ImageFont.truetype(self.font_path, 45)  # 确保字体文件存在
                    bbox = draw.textbbox((0, 0), mana_cost_str, font=font)
                    text_width = bbox[2] - bbox[0]
                    
                    image.paste(
                        svg_image, 
                        (int(self.width*0.12+position), int(self.height*0.07)),
                        svg_image
                    )
                    position+=40
                    draw.text((self.width*0.12+position, self.height*0.06), mana_cost_str, fill=(0, 0, 0), font=font)
                    position+=text_width

                    position+=20
            return image
        
    def add_type(self,image):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, 45)  # 确保字体文件存在
        
        
        draw.text((self.width*0.12, self.height*0.60), self.type, fill=(0, 0, 0), font=font)
        return image

    def add_effect(self,image):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, 45)  # 确保字体文件存在
        draw.text((self.width*0.12, self.height*0.69), self.effect, fill=(0, 0, 0), font=font)
        return image
    
    def add_description(self,image):
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, 45)  # 确保字体文件存在
        bbox = draw.textbbox((0, 0), "A", font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x_text = self.width * 0.12
        y_text = self.height * 0.74


        for chr in self.description:
            bbox = draw.textbbox((0, 0), chr, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            draw.text((x_text, y_text), chr, font=font, fill=(0, 0, 0))
            
            x_text += text_width
            if x_text > self.width * 0.80:
                x_text = self.width * 0.12
                y_text += text_height+10
        

        return image
    
    def add_power_toughness(self,image):
        if self.power == 0 and self.toughness == 0:
            return image
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(self.font_path, 60)  # 确保字体文件存在
        bbox = draw.textbbox((0, 0), f"{self.power}", font=font)
        text_width_power = bbox[2] - bbox[0]

        bbox = draw.textbbox((0, 0), f"{self.toughness}", font=font)
        text_width_toughness = bbox[2] - bbox[0]
        
        power_icon = Image.open("template/axe.png")
        toughness_icon = Image.open("template/shield.png")
        size=60
        power_icon = power_icon.resize((size, size))
        toughness_icon = toughness_icon.resize((size, size))
        expect_length=size*2+text_width_power+text_width_toughness
        start_x=self.width*0.86-expect_length-40
        image.paste(power_icon, (int(start_x), int(self.height*0.87)), power_icon)
        start_x+=size
        draw.text((int(start_x), int(self.height*0.87)), f"{self.power}", fill=(0, 0, 0), font=font)
        start_x+=text_width_power+40
        image.paste(toughness_icon, (int(start_x), int(self.height*0.87)), toughness_icon)
        start_x+=size
        draw.text((int(start_x), int(self.height*0.87)), f"{self.toughness}", fill=(0, 0, 0), font=font)
        return image

    def add_front_image(self,image):
        image_front=Image.open("template/front.png")
        image_front=image_front.resize((int(self.width*0.998),int(self.height*0.988)))
        image.paste(image_front, (-2, 7), image_front)
        return image

    def create_card(self):
        background = self.create_background()
        container = self.create_container(background)
        container=self.add_picture(container)
        container=self.add_text_title(container)
        container=self.add_mana_cost(container)
        container=self.add_type(container)
        container=self.add_effect(container)
        container=self.add_description(container)
        container=self.add_power_toughness(container)

        
        result=self.add_front_image(container)
        result.save(f"output/{self.name}.png")
        #result.show()
        

def initinal_svg():
    mana_cost_icons=[
        "template/person.svg",
        "template/follower.svg",
        "template/gold.svg",
        "template/stone.svg",
        "template/horse.svg",
        "template/axe.svg",
        "template/shield.svg"
    ]
    for i in range(len(mana_cost_icons)):
        png_path = mana_cost_icons[i].replace(".svg", ".png")
        cairosvg.svg2png(url=mana_cost_icons[i], write_to=png_path)


def read_json(path):
    with open(path, "r") as f:
        card_data = json.load(f)
    return card_data


def main():
    card_data = read_json(path="test_example.json")
    print(card_data)
    for card in card_data:
        card = Card(
            image_path=card["image_path"],
            name=card["name"],
            type=card["type"],
            effect=card["effect"],
            description=card["description"],
            color_scheme=card["color_scheme"],
            mana_cost=card["mana_cost"],
            power=card["power"],
            toughness=card["toughness"]
        )
        card.create_card()
if __name__ == "__main__":
    main()
    #initinal_svg()
    # card = Card(
    #     image_path="template/test.jpg",
    #     name="超级农民",
    #     type="传奇建筑",
    #     effect="【触发效果】",
    #     description="当回合结束时，对所有敌方部队造成一点伤害,如果有部队被击杀，自己+1/+1",
    #     color_scheme=3,
    #     mana_cost="0 0 0 0 0",
    #     power=0,
    #     toughness=0
    # )
    # card.create_card()
