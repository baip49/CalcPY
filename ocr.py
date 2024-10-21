import cv2
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def cam():
    # Inicializar la captura de imagen
    video = cv2.VideoCapture(0)

    # Esta variable deberá ser un string de Tkinter
    expresion = ''

    while True:
        ret, frame = video.read()
        if not ret:
            print("Error al capturar el frame")
            break

        cv2.imshow('Capturar imagen', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # Presionar barra espaciadora para leer texto
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
                        expresion += line.text + ' '

            # Eliminar la imagen temporal
            os.remove(temp_image_path)

            # Imprime el texto capturado
            print(expresion)

            # Reinicia la expresión
            # En este punto se debe llamar al método que calcula pasandole el string capturado
            video.release()
            cv2.destroyAllWindows()
            return expresion

        if key == ord('q') or key == 27:  # Presionar 'q' o 'ESC' para salir
            break

    video.release()
    cv2.destroyAllWindows()
    return expresion