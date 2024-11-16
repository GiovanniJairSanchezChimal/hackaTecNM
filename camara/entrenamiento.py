import os
from ultralytics import YOLO

# Ruta a tu archivo de configuración data.yml
data_file_path = os.path.join('C:/Users/ghost/Proyectos_Dev/hackaton/vigilanciaIA/camara/maizinfectado', 'data.yml')

# Inicializar el modelo YOLOv8
model = YOLO('yolov8n.yaml')  # Puedes ajustar el tamaño del modelo (nano, small, medium, etc.)

# Entrenar el modelo
model.train(data=data_file_path, epochs=200, imgsz=640, batch=16, name='maizinfectado_model')

# Guardar los pesos del modelo entrenado
model.save('C:/Users/ghost/Proyectos_Dev/hackaton/vigilanciaIA/camara/maizinfectado/weights/best.pt')
