"""
Created on Mon June 11 12:06:20 2018

@author: Jakub Grzeszczak
"""


from PIL import Image, ImageFont, ImageDraw, ImageTk
import copy
import textwrap
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter import filedialog

Background_color = [(0, 0, 0), '#000000']
Text_color = [(255, 255, 255), '#FFFFFF']
Template_Image = None
Created_Image = None
Example_Image = None


def decode_image():
    global Background_color
    global Text_color
    global Template_Image
    global Created_Image
    if Template_Image is None:
        return
    red_channel = Template_Image.split()[0]

    x_size = Template_Image.size[0]
    y_size = Template_Image.size[1]

    temp_image = Image.new("RGBA", Template_Image.size, (0, 0, 0, 0))
    pixels = temp_image.load()

    for x in range(x_size):
        for y in range(y_size):
            if bin(red_channel.getpixel((x, y)))[-1] == '0':
                pixels[x, y] = Background_color[0]
            else:
                pixels[x, y] = Text_color[0]
    Created_Image = temp_image
    temp_image = copy.deepcopy(Created_Image).resize((220, 220), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(temp_image)
    created_picture_label.config(image=render)
    created_picture_label.image = render


def write_text(text_to_write, image_size):
    image_text = Image.new("RGBA", image_size, (0, 0, 0, 0))
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping
    para = textwrap.wrap(text_to_write, width=int(image_size[0] / 7))
    current_h, pad = int(image_size[1] / 2 - len(para) * 10), 10
    for line in para:
        w, h = drawer.textsize(line)
        drawer.text(((image_size[0] - w) / 2, current_h), line, font=font)
        current_h += h + pad

    return image_text


def create_example_image():
    global Text_color
    global Background_color
    global Example_Image
    text_to_write = message_input.get()
    if text_to_write == "":
        text_to_write = "TOP SECRET! This is an example message."
    image_size = (320, 160)
    image_text = Image.new("RGBA", image_size, (0, 0, 0, 0))
    image_text.paste(Background_color[0], [0, 0, image_size[0], image_size[1]])
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping.
    para = textwrap.wrap(text_to_write, width=int(image_size[0]/7))
    current_h, pad = int(image_size[1] / 2 - len(para) * 10), 10
    for line in para:
        w, h = drawer.textsize(line)
        drawer.text(((image_size[0] - w) / 2, current_h), line, font=font, fill=Text_color[0])
        current_h += h + pad

    Example_Image = image_text
    render = ImageTk.PhotoImage(Example_Image)
    example_image_label.config(image=render)
    example_image_label.image = render


def encode_image():
    global Template_Image
    global Created_Image
    if Template_Image is None or message_input.get() is "":
        return
    red_template, green_template, blue_template, alpha_template = Template_Image.split()
    x_size = Template_Image.size[0]
    y_size = Template_Image.size[1]

    image_text = write_text(message_input.get(), Template_Image.size)
    bw_encode = image_text.convert('1')

    temp_image = Image.new("RGBA", (x_size, y_size), (0, 0, 0, 0))
    pixels = temp_image.load()
    for x in range(x_size):
        for y in range(y_size):
            red_template_pix = bin(red_template.getpixel((x, y)))
            tencode_pix = bin(bw_encode.getpixel((x, y)))

            if tencode_pix[-1] == '1':
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            pixels[x, y] = (int(red_template_pix, 2),
                            green_template.getpixel((x, y)),
                            blue_template.getpixel((x, y)),
                            alpha_template.getpixel((x,y)))
    Created_Image = temp_image
    temp_image = copy.deepcopy(Template_Image).resize((220, 220), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(temp_image)
    created_picture_label.config(image=render)
    created_picture_label.image = render


def save_picture():
    global Created_Image
    if Created_Image is None:
        return
    filename = filedialog.asksaveasfilename(initialdir="/", title="Save picture", filetypes=(("PNG images", "*.png"),
                                                                                             ("All files", "*.*")))
    if not filename:
        return
    if not filename.endswith('.png'):
        filename += '.png'
    Created_Image.save(filename)


def load_picture():
    global Template_Image
    filename = filedialog.askopenfilename(initialdir="/", title="Load picture", filetypes=(("PNG images", "*.png"),
                                                                                           ("All files", "*.*")))
    if not filename:
        return
    Template_Image = Image.open(filename)
    temp_image = copy.deepcopy(Template_Image).resize((220, 220), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(temp_image)
    template_picture_label.config(image=render)
    template_picture_label.image = render
    created_picture_label.image = None


def pick_color(flag):
    global Background_color
    global Text_color
    global Example_Image
    color = askcolor()
    color = [tuple(int(i) for i in color[0]), color[1]]
    if flag == "bg":
        Background_color = color
    else:
        Text_color = color
    create_example_image()


if __name__ == "__main__":

    window = tk.Tk()
    window.title("Steganography")
    window.resizable(width=False, height=False)
    window.geometry("%dx%d+%d+%d" % (470, 470,
                                     window.winfo_screenwidth() / 2 - 235,
                                     window.winfo_screenheight() / 2 - 235))
    template_picture_label = tk.Label(window, image=None, borderwidth=4, relief="sunken", text="picture input")
    template_picture_label.place(x=10, y=10, width=220, height=220)
    load_picture_button = tk.Button(window, text="load picture", command=load_picture)
    load_picture_button.place(x=10, y=235, width=220, height=25)
    created_picture_label = tk.Label(window, image=None, borderwidth=4, relief="sunken", text="picture output")
    created_picture_label.place(x=240, y=10, width=220, height=220)
    save_picture_button = tk.Button(window, text="save picture", command=save_picture)
    save_picture_button.place(x=240, y=235, width=220, height=25)

    def update_picture():
        create_example_image()

    def limit_length(added_value):
        return ord(added_value) <= 255
    reg = window.register(limit_length)

    input_var = tk.StringVar()
    input_var.trace("w", lambda name, index, mode, sv=input_var: update_picture())
    message_input = tk.Entry(window, textvariable=input_var, validate="key", validatecommand=(reg, '%S'))
    message_input.place(x=10, y=270, width=350, height=25)
    message_input_label = tk.Label(window, text="secret message")
    message_input_label.place(x=370, y=270, height=25)
    hide_picture_button = tk.Button(window, text="hide message", command=encode_image)
    hide_picture_button.place(x=340, y=310, width=120, height=30)
    decode_picture_button = tk.Button(window, text="decode picture", command=decode_image)
    decode_picture_button.place(x=340, y=350, width=120, height=30)
    choose_bg_color_button = tk.Button(window, text="change background", command=lambda: pick_color("bg"))
    choose_bg_color_button.place(x=340, y=390, width=120, height=30)
    choose_text_color_button = tk.Button(window, text="set text color", command=lambda: pick_color("fg"))
    choose_text_color_button.place(x=340, y=430, width=120, height=30)

    example_image_label = tk.Label(window, image=None, borderwidth=4, relief="sunken")
    example_image_label.place(x=10, y=305, width=320, height=160)
    create_example_image()
    window.mainloop()
