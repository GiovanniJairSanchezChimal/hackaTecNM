# camara/views.py
from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect
import cv2
import re
import numpy as np
import pygame
from ultralytics import YOLO
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm

# Inicializar el modelo YOLO
model = YOLO('D:/Ghost/Hackaton/vigilanciaIA/camara/padi.pt')
pygame.mixer.init()

# Diccionario de nombres de clases
names = {
    0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck',
    8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench',
    14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear',
    22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase',
    29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat',
    35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass',
    41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich',
    49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair',
    57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop',
    64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster',
    71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
    78: 'hair dryer', 79: 'toothbrush'
}

def gen():
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detección de objetos
        resultados = model.predict(frame, imgsz=640)
        anotaciones = resultados[0].plot()

        for r in resultados:
            boxes = r.boxes.cpu().numpy()

        str_boxes = str(boxes)
        match = re.search(r'cls: array\(\[([\d\s\.,]+)\]', str_boxes)

        if match:
            cls_str = match.group(1)
            cls = np.fromstring(cls_str, sep=',', dtype=float)
        else:
            cls = np.array([])

        results_counts = {}
        for result_id in cls:
            if result_id in results_counts:
                results_counts[result_id] += 1
            else:
                results_counts[result_id] = 1

        final_name = []
        final_count = []
        for result_id, count in results_counts.items():
            if result_id in names:
                name = names[result_id]
                final_count.append(count)
                final_name.append(name)
                # Reproducir audio si se detecta una persona
                if name == 'person':
                    pygame.mixer.music.load('C:/Users/ghost/vigilanciaIA/camara/alarmaAlerta.mp3')
                    pygame.mixer.music.play()

        resultados = []
        for nombre, valor in zip(final_name, final_count):
            resultados.append(f'{valor}:{nombre}')

        texto_final = '\n'.join(resultados)
        #for i in resultados

        # Convertir frame anotado a JPEG
        ret, jpeg = cv2.imencode('.jpg', anotaciones)
        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    return redirect('video_stram.html', resultados = resultados)
    cap.release()

def video_stream(request):
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def video(request):

    return render(request, 'video_stream.html')

def index(request):
    return render(request, 'index.html')

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('index')

    return render(request, 'registration/register.html', data)
