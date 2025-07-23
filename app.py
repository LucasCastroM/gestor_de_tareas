import json
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

tareas = []
siguiente_id = 1

def guardar_datos():
    with open('tareas.json', 'w') as f:
        json.dump({'siguiente_id': siguiente_id, 'tareas': tareas}, f)

def cargar_datos():
    global siguiente_id, tareas
    try:
        with open('tareas.json', 'r') as f:
            data = json.load(f)
            tareas = data['tareas']
            siguiente_id = data['siguiente_id']
    except FileNotFoundError:
        pass  # Si el archivo no existe, no hace nada

# Cargar datos al iniciar el programa
cargar_datos()

def agregar_tarea(texto):
    global siguiente_id
    tareas.append({'id': siguiente_id, 'texto': texto, 'completado': False})
    siguiente_id += 1
    guardar_datos()

def completar_tarea(id):
    for tarea in tareas:
        if tarea['id'] == id:
            tarea['completado'] = True
            guardar_datos()
            break

@app.route('/')
def index():
    tareas_ordenadas = sorted(tareas, key=lambda t: t['completado'])
    return render_template('index.html', tareas=tareas_ordenadas)

@app.route('/agregar', methods=['POST'])
def agregar():
    texto_area = request.form['texto_tarea']
    if texto_area:
        agregar_tarea(texto_area)
    return redirect('/')

@app.route('/completar/<int:id>')
def completar(id):
    completar_tarea(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
