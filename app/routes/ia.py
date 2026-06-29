from flask import Blueprint, render_template, request, session, redirect, url_for, flash
import joblib
import numpy as np
import os

ia_bp = Blueprint('ia', __name__)

MODEL_PATH = 'app/services/modelo_precio_ia.joblib'
modelo_ia = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None

@ia_bp.route('/predecir', methods=['GET', 'POST'])
def predecir_precio():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    precio_sugerido = None
    if request.method == 'POST':
        duracion = float(request.form.get('duracion'))
        valoracion = float(request.form.get('valoracion'))

        if modelo_ia:
            prediccion = modelo_ia.predict(np.array([[duracion, valoracion]]))
            precio_sugerido = round(float(prediccion[0]), 2)
    return render_template('ia/predict.html', resultado=precio_sugerido)

