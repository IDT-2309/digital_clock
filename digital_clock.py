from PIL import Image
from PIL import ImageTk
from pygame import mixer


from tkinter import Tk,Canvas, Button, Scale, Label, OptionMenu, StringVar
from time import strftime
from datetime import datetime
from json import load, dump
from pathlib import Path
from lunarcalendar import Converter, Solar

class Music:
    def __init__(self, on, volume):
        self.on = on
        self.volume = volume

class Animation:
    def __init__(self, speed):
        self.speed = speed
    
class Params:
    def __init__(self, value):
        self.value = value


def open_settings():
    f = open(path_json)
    settings_data = load(f)
    return settings_data

def save_settings(settings_data):
    with open(path_json, 'w') as f:
        dump(settings_data, f, indent=2)
    return

def month_format(month):
    return datetime.strptime(month, '%m').strftime('%b')


# DIRECTORY AND JSON PATH
working_directory = Path(__file__).parent
path_json = Path(working_directory, 'settings_db_tkinter.json')

# MIXER
mixer.init()



solar = strftime('%d-%m-%Y')
solar = solar.split('-')
solar = Solar(int(solar[2]), int(solar[1]), int(solar[0]))
lunar_date = Converter.Solar2Lunar(solar)
# convert lunar:  dd.mm.yyyy --> (dd.mm Lunar)

month_lunar = month_format(str(lunar_date.month))
month_solar = month_format(str(solar.month))

lunar_date = f"({lunar_date.day} {month_lunar} Lunar)"
solar_date = f"{solar.day} {month_solar} {solar.year}"



# MAIN
def main():

    def load_info():
        settings_data = open_settings()
        theme_selected = settings_data['theme_selected']                                  
        selected_theme_folder = settings_data['themes'][theme_selected]
        return settings_data, theme_selected, selected_theme_folder


    def time_display():
        # TIME
        hours_and_mins = strftime('%H:%M')
        seconds = strftime(':%S')
        # TOP
        canvas.itemconfig(hours_and_mins_display, text=hours_and_mins)
        canvas.itemconfig(seconds_display, text=seconds)
        # BACK - "SHADOW"
        canvas.itemconfig(hours_and_mins_display_2nd, text=hours_and_mins)
        canvas.itemconfig(seconds_display_2nd, text=seconds)
        # CALLBACK
        canvas.after(1000, lambda:time_display())


    # MUSIC
    def music_stop():
        mixer.music.fadeout(0)


    def music_load_play():
        mixer.music.load(Path(working_directory, 'themes', theme_selected, 'music.mp3'))
        mixer.music.set_volume(music.volume)
        mixer.music.play(loops=-1)


    def music_switch_on_off():
        
        settings_data, theme_selected, selected_theme_folder = load_info()
        
        # MUSIC ON --> OFF
        if settings_data['music_on']:
            music_stop()
            settings_data['music_on'] = False
            sound_button.configure(image=button_image_start)

        # MUSIC OFF --> ON
        else:
            music_load_play()
            settings_data['music_on'] = True
            sound_button.configure(image=button_image_stop)

        selected_theme_folder['music_volume'] = music.volume
        save_settings(settings_data)


    # IMAGE CREATION - resizable
    def image_generate(image_size, picture_name):   
        my_img_path = Path(working_directory, 'themes', 'img', picture_name)
        my_img = Image.open(my_img_path)
        width = int(image_size)
        height = int(image_size)
        resized_image = my_img.resize((width, height))
        photo = ImageTk.PhotoImage(resized_image)
        return photo

    
    # JSON / SETTINGS / theme - LOAD INFO
    settings_data, theme_selected, selected_theme_folder = load_info()

    # MUSIC
    music = Music(settings_data['music_on'], selected_theme_folder['music_volume'])

    # ANIMATION
    count = 0
    animation = Animation(selected_theme_folder['animation_speed'])  # 1000 = 1 sec

    # BUTTONS
    button_bg_color = selected_theme_folder['button_bg_color']
    button_bg_color_clicked = selected_theme_folder['button_bg_color_clicked']
    button_pos_x = selected_theme_folder['button_pos_x']
    button_pos_y = selected_theme_folder['button_pos_y']

    # TIME
    time_font_color = selected_theme_folder['time_font_color']
    time_font_style = selected_theme_folder['time_font_style']
    hour_minute_font_size = selected_theme_folder['hour_minute_font_size']
    second_font_size = selected_theme_folder['second_font_size']

    # HOURS & MINUTES
    hour_minute_pos_x = selected_theme_folder['hour_minute_pos_x']
    hour_minute_pos_y = selected_theme_folder['hour_minute_pos_y']

    # SECONDS
    second_pos_x = selected_theme_folder['second_pos_x']
    second_pos_y = selected_theme_folder['second_pos_y']

    #Date
    time_date_pos_x = selected_theme_folder['date_pos_x']
    time_date_pos_y = selected_theme_folder['date_pos_y']
    time_date_font_color = selected_theme_folder['date_font_color']
    time_date_font_style = selected_theme_folder['date_font_style']
    time_date_font_size = selected_theme_folder['date_font_size']


    # CANVAS 2nd - SETTINGS
    canvas_settings_orentation = selected_theme_folder['canvas_settings_orentation']
    canvas_settings_pos_x_diff = selected_theme_folder['canvas_settings_pos_x_diff']



    # WINDOW
    window = Tk()
    window.title(selected_theme_folder['window_title'])
    window_width = 735 + 2
    window_high = 420 +2
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f'{window_width}x{window_high}+%d+%d' % (screen_width/2, screen_height-window_high-80))
    window.resizable(0,0)   # locks the main window
    

    # CANVAS
    canvas = Canvas(
        window,
        width=window_width,
        height=window_high)
    canvas.place(x=0,y=0)
    # BASE IMAGE FOR ANIMATION
    image_display = canvas.create_image((0,0))


    # ANIMATION
    def img_seq_creation(scale_factor):
        path_gif = Path(working_directory, 'themes', theme_selected, 'GIF.GIF')
        gif_image = Image.open(path_gif)
        frames_count_all = gif_image.n_frames

        images_list = []

        for i in range(frames_count_all):
            # Load each frame
            gif_image.seek(i)
            frame = gif_image.copy()
            # Resize the frame
            scaled_frame = frame.resize((int(frame.width * scale_factor), int(frame.height * scale_factor)), Image.Resampling.LANCZOS)
            # Convert to PhotoImage and add to the list
            images_list.append(ImageTk.PhotoImage(scaled_frame))
        return images_list, frames_count_all

    # Example usage with a scale factor of 2 (doubling the size)
    scale_factor = 1.5
    
    images_list, frames_count_all = img_seq_creation(scale_factor)

    def animation_func(animation_param, count):
        image_next = images_list[count]
        canvas.itemconfig(image_display, image=image_next, anchor='nw')
        count += 1
        if count == frames_count_all:
            count = 0
        # CALLBACK
        canvas.after(animation.speed, lambda: animation_func(animation_param, count))





    ## TIME
    re_pos = 2  # for the "shadows"
    # BACK
    # anchor = se/sw -> changing time size(11<55): will no overlapping or too far from eachother
    hours_and_mins_display_2nd = canvas.create_text(
        (hour_minute_pos_x + re_pos, hour_minute_pos_y + re_pos),
        text=strftime('%H:%M'),
        font=(time_font_style, hour_minute_font_size, 'bold'),
        fill='black',
        anchor='se')
    seconds_display_2nd = canvas.create_text(
        (second_pos_x + re_pos, second_pos_y + re_pos),
        text=strftime(':%S'),
        font=(time_font_style, second_font_size, 'bold'),
        fill='black',
        anchor='sw')
    # TOP
    hours_and_mins_display = canvas.create_text(
        (hour_minute_pos_x, hour_minute_pos_y),
        text=strftime('%H:%M'),
        font=(time_font_style, hour_minute_font_size, 'bold'),
        fill=time_font_color,
        anchor='se')
    seconds_display = canvas.create_text(
        (second_pos_x, second_pos_y),
        text=strftime(':%S'),
        font=(time_font_style, second_font_size, 'bold'),
        fill=time_font_color,
        anchor='sw')
    
    ## solar 
    date_display = canvas.create_text(
        (time_date_pos_x, time_date_pos_y),
        text=solar_date,
        font=(time_date_font_style, time_date_font_size, 'bold'),
        fill=time_date_font_color,
        anchor='nw')

    ## lunar date
    
    date_display = canvas.create_text(
        (time_date_pos_x , time_date_pos_y + 40),
        text= lunar_date,
        font=(time_date_font_style, time_date_font_size - 5, 'normal'),
        fill=time_date_font_color,
        anchor='nw')

    ## BUTTONS - ON THE MAIN WINDOW
    pos_y_diff = 33

    # SETTINGS BUTTON
    button_image_settings = image_generate(21, 'settings.png')
    Button(
        canvas,
        command=lambda:[canvas_launcher()], 
        image = button_image_settings,
        background=button_bg_color,
        activebackground=button_bg_color_clicked
        ).place(x=button_pos_x, y=button_pos_y)


    # MUSIC BUTTON
    button_image_start = image_generate(20, 'start.png')
    button_image_stop = image_generate(20, 'stop.png')
    if music.on:
        music_start_stop_img = button_image_stop
    else:
        music_start_stop_img = button_image_start
    sound_button = Button(canvas,
                text='sound',
                command=lambda:[music_switch_on_off()], 
                image = music_start_stop_img,
                background=button_bg_color,
                activebackground=button_bg_color_clicked)
    sound_button.place(x=button_pos_x, y=button_pos_y + pos_y_diff)



    '''
    CANVAS - FOR THE SETTINGS WINDOW, TRIGGERED BY THE SETTINGS BUTTON
    '''
    # CANVAS COUNTER, LAUNCHER
    canvas_launched = Params(False)
    def canvas_launcher():      # command of the SETTINGS button
        if canvas_launched.value:
            pass
        else:
            display_canvas_settings()
            canvas_launched.value = True

    # def get_gif_size()


    # DISPLAY CANVAS
    def display_canvas_settings():
        # CANVAS
        canvas_settings_width = 300
        canvas_settings_height = 200
        canvas_settings = Canvas(
            window,
            background=button_bg_color,
            highlightthickness=3,
            highlightbackground='black',
            width=canvas_settings_width,
            height=canvas_settings_height)
        canvas_settings.place(
            x=button_pos_x+canvas_settings_pos_x_diff,
            y=button_pos_y-3,
            anchor=canvas_settings_orentation)
        

        # CLOSE BUTTON
        Button(
            canvas_settings,
            image=button_image_close,
            command=lambda:[close_canvas_settings()],
            background=button_bg_color,
            activebackground=button_bg_color_clicked
            ).place(x=canvas_settings_width-30, y=15)



        ## SLIDERS
        slider_width = 13
        # VOLUME SLIDER
        volume_slider = Scale(
            canvas_settings,
            from_=0,
            to=10,
            length=190,
            width=slider_width,
            background=button_bg_color,
            activebackground=button_bg_color,
            troughcolor=button_bg_color_clicked,
            highlightthickness=0,
            orient='horizontal',
            showvalue=False
            )
        volume_slider.set(music.volume*10)
        volume_slider.place(x=60, y=40)


        def volume_slider_update(music_volume_param):       
            # GET LATEST VALUE
            volume_slider_value = volume_slider.get()/10
            
            # UPDATE VOLUME, WHEN THERE IS A CHANGE IN SLIDER POSITION/VALUE
            if volume_slider_value != music_volume_param:     
                mixer.music.set_volume(volume_slider_value)
                music_volume_param = volume_slider_value
                music.volume = volume_slider_value
            
            # CALLBACK
            canvas_settings.after(50, lambda: volume_slider_update(music_volume_param))    # 1000 = 1 sec
        
        volume_slider_update(music.volume)

        
        # ANIMATION SPEED SLIDER
        animation_slider = Scale(
            canvas_settings,
            from_=200,
            to=10,
            length=190,
            width=slider_width,
            background=button_bg_color,
            activebackground=button_bg_color,
            troughcolor=button_bg_color_clicked,
            highlightthickness=0,
            orient='horizontal',
            showvalue=False)
        animation_slider.set(animation.speed)
        animation_slider.place(x=60, y=90)

        def animation_speed_update():
            animation.speed=animation_slider.get()
            # CALLBACK
            canvas_settings.after(50, lambda:animation_speed_update())
        
        animation_speed_update()


        # CHANGE theme, TRIGGERED BY THE theme OPTIONMENU SELECTION
        def change_theme(__):
            for selected_title in themes_dic:
                
                # SELECTED TITLE(Back to the Future I.) --> FOLDER NAME(back_to_the_future) = theme_selected
                if themes_dic[selected_title]['title'] == themes_roll_down_clicked.get():
                    
                    # LOAD INFO
                    settings_data, theme_selected, selected_theme_folder = load_info()
                    
                    # SAVING CURRENT SETTINGS AND THE NEWLY SELECTED theme
                    selected_theme_folder['music_volume'] = music.volume
                    selected_theme_folder['animation_speed'] = animation.speed
                    settings_data['theme_selected'] = music.on
                    settings_data['theme_selected'] = selected_title
                    save_settings(settings_data)
                    
                    # CANCEL MUSIC, WINDOW
                    music_stop()
                    window.destroy()
                    
                    # CANCEL CALLBACKS - time, volume, animation
                    for after_id in window.eval('after info').split():
                        window.after_cancel(after_id)
                    
                    # RELAUNCH MAIN
                    main()


        
        # LIST OF MOVIE TITLES
        themes_dic = settings_data['themes']
        themes_options = []
        for _ in themes_dic:
            themes_options.append(settings_data['themes'][_]['title'])

        
        # OPTION MENU
        themes_roll_down_clicked = StringVar()
        themes_roll_down_clicked.set(themes_dic[theme_selected]['title'])
        themes_roll_down = OptionMenu(
            canvas_settings,
            themes_roll_down_clicked,
            *themes_options,
            command=change_theme)
            # ROLL DOWN - BUTTON
        themes_roll_down.configure(
            font=(None, 10, 'bold'),
            foreground=button_bg_color_clicked,
            activeforeground = button_bg_color,
            background=button_bg_color,
            activebackground=button_bg_color_clicked,
            highlightbackground=button_bg_color)
        
        # ROLL DOWN - MENU
        themes_roll_down['menu'].configure(
            font=(None, 10, 'bold'),
            activeborderwidth=9,
            foreground=button_bg_color_clicked,
            activeforeground=button_bg_color,
            background=button_bg_color,
            activebackground=button_bg_color_clicked)
        themes_roll_down.place(x=60, y=130)
    


        # CLOSE CANVAS
        def close_canvas_settings():
            settings_data, theme_selected, selected_theme_folder = load_info()
            selected_theme_folder['music_volume'] = music.volume
            selected_theme_folder['animation_speed'] = animation.speed
            save_settings(settings_data)
            canvas_launched.value = False
            canvas_settings.destroy()
        

        ## DISPLAY IMAGES
        # VOLUME IMAGE
        Label(canvas_settings,image=image_volume, background=button_bg_color).place(x=15, y=30)
        
        # ANIMATION SPEED IMAGE
        Label(canvas_settings,image=image_animation_speed, background=button_bg_color).place(x=15, y=80)

        # theme SWITCH IMAGE
        Label(canvas_settings,image=image_theme_switch, background=button_bg_color).place(x=13, y=125)


    # IMAGE GENERATION FOR SETTINGS WINDOW(CANVAS)
    image_volume = image_generate(30, 'volume.png')
    image_animation_speed = image_generate(30, 'animation_speed.png')
    image_theme_switch = image_generate(37, 'theme_switch.png')
    button_image_close = image_generate(15, 'close.png')


    # FUNCTIONS
    time_display()
    animation_func(animation.speed, count)
    if music.on: music_load_play()
    

    window.mainloop()


if __name__ == "__main__":
    main()