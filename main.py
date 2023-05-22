import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import load as l
import ope

class Program:
    author1 = "Jakub Grzesiak"
    author2 = "Sebastian Szymański"
    author3 = "Jakub Wiśniewski"
    author4 = "Filip Kulas"
    author5 = "Igor Mielczarek"
    version = "4.2.6"

model1, class_to_idx = l.load_checkpoint("checkpoints/checkpoint_ing.pth")
model2, class_to_idx = l.load_checkpoint("checkpoints/Checkpoint_4_15_epoch.pth")
model3, class_to_idx = l.load_checkpoint("checkpoints/Checkpoint_3_15_epoch_recursive.pth")


class_names = ['0', '1', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '2', '20', '3', '4', '5', '6', '7', '8', '9']


def predykcja_obrazu():
    try:
        path_to_image = imageEntry.get()
        pass_count = 0
        prediction = {}
        # image based predictions
        try:
            probs, classes = l.predict2(path_to_image, model1.to(l.device))
            res_x = dict(zip(classes, probs))
            print(f"Alg IMG: {res_x}")
            for key in res_x.keys():
                if key in prediction.keys():
                    prediction[key] += res_x[key]
                else:
                    prediction[key] = res_x[key]
            pass_count += 1
        except Exception as ex:
            print(ex)
            pass

        # paragraph based predictions
        try:
            par_img = "assets/par_predict.jpg"
            ope.start(path_to_image, 4, par_img)
            probs, classes = l.predict2(par_img, model2.to(l.device))
            res_x = dict(zip(classes, probs))
            print(f"Alg PARAGRAPH: {res_x}")
            for key in res_x.keys():
                if key in prediction.keys():
                    prediction[key] += res_x[key]
                else:
                    prediction[key] = res_x[key]
            pass_count += 1
        except Exception as ex:
            print(ex)
            pass

        # line based predictions
        try:
            line_img = "assets/line_predict.jpg"
            ope.start(path_to_image, 3, line_img)
            probs, classes = l.predict2(line_img, model3.to(l.device))
            res_x = dict(zip(classes, probs))
            print(f"Alg TEXTLINE: {res_x}")
            for key in res_x.keys():
                if key in prediction.keys():
                    prediction[key] += res_x[key]
                else:
                    prediction[key] = res_x[key]
            pass_count += 1
        except Exception as ex:
            print(ex)
            pass

        if not prediction:
            raise Exception

        # Divide predictions over its count
        for key in prediction.keys():
            prediction[key] /= pass_count

        print([(l.cat_to_name[str(v)], prediction[v]) for v in prediction.keys()])
        max_prob = max(prediction, key=prediction.get)
        res = str(round(float(prediction[max_prob] * 100))) + "%"
        resultLabel.configure(text=f"Accuracy: {res}, Predicted document type: {l.cat_to_name[str(max_prob)]}", text_color="green")
    except:
        resultLabel.configure(text="Failed to analyze document", text_color="red")

def openImage():
    imageEntry.delete(0,ctk.END)
    openedImage = filedialog.askopenfilename(title="Select a file", filetypes=[("Images", "*.*")])
    imageEntry.insert(0, openedImage)
    # imageImage._light_image = open(openedImage)
    photo = Image.open(openedImage)
    photo.show()

def RunStartMenu():
    root.withdraw()
    startRoot.deiconify()


def RunInfo():
    root.withdraw()
    infoRoot.deiconify()


def StartBack():
#    startRoot.destroy()
    startRoot.withdraw()
    root.deiconify()


def InfoBack():
#    infoRoot.destroy()
    infoRoot.withdraw()
    root.deiconify()


if __name__ == '__main__':
    # MAIN
    import os
    ctk.set_default_color_theme("green")
    root = ctk.CTk()

    w = 600
    h = 400
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    root.title("ByteXpertise document classification")
    root.resizable(False, False)
    curr_path = os.getcwd()



    menuButton1 = ctk.CTkButton(root, text="Start", command=RunStartMenu)
    menuButton4 = ctk.CTkButton(root, text="About", command=RunInfo)
    menuButton5 = ctk.CTkButton(root, text="Exit", command=exit)

    menuButton1.place(relx=0.6, rely=0.3)
    menuButton4.place(relx=0.6, rely=0.45)
    menuButton5.place(relx=0.6, rely=0.6)

    # START

    startRoot = ctk.CTk()

    w = 1080
    h = 720
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    startRoot.geometry('%dx%d+%d+%d' % (w, h, x, y))

    startRoot.title("ByteXpertise document classification")
    startRoot.resizable(False, False)

    imageLabel = ctk.CTkLabel(startRoot, text="Enter image path:")
    imageEntry = ctk.CTkEntry(startRoot, width=980)
    resultLabel = ctk.CTkLabel(startRoot, text="")
    # imageImage = ctk.CTkImage(Image.open("C:/Users/SRQar/PycharmProjects/HackING/assets/temp.png"), size=(400, 400))
    # imageImageLabel = ctk.CTkLabel(startRoot, image=imageImage, text="")
    backButton = ctk.CTkButton(startRoot, text="Back", command=StartBack)
    openImageButton = ctk.CTkButton(startRoot, text="Choose file", command=openImage, width=40)
    startButton = ctk.CTkButton(startRoot, text="Start", command=predykcja_obrazu, width=85)
    imageLabel.place(relx=0.45, rely=0.05)
    # imageImageLabel.place(relx=0.05, rely=0.2)
    imageEntry.place(relx=0.045, rely=0.12)
    backButton.place(relx=0.45, rely=0.85)
    startButton.place(relx=0.87, rely=0.20)
    openImageButton.place(relx=0.045, rely=0.20)
    resultLabel.place(relx=0.37, rely=0.8)

    # INFO

    infoRoot = ctk.CTk()

    w = 600
    h = 400
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    infoRoot.geometry('%dx%d+%d+%d' % (w, h, x, y))

    infoRoot.title("ByteXpertise document classification")
    infoRoot.geometry("600x400")
    infoRoot.resizable(False, False)

    authorLabel = ctk.CTkLabel(infoRoot, text=f"Authors: {Program.author1}, {Program.author2}, {Program.author3}, {Program.author4}, {Program.author5}")
    versionLabel = ctk.CTkLabel(infoRoot, text=f"Version: {Program.version}")
    BackButtoni = ctk.CTkButton(infoRoot, text="Back", command=InfoBack)
    authorLabel.place(relx=0.05, rely=0.35)
    versionLabel.place(relx=0.42, rely=0.46)
    BackButtoni.place(relx=0.39, rely=0.71)

    root.mainloop()
