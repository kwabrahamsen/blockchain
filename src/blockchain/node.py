from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "supersecret"  # Trengs for flash-meldinger
blockchain = Blockchain()


# Rot-endepunkt
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.form['data']
    blockchain.add_block(data)
    flash("✅ Ny blokk lagt til!")
    return redirect(url_for('index'))

@app.route('/log')
def view_log():
    chain = blockchain.chain
    invalid_blocks = []

    for i in range(1, len(chain)):
        current = chain[i]
        prev = chain[i - 1]

        if current.hash != current.calculate_hash() or current.previous_hash != prev.hash:
            invalid_blocks.append(current.index)

    log = list(reversed(chain))  # nyeste først
    return render_template("log.html", log=log, invalid_blocks=invalid_blocks)

# Hent hele blokkjeden
@app.route("/chain")
def get_chain():
    full_chain = blockchain.chain
    validated_chain = []

    for i, block in enumerate(full_chain):
        valid = True
        if block.hash != block.calculate_hash():
            valid = False
        if i > 0 and block.previous_hash != full_chain[i - 1].hash:
            valid = False

        validated_chain.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "nonce": block.nonce,
            "valid": valid
        })

    return jsonify(validated_chain)


# Hent lengden på kjeden
@app.route('/length', methods=['GET'])
def get_length():
    return jsonify({'length': len(blockchain.chain)}), 200


# Legg til ny blokk med data via POST
@app.route('/add_block', methods=['POST'])
def add_block():
    values = request.get_json()

    # Sjekk at nødvendig felt er tilstede
    required = ['data']
    if not values or not all(k in values for k in required):
        return 'Manglende datafelt', 400

    # Legg til ny blokk
    data = values['data']
    blockchain.add_block(data)

    # Returner den nye blokken
    block = blockchain.get_latest_block()
    response = {
        'message': 'Ny blokk lagt til!',
        'index': block.index,
        'timestamp': block.timestamp,
        'data': block.data,
        'hash': block.hash,
        'previous_hash': block.previous_hash,
        'nonce': block.nonce
    }
    return jsonify(response), 201

@app.route('/break/<int:index>', methods=['POST'])
def break_block(index):
    success = blockchain.break_block(index)
    if success:
        flash(f"💥 Blokk #{index} er manipulert!")
    else:
        flash(f"🚫 Kunne ikke manipulere blokk #{index}.")
    return redirect(url_for('view_log'))

@app.route('/repair', methods=['POST'])
def repair_chain():
    blockchain.repair_chain()
    flash("🔧 Kjeden er forsøkt reparert!")
    return redirect(url_for('view_log'))


# Sjekk om kjeden er gyldig
@app.route('/valid', methods=['GET'])
def validate_chain():
    is_valid = blockchain.is_chain_valid()
    return jsonify({'valid': is_valid}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)