import customtkinter as ctk
import tkinter
import tkinter as tk
from PIL import ImageTk, Image
import webbrowser
import qrcode
import requests
from bs4 import BeautifulSoup


class Movie(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.movie_list = []
        self.frame_name = []
        self.label_date = []
        self.label_title = []
        self.button_play = []
        self.no_data = False

        self.selected_server = "xyz"
        self.gen = ""

        ctk.set_appearance_mode("light")

        self.geometry("900x625")
        self.minsize(900, 625)
        self.maxsize(900, 625)
        self.title("StreaMovie")
        self.iconbitmap("icon.ico")

        self.frame_canvas = ctk.CTkFrame(self, fg_color="#ebebeb", width=135, height=135)
        self.frame_canvas.place(x=700, y=150)

        self.qr_canvas = tk.Canvas(self.frame_canvas, width=135, height=135)

        self.block = ctk.CTkLabel(self, text="")
        self.block.pack(pady=35)

        self.entry = ctk.CTkEntry(self, placeholder_text="Research for a movie, a tv show, a series...", width=400,
                                  height=40, font=("Helvetica", 15), corner_radius=25)
        self.entry.pack(pady=5)

        self.button_search = ctk.CTkButton(self.entry, text="Search", width=15, height=28, corner_radius=25,
                                           font=("Helvetica", 13), fg_color="#1D64D8", hover_color='#164797',
                                           command=self.search)
        self.button_search.place(x=320, y=6)

        self.open = Image.open("bouton play.png")
        self.image_button_play = ctk.CTkImage(self.open, size=(50, 50))

        self.frame_error_404 = ctk.CTkFrame(self, fg_color="#ebebeb", width=485, height=300)

        self.open_image = Image.open("image_viceversa_404.png")
        self.image_404 = ctk.CTkImage(self.open_image, size=(450, 250))
        self.label_image_404 = ctk.CTkLabel(self.frame_error_404, image=self.image_404, text="", width=100)

        self.dont_cry_label = ctk.CTkLabel(self.frame_error_404, text="Awww...Don't Cry.", font=("Helvetica", 20, "bold"),
                                           text_color="black")
        self.error_404 = ctk.CTkLabel(self.frame_error_404, text="It's just a 404 Error!", font=("Helvetica", 13), text_color="black")
        self.reference_viceversa = ctk.CTkLabel(self.frame_error_404, text="What you're looking for may have been misplaced\nin Long Term Memory",
                                                font=("Helvetica", 13), text_color="black")

        self.label_image_404.place(x=0, y=25)
        self.dont_cry_label.place(x=250, y=90)
        self.error_404.place(x=275, y=130)
        self.reference_viceversa.place(x=195, y=170)

        self.label_strea = ctk.CTkLabel(self, text="Strea", text_color="#1D64D8", font=("League Gothic", 37))
        self.m = ctk.CTkLabel(self, text="M", text_color="#D8201D", font=("League Gothic", 37))
        self.ovie = ctk.CTkLabel(self, text="ovie", text_color="#1D64D8", font=("League Gothic", 37))
        self.label_strea.place(x=350, y=40)
        self.m.place(x=435, y=40)
        self.ovie.place(x=465, y=40)

        self.looking_for_label = ctk.CTkLabel(self, text="You are looking for :", font=("Helvetica", 17))
        self.looking_for_label.place(x=50, y=109)

        self.radio_var = ctk.StringVar(value="movie")

        self.radio_button_movie = ctk.CTkRadioButton(self, text="Movies", value="movie", variable=self.radio_var,
                                                     font=("Helvetica", 15), fg_color="#D8201D",
                                                     border_color="#1D64D8", hover_color="#164797")
        self.radio_button_tv = ctk.CTkRadioButton(self, text="Tv Shows/Series", value="tv", variable=self.radio_var,
                                                  font=("Helvetica", 15), fg_color="#D8201D", border_color="#1D64D8",
                                                  hover_color="#164797", )

        self.radio_button_movie.place(x=50, y=150)
        self.radio_button_tv.place(x=50, y=180)

        self.server1 = ctk.CTkButton(self, fg_color="#D8201D", text="Serveur 1", height=40, corner_radius=20,
                                     font=('Helvetica', 18), hover_color='#AA1917',
                                     command=lambda: self.change_server(self.server1, self.server2, self.server3))
        self.server2 = ctk.CTkButton(self, fg_color="#1D64D8", text="Serveur 2", height=40, corner_radius=20,
                                     font=('Helvetica', 18), hover_color='#164797',
                                     command=lambda: self.change_server(self.server2, self.server1, self.server3))
        self.server3 = ctk.CTkButton(self, fg_color="#1D64D8", text="Serveur 3", height=40, corner_radius=20,
                                     font=('Helvetica', 18), hover_color='#164797',
                                     command=lambda: self.change_server(self.server3, self.server1, self.server2))

        self.server1.place(x=50, y=250)
        self.server2.place(x=50, y=310)
        self.server3.place(x=50, y=370)

    def change_server(self, server_clicked, server_descatived_1, server_descatived_2):
        if server_clicked.cget("fg_color") == '#D8201D':
            pass
        else:
            server_clicked.configure(fg_color="#D8201D", hover_color='#AA1917')
            server_descatived_1.configure(fg_color="#1D64D8", hover_color='#164797')
            server_descatived_2.configure(fg_color="#1D64D8", hover_color='#164797')
            if server_clicked == self.server1:
                self.selected_server = "xyz"
                self.gen = ""
            elif server_clicked == self.server2:
                self.selected_server = "in"
                self.gen = ""
            else:
                self.selected_server = "cc"
                self.gen = "/v2"

    def search(self):
        choose = self.radio_var.get()
        self.frame_canvas.place_forget()
        for i, suggestions in enumerate(self.frame_name):
            self.frame_name[i].pack_forget()
        self.movie_list = []
        url = 'https://www.themoviedb.org/search?query='
        input_ = self.entry.get()
        counte = input_.count("'")
        if counte == 0:
            change = input_.replace(" ", "+")
            self.get_all(url, change, choose)
            self.place_suggestions()
        else:
            change = input_.replace("'", "%27").replace(" ", "+")
            self.get_all(url, change, choose)
            self.place_suggestions()

    def get_all(self, url_, change_, data_type_choose):
        url_final = url_ + change_
        page = requests.get(url_final)
        soup = BeautifulSoup(page.text, "html.parser")
        find_media_type_code_tmdb = soup.find_all("a", class_="result")
        all_movie = str(find_media_type_code_tmdb).split("/h2></a>, <")
        for i, movie in enumerate(all_movie):
            if len(self.movie_list) <= 4:
                try:
                    begin = movie.index("data-media-type=")
                    end = movie.index(">")
                    precise = movie[begin:end]
                    separate = precise.split(" ")
                    data_media_type = separate[0].split("=")[1].replace('"', "")
                    if data_media_type != "movie" and data_media_type != "tv" or data_media_type != data_type_choose:
                        continue
                    code_tmdb = separate[1].split("=")[1].replace('"', "").split("/")[2].split("-")[0]
                    find_title_name = soup.find_all("h2")
                    title_name = find_title_name[i].text
                    find_release_date = soup.find_all("span", class_="release_date")
                    if len(str(find_release_date).split(', ')) <= i:
                        release_date = ''
                    else:
                        release_date = find_release_date[i].text.strip()
                    punctuation = '§ '
                    self.movie_list.append(
                        title_name + punctuation + release_date + punctuation + data_media_type + punctuation + code_tmdb)
                    self.no_data = False
                except ValueError:
                    self.no_data = True
        if not self.movie_list:
            self.no_data = True

    def place_suggestions(self):
        self.frame_name = []
        self.label_date = []
        self.label_title = []
        if self.no_data:
            self.frame_error_404.pack()
            self.frame_canvas.place_forget()
        else:
            self.frame_error_404.pack_forget()
            for i, suggestions in enumerate(self.movie_list):
                separate = suggestions.split("§")
                title = separate[0]
                if len(title) > 36:
                    first_line = title[0:37]
                    other_line = title[37:len(title)]
                    finish_line = f"{first_line}\n{other_line}"
                else:
                    finish_line = title
                date = separate[1].strip()
                data_media_type = separate[2].strip()
                code_tmdb = separate[3].strip()
                self.frame_name.append(f"frame_{i}")
                self.label_date.append(f"label_date_{i}")
                self.label_title.append(f"label_title{i}")
                self.button_play.append(f"button_play{i}")
                self.frame_name[i] = ctk.CTkFrame(self, height=80, width=400, fg_color="white", border_width=3,
                                                  border_color="#D8201D", corner_radius=15)
                self.label_title[i] = ctk.CTkLabel(self.frame_name[i], font=("Helvetica", 18), text_color="black", text=finish_line, height=30, fg_color="white", justify='left')
                self.label_date[i] = ctk.CTkLabel(self.frame_name[i], text=date, font=("Helvetica", 13), height=1)
                self.button_play[i] = ctk.CTkButton(self.frame_name[i], image=self.image_button_play, text="",
                                                    width=20, fg_color="white", hover_color="white", command=lambda codetmdb_=code_tmdb, data_media_type_=data_media_type: self.browse_url(codetmdb_, data_media_type_))

                self.button_play[i].place(x=330, y=10)
                self.label_date[i].place(x=15, y=52)
                self.label_title[i].place(x=15, y=10)
                self.frame_name[i].pack(pady=5)

    def browse_url(self, code_tmdb, media_type):
        if media_type == "movie":
            url = f'https://vidsrc.{self.selected_server}{self.gen}/embed/movie/{code_tmdb}'
        else:
            url = f'https://vidsrc.{self.selected_server}{self.gen}/embed/tv/{code_tmdb}'
        webbrowser.open_new(url)
        self.generate_qr_code(url)

    def generate_qr_code(self, url):
        if url:
            self.frame_canvas.place(x=700, y=150)
            self.frame_canvas.configure(border_width=5, border_color="white")
            self.qr_canvas.pack(fill=tkinter.BOTH)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=(216, 32, 29), back_color=(29, 100, 216))
            self.qr_canvas.delete("all")
            resize = img.resize((135, 135))
            tkimage = ImageTk.PhotoImage(resize)
            self.qr_canvas.create_image(0, 0, anchor=tk.NW, image=tkimage)
            self.qr_canvas.image = tkimage


app_movie = Movie()
app_movie.mainloop()
