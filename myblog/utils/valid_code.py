def get_valid_value(request):
    import random
    def get_random_color():
        return(random.randint(0,255),random.randint(0,255),random.randint(0,255))

    from PIL import Image,ImageDraw,ImageFont
    from io import BytesIO
    image = Image.new("RGB",(280,40),get_random_color())

    #给image对象输入文字
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("static/font/KumoFont.ttf",size=35)

    keep_valid_codes = ""
    for i in range(5):
        random_num = str(random.randint(0,9))
        random_lower = chr(random.randint(97,122))
        random_upper = chr(random.randint(65,90))
        random_char = random.choice([random_num,random_lower,random_upper])[0]
        print(random_char,"===")
        draw.text((20+i*50,0),random_char,fill=get_random_color(),font=font)
        keep_valid_codes += random_char

    width = 280
    height = 40

    f = BytesIO()
    image.save(f,"png")
    data = f.getvalue()
    print("valid_codes:",keep_valid_codes)

    request.session["keep_valid_codes"] = keep_valid_codes

    return data


