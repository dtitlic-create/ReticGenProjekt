from flask import Flask, make_response, request, jsonify
from genska_lista import KODOMINANTNI_GENI, SUPER_GENI
from genetika_zmija import izracun_gena
from pony import orm
from leglo import Leglo
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    svi_moguci = sorted(KODOMINANTNI_GENI)
    return jsonify(svi_moguci)
@app.route('/izracunaj', methods=['POST'])
@orm.db_session
def izracunaj():
    podaci = request.get_json()
    geni_oca = podaci.get('zmija1')
    geni_majke = podaci.get('zmija2')

    rezultat = izracun_gena(geni_oca, geni_majke)

    # spremanje u bazu
    novo_leglo = Leglo(
        roditelj1=geni_oca,
        roditelj2=geni_majke,
        rezultat=rezultat
    )
    # Izracun + share
    orm.commit() #forsiranje bez kojeg neradi share
    return jsonify({
        "id_legla": novo_leglo.id,
        "share_link": f"http://127.0.0.1:5000/izracunaj/{novo_leglo.id}",
        "rezultat_parenja": rezultat
    })

@app.route('/izracunaj/<int:leglo_id>', methods = ['GET'])
@orm.db_session
def pretraga(leglo_id):
    zapis = Leglo.get(id=leglo_id)

    if not zapis:
        return "Izracun pod tim brojem nepostoji u arhivi"
    return jsonify({
        "id_legla" : zapis.id,
        "otac" : zapis.roditelj1,
        "majka" : zapis.roditelj2,
        "leglo" : zapis.rezultat
    })

if __name__ == '__main__':
    app.run(debug=True)