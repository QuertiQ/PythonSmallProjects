import requests
from bs4 import BeautifulSoup
import tkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from io import BytesIO

# Default Headers to scrap functions
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


# Scrap price
def get_product_price(url, headers = DEFAULT_HEADERS):
    try:

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding price
        price_string = soup.find("span", {"class": "a-price-whole"}).text.strip()
        decimal_price = soup.find("span",{"class": "a-price-fraction"}).text.strip()
        price = f'{price_string}{decimal_price}'

        return price
    except Exception as e:
        print(f"Błąd podczas scrapowania: {e}")
        return None
# Scrap title
def get_product_title(url, headers = DEFAULT_HEADERS):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find("span", {"class" : "a-size-large product-title-word-break"}).text.strip()
        return title
    except Exception as e:
        print(f"Błąd podczas scrapowania: {e}")
        return None
# Scrap src
def get_jpg_src(url, headers = DEFAULT_HEADERS):
    try:
        jpg_source = []
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tag = soup.find("img", {"id": "landingImage"})
        if image_tag and 'src' in image_tag.attrs:
            return image_tag['src']
    except Exception as e:
        print(f"Błąd podczas scrapowania: {e}")
        return None
#Button onclick function
def button_pressed():
    title = get_product_title(link.get())
    price = get_product_price(link.get())
    jpg_src = get_jpg_src(link.get())
    response = requests.get(get_jpg_src(link.get()))
    img_data = response.content
    image = Image.open(BytesIO(img_data))
    image = image.resize((300, 300))
    img = ImageTk.PhotoImage(image)


    if price:
        textbox = ctk.CTkTextbox(app, width=400, height=300)

        textbox.place(x=300, y=100)

        textbox.insert('0.0', f'Nazwa produkt: {title} \nCena produktu to: {price} zł\nZdjecia:{str(jpg_src)}')  # insert at line 0 character 0
        label = ctk.CTkLabel(app, image=img)
        label.place(x=600, y=600)

    else:
        print("Nie udało się pobrać ceny oraz tytułu produktu.")




ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1920x1440")
app.title("Ceny produktów")
url_text = tkinter.StringVar()
link = ctk.CTkEntry(app, width=350,height=40, textvariable=url_text)
link.pack()


button = ctk.CTkButton(app, text='Pobierz cene', width=140, height=28, command=button_pressed)
button.place(x=100, y=100)
app.mainloop()