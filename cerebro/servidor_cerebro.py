from flask import Flask, request, jsonify
from cerebro_mosca import estimular_cerebro, EVENTO_A_FRACCION

app = Flask(__name__)

@app.route('/estimular', methods=['POST'])
def estimular():
    data = request.get_json(force=True)
    tipo_evento = data.get('tipo_evento', 'comando_simple')

    if tipo_evento not in EVENTO_A_FRACCION:
        tipo_evento = 'comando_simple'

    resultado = estimular_cerebro(tipo_evento)
    return jsonify(resultado)

@app.route('/salud', methods=['GET'])
def salud():
    return jsonify({'status': 'ok', 'eventos_disponibles': list(EVENTO_A_FRACCION.keys())})

if __name__ == '__main__':
    print(">>> Servidor del cerebro de la mosca iniciando en puerto 5000...")
    app.run(host='0.0.0.0', port=5000)
