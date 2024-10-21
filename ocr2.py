import cv2
import os
from tkinter import Tk, Label, Button
from PIL import Image, ImageTk
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Variables globales
capture_flag = False
cap = cv2.VideoCapture(0)

def capture_image():
    global capture_flag
    capture_flag = True
def process_frame():
    global capture_flag, cap
    ret, frame = cap.read()
    if ret:
        if capture_flag:
            capture_flag = False
            recognized = ""  # Reiniciar la variable recognized

            # Guardar la imagen temporalmente
            temp_image_path = "temp_image.jpg"
            cv2.imwrite(temp_image_path, frame)

            # Leer la imagen desde el archivo temporal
            with open(temp_image_path, "rb") as image_stream:
                read_response = computervision_client.read_in_stream(image_stream, raw=True)

            # Obtener la ubicación de la operación
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]

            # Esperar a que el análisis termine
            while True:
                read_result = computervision_client.get_read_result(operation_id)
                if read_result.status.lower() not in ['notstarted', 'running']:
                    break

            # Obtener el texto reconocido
            if read_result.status == 'succeeded':
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        recognized += line.text + " "

            # Eliminar la imagen temporal
            os.remove(temp_image_path)
            print(recognized)
            return recognized
    return None

def update_frame():
    global cap, camera_label
    ret, frame = cap.read()
    if ret:
        recognized = process_frame()
        if recognized:
            print(recognized)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Ensure the image exists before configuring the label
        if imgtk:
            camera_label.configure(image=imgtk)
            camera_label.imgtk = imgtk  # Keep a reference to avoid garbage collection
        else:
            print("Error: Image not loaded correctly.")
        
        camera_label.after(10, update_frame)

def camera():
    global cap, camera_label

    # Crear la interfaz gráfica
    root = Tk()
    root.title("Captura de Imagen")

    # Crear el label para mostrar la cámara
    camera_label = Label(root)
    camera_label.pack()

    # Crear el botón de captura
    capture_button = Button(root, text="📷", font=("Segoe UI Emoji", 24),
                            bg='#4cc2ff',
                            fg='#fff',
                            activebackground='lightblue',
                            borderwidth=0,
                            relief='flat',
                            width=11, command=capture_image)
    capture_button.pack(expand=True, fill='both')

    # Iniciar la actualización del frame después de que la interfaz gráfica esté completamente configurada
    root.after(10, update_frame)

    # Iniciar el bucle principal de la interfaz gráfica
    root.mainloop()

    # Liberar la cámara cuando se cierre la ventana
    cap.release()
    cv2.destroyAllWindows()