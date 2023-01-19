import customtkinter
import scipy.cluster.hierarchy as shc
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.df = None
        self.dendrogramMethod = "complete"
        self.title("46171 projekt AAD")
        self.geometry("935x540")
        self.resizable(False, False)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebarFrame = customtkinter.CTkFrame(self)
        self.sidebarFrame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.title = customtkinter.CTkLabel(self.sidebarFrame, text="Program\n do generowania\ndendrogramow",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title.grid(row=0, column=0, padx=20, pady=15)

        self.openFileLabel = customtkinter.CTkLabel(self.sidebarFrame,
                                                    text="Wybierz plik:",
                                                    font=customtkinter.CTkFont(size=14, weight="bold"))
        self.openFileLabel.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.openFileButton = customtkinter.CTkButton(self.sidebarFrame,
                                                      text="Wybierz",
                                                      anchor="center",
                                                      command=self.openFile)
        self.openFileButton.grid(row=2, column=0, padx=20, pady=10)

        self.dendroOptionsLabel = customtkinter.CTkLabel(self.sidebarFrame,
                                                         text="Metoda dendrogramu:",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.dendroOptionsLabel.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.dendroOptionsMenu = customtkinter.CTkOptionMenu(self.sidebarFrame,
                                                             values=["complete", "ward", "single", "average", "weighted", "centroid", "median"],
                                                             anchor="center",
                                                             command=self.changeDendrogramMethod)
        self.dendroOptionsMenu.set("complete")
        self.dendroOptionsMenu.grid(row=4, column=0, padx=20, pady=10)

        self.genDendrogramLabel = customtkinter.CTkLabel(self.sidebarFrame,
                                                         text="Narysuj dendrogram:",
                                                         font=customtkinter.CTkFont(size=14, weight="bold"))
        self.genDendrogramLabel.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.genDendrogramButton = customtkinter.CTkButton(self.sidebarFrame,
                                                           text="Wygeneruj",
                                                           anchor="center",
                                                           state="disabled",
                                                           command=self.generateDendrogramButton)
        self.genDendrogramButton.grid(row=6, column=0, padx=20, pady=10)

        self.plotFrame = customtkinter.CTkFrame(self)
        self.plotFrame.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="nsew")

    def generateDendrogramButton(self):
        if self.df is not None:
            self.generateDendrogram(self.df, self.dendrogramMethod)

    def checkPath(self):
        dialog = customtkinter.filedialog.askopenfilename(filetypes=(("CSV Files", "*.csv"),))
        if dialog:
            print("Plik: ", dialog.title())
            return dialog.title()

    def openFile(self):
        try:
            self.df = pd.read_csv(self.checkPath())
            print(self.df)
            self.genDendrogramButton.configure(state="normal")
        except:
            print("Nie wczytano pliku")

    def changeDendrogramMethod(self, newDendrogramMethod: str):
        self.dendrogramMethod = newDendrogramMethod

    def generateDendrogram(self, file, dendrogramMethod: str):
        fig = Figure()
        fig.set_facecolor('#2b2b2b')
        plot = fig.add_subplot(111)
        shc.dendrogram(shc.linkage(file, method=dendrogramMethod), ax=plot)
        plot.set_facecolor("#2b2b2b")
        plot.set_title("Dendrogram")
        plot.set_xlabel("Nr instancji (wiersza)")
        plot.set_ylabel("Odleglosci euklidesowe")
        canvas = FigureCanvasTkAgg(fig, master=self.plotFrame)
        canvas.get_tk_widget().grid(row=0, column=0, padx=20, pady=15)
        canvas.draw()


if __name__ == "__main__":
    app = App()
    app.mainloop()
