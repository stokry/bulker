import tkinter as tk
from threading import Thread
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from PIL import ImageTk, Image
from tkinter.ttk import Progressbar
from tkinter import messagebox
import face_recognition
import os
ss


class FaceApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("900x800")
        self.resizable(True, True)
        self.title('Bulker')
        row = tk.Frame(self)
        lab = tk.Label(row, width=5, text="Image : ", anchor='w')
        self._file_field = tk.Entry(row)
        self._file_open_btn = tk.Button(row, text='Find',
                                        command=lambda: self.load_file())
        row1 = tk.Frame(self)
        lab1 = tk.Label(row1, width=5, text="Folder : ", anchor='w')
        self._folder_field = tk.Entry(row1)
        self._folder_open_btn = tk.Button(row1, text='Open',
                                          command=lambda: self.load_folder())

        self._image_panel = tk.Frame(self)

        bottom_row = tk.Frame(self)
        self._start_btn = tk.Button(bottom_row, text='Start',
                                    command=lambda: self.run_process())
        self._progress = Progressbar(bottom_row, orient=tk.HORIZONTAL, length=500, mode='determinate')

        lab.pack(side=tk.LEFT, padx=30)
        self._file_field.pack(side=tk.LEFT, ipadx=250)
        self._file_open_btn.pack(side=tk.LEFT, ipadx=10, padx=10)
        row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        lab1.pack(side=tk.LEFT, padx=30)
        self._folder_field.pack(side=tk.LEFT, ipadx=250)
        self._folder_open_btn.pack(side=tk.LEFT, ipadx=10, padx=10)
        row1.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        self._image_panel.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        self._start_btn.pack(side=tk.BOTTOM, ipadx=10, padx=10)
        self._progress.pack(side=tk.BOTTOM, pady=5)
        bottom_row.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

    def load_file(self):
        filename = askopenfilename()
        self._file_field.delete(0, tk.END)  # deletes the current value
        self._file_field.insert(0, filename)
        for widget in self._image_panel.winfo_children():
            widget.destroy()

        img = ImageTk.PhotoImage(Image.open(filename))
        panel = tk.Label(self._image_panel, image=img)
        panel.img = img
        panel.pack(side="bottom", fill="both", expand="yes")

    def load_folder(self):
        filename = askdirectory()
        self._folder_field.delete(0, tk.END)  # deletes the current value
        self._folder_field.insert(0, filename)

    def start_process(self):
        ref_path = self._file_field.get()
        folder_path = self._folder_field.get()
        self.find_and_delete(folder_path, ref_path)

    def run_process(self):
        self._run_task = True
        t = Thread(target=self.start_process)
        t.start()

    def find_and_delete(self, directory, ref_image_path):
        ref_face = self.get_ref_face(ref_image_path)
        if ref_face is None:
            messagebox.showinfo("Error", "Can't find a face. Reference Image quality is not enough")
            return
        files = os.listdir(directory)
        i = 1
        for filename in files:
            try:
                percentage = int((i / len(files)) * 100)
                self._progress['value'] = percentage
                self.update_idletasks()
                i += 1
                file_path = os.path.join(directory, filename)
                if self.is_user_in_image(ref_face, file_path):
                    os.remove(file_path)
                    print(filename, 'deleted.')
            except:
                print('Error reading file', filename)
        messagebox.showinfo("Information", "Process Finished")

    def get_ref_face(self, ref_image_path):
        try:
            ref_image = face_recognition.load_image_file(ref_image_path)
            ref_face = face_recognition.face_encodings(ref_image)[0]
            return ref_face
        except:
            return None


    def is_user_in_image(self, ref_face, image_path):
        unknown_picture = face_recognition.load_image_file(image_path)
        unknown_faces = face_recognition.face_encodings(unknown_picture)

        for unknown_face in unknown_faces:
            results = face_recognition.compare_faces([ref_face], unknown_face)
            if results[0]:
                return True

        return False


if __name__ == "__main__":
    app = FaceApp()
    app.mainloop()
