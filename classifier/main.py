"""
Offline inference
"""

from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

carpeta_local = "./mi_modelo_local"

# Cargar los componentes guardados localmente
tokenizer = AutoTokenizer.from_pretrained(carpeta_local)
model = AutoModelForSequenceClassification.from_pretrained(carpeta_local)

# Crear el pipeline pasando los objetos locales
classifier = pipeline("zero-shot-classification", model=model, tokenizer=tokenizer)

# Inferencia rápida sin conexión
oferta = "Buscamos un desarrollador Python con experiencia en Django."
texto_cv = "Experiencia de 3 años programando en Python y creando APIs con Django."
labels = ["apto para la posición", "posiblemente apto", "no apto para la posición"]

resultado = classifier(f"Oferta: {oferta}\nCV: {texto_cv}", candidate_labels=labels)

print(f"Resultado: {resultado['labels'][0]} ({resultado['scores'][0]:.2%})")
