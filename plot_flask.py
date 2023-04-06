from flask import Flask, render_template, Response, request
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from wsgiref.handlers import CGIHandler
from flaskapp import create_app


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/plot.png')
def plot_png():
    fig = create_figure(np.linspace(0, 15, 200))
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure(x):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    #x = np.linspace(0, 10, 100)
    y = np.sin(x)
    axis.plot(x, y)
    return fig

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        # Hole die ausgewählten X-Werte aus dem Formular
        x_values = request.form.getlist('x_values')
        x_values = list(map(int, x_values))

        # Generiere die Grafik mit den ausgewählten X-Werten
        y_values = [x**2 for x in x_values]
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x_values, y_values)
        ax.set_xlabel('X values')
        ax.set_ylabel('Y values')
        ax.set_title('Grafik mit ausgewählten X-Werten')
        plt.tight_layout()

       # Erstelle ein FigureCanvas-Objekt aus der Grafik
        canvas = FigureCanvas(fig)

        # Rendere die Grafik als PNG-Datei im Speicher
        png_output = io.BytesIO()
        FigureCanvas(fig).print_png(png_output)
        canvas.print_png(png_output)
        png_output.seek(0)
        img_bytes = base64.b64encode(png_output.getvalue()).decode('utf-8')
        # Rendere die HTML-Vorlage mit der Grafik
        return render_template('graph.html', img_bytes=img_bytes)
    else:
        # Wenn keine X-Werte ausgewählt wurden, zeige die Index-Seite an
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
