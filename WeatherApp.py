from tkinter import messagebox, END
import ttkbootstrap
from PIL import Image, ImageTk
import requests


def get_weather(city):
    if city == '' or city == '        Enter the city':
        messagebox.showerror("Error", "Enter the city")
        return None
    API_key = "f6ad032b28cc8cdf1bcdbb12841320a2"
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}'
    result = requests.get(url)

    if result.status_code == 404:
        messagebox.showerror("Error", "City doesn't found")
        return None

    weather = result.json()
    icon_id = weather['weather'][0]['icon']
    temperature = int(weather['main']['temp'] - 273.15)
    feels_like = int(weather['main']['feels_like'] - 273.15)
    description = weather['weather'][0]['description']
    words = description.split()
    capitalized_words = [word.capitalize() for word in words]
    description = " ".join(capitalized_words)
    city = weather['name']
    country = weather['sys']['country']
    pressure = weather['main']['pressure']
    humidity = weather['main']['humidity']
    visibility = int(weather['visibility'] / 1000)
    wind = int(weather['wind']['speed'] * 3.6)
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return icon_url, temperature, feels_like, description, city, country, pressure, humidity, visibility, wind


root = ttkbootstrap.Window(title='SkyCast', themename='morph')
root.iconbitmap('weather.ico')
root.geometry('410x510')
root.resizable(False, False)


def remove_text(event):
    entry = event.widget
    current_text = entry.get()
    if current_text == '        Enter the city':
        entry.delete(0, END)


search_frame = ttkbootstrap.Frame(root)
search_frame.pack(pady=20, side='top')

city_entry = ttkbootstrap.Entry(search_frame, foreground='#373738', font="Helvetica, 13", style='dark.TEntry')
city_entry.insert(0, '        Enter the city')
city_entry.bind('<FocusIn>', remove_text)
city_entry.pack()

search_button = ttkbootstrap.Button(search_frame, text="Search", style='dark-outline',
                                    command=lambda: search(city_entry.get()))
search_button.pack(pady=10)

location_label = ttkbootstrap.Label(root)
location_label.pack(side='top')

icon_label = ttkbootstrap.Label(root)
icon_label.pack(side='top', anchor='center')

temperature_frame = ttkbootstrap.Frame(root)
temperature_frame.pack(side='top', fill='x', pady=3)

temperature_label = ttkbootstrap.Label(temperature_frame)
temperature_label.pack(anchor='center')

description_label = ttkbootstrap.Label(temperature_frame)
description_label.pack(anchor='center')

feelslike_label = ttkbootstrap.Label(temperature_frame)
feelslike_label.pack()

weather_details_frame = ttkbootstrap.Frame(root)
weather_details_frame.pack(side='top', anchor='center', pady=15)

left_frame_weather_details = ttkbootstrap.Frame(weather_details_frame)
left_frame_weather_details.pack(side='left', padx=25)

right_frame_weather_details = ttkbootstrap.Frame(weather_details_frame)
right_frame_weather_details.pack(side='left', padx=25)

pressure_frame = ttkbootstrap.Frame(left_frame_weather_details)
pressure_frame.pack(side='top', pady=6)
wind_speed_frame = ttkbootstrap.Frame(left_frame_weather_details)
wind_speed_frame.pack(side='top', pady=6)

humidity_frame = ttkbootstrap.Frame(right_frame_weather_details)
humidity_frame.pack(side='top', pady=6)
visibility_frame = ttkbootstrap.Frame(right_frame_weather_details)
visibility_frame.pack(side='top', pady=6)

pressure_label = ttkbootstrap.Label(pressure_frame)
pressure_label.pack(side='top')

pressure_text_label = ttkbootstrap.Label(pressure_frame)
pressure_text_label.pack(side='top')

humidity_label = ttkbootstrap.Label(humidity_frame)
humidity_label.pack(side='top')

humidity_text_label = ttkbootstrap.Label(humidity_frame)
humidity_text_label.pack(side='top')

visibility_label = ttkbootstrap.Label(visibility_frame)
visibility_label.pack(side='top')

visibility_text_label = ttkbootstrap.Label(visibility_frame)
visibility_text_label.pack(side='top')

wind_label = ttkbootstrap.Label(wind_speed_frame)
wind_label.pack(side='top')

wind_text_label = ttkbootstrap.Label(wind_speed_frame)
wind_text_label.pack(side='top')


def search(city):
    city_entry.delete(0, END)
    city_entry.insert(0, '        Enter the city')
    result = get_weather(city)
    if result is None:
        return
    icon_url, temperature, feels_like, description, city, country, pressure, humidity, visibility, wind = result
    location_label.configure(text=f"{city}, {country}", font=("Helvetica", 15), foreground='black')
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon
    temperature_label.configure(text=f"{temperature}°C", font=("Helvetica", 14), foreground='black')
    description_label.configure(text=f"{description}", font=("Helvetica", 11), foreground='black')
    wind_label.configure(text=f"{wind} km/h", font=("Helvetica", 13), foreground='black')
    humidity_label.configure(text=f"{humidity}%", font=("Helvetica", 13), foreground='black')
    visibility_label.configure(text=f"{visibility} km", font=("Helvetica", 13), foreground='black')
    pressure_label.configure(text=f"{pressure} hPa", font=("Helvetica", 13), foreground='black')
    feelslike_label.configure(text=f"Feels Like {feels_like}°C", font=("Helvetica", 11), foreground='black')
    wind_text_label.configure(text="Wind Speed", font=("Helvetica", 10), foreground='black')
    visibility_text_label.configure(text="Visibility", font=("Helvetica", 10), foreground='black')
    humidity_text_label.configure(text="Humidity", font=("Helvetica", 10), foreground='black')
    pressure_text_label.configure(text="Pressure", font=("Helvetica", 10), foreground='black')


root.mainloop()
