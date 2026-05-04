from flask import Flask, make_response, request, jsonify
from genska_lista import KODOMINANTNI_GENI, SUPER_GENI
from genetika_zmija import izracun_gena
from pony import orm
from leglo import Leglo
app = Flask(__name__)
# POST metoda
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
    }), 201
# GET metoda
@app.route('/izracunaj/<int:leglo_id>', methods = ['GET'])
@orm.db_session
def pretraga(leglo_id):
    zapis = Leglo.get(id=leglo_id)

    if not zapis:
        return jsonify({"message" : f"Izracun pod brojem {leglo_id} nepostoji u arhivi"}), 404
    return jsonify({
        "id_legla" : zapis.id,
        "otac" : zapis.roditelj1,
        "majka" : zapis.roditelj2,
        "leglo" : zapis.rezultat
    })
# GET metoda arhiva
@app.route('/arhiva', methods = ['GET'])
@orm.db_session
def arhiva():
    svi_zapisi = Leglo.select().order_by(orm.desc(Leglo.id)) # ispis od najnovijeg
    ispis = []
    for z in svi_zapisi:
        ispis.append({
            "id" : z.id,
            "otac" : z.roditelj1,
            "majka" : z.roditelj2,
            "leglo" : z.rezultat
        })
    return jsonify(ispis), 200
# PUT metoda
@app.route('/azuriraj/<int:leglo_id>', methods = ['PUT'])
@orm.db_session # razgovor s bazom, nuzan da bi radilo
def azuriraj(leglo_id):
    zapis = Leglo.get(id=leglo_id)
    if not zapis:
        return jsonify({"message": f"Leglo s id-em {leglo_id} nije pronadjeno"}), 404 #http errori
    podaci = request.get_json() #preuzima trenutan upis u postmanu
    novi_otac = podaci.get('zmija1', zapis.roditelj1) # uzima novi ako ga ima inace uzima stari
    nova_majka = podaci.get('zmija2', zapis.roditelj2)
    novi_rezultat = izracun_gena(novi_otac, nova_majka)

    # spremanje u bazu
    zapis.roditelj1 = novi_otac
    zapis.roditelj2 = nova_majka
    zapis.rezultat = novi_rezultat

    return jsonify ({
        "id_legla": zapis.id,
        "novi_otac" : zapis.roditelj1,
        "nova_majka" : zapis.roditelj2,
        "rezultat_parenja": zapis.rezultat
    }), 201

# DELETE metoda
@app.route('/izbrisi/<int:leglo_id>', methods = ['DELETE'])
@orm.db_session
def izbrisi(leglo_id):
    zapis = Leglo.get(id=leglo_id)
    if not zapis:
        return jsonify({"message" : f"Zapis legla sa id-om {leglo_id} nepostoji! "}), 404
    zapis.delete()
    return jsonify ({"message": f"Leglo s id-om {leglo_id} je obrisano!"})

if __name__ == '__main__':
    app.run(debug=True)