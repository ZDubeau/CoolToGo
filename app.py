from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, json, g, abort, session
from flask_restful import Api
import socket
import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim

import DB_Protocole
from DB_Protocole import ConnexionDB, DeconnexionDB, make_engine
import DB_Table_Definitions
import DB_Functions as functions   # insert database related code here
import apidae_extraction as apex  # my function retrieving data from apiade


app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

api = Api(app)
# to allow angular to your python app
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response

#-------------------------- Homepage ---------------------------#


@app.route('/', methods=['GET'])
def get_homepage():
    session.clear()
    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.nombre_administrators)
    nb_admin = DB_Protocole.cur.fetchone()[0]
    inscription = False
    if nb_admin == 0:
        inscription = True
    DeconnexionDB()
    return render_template('homepage.html', inscription=inscription)

#---------------------- Inscription ----------------------#


@app.route("/inscription", methods=["POST"])
def post_inscription():
    ConnexionDB()
    username = request.form["uname"]
    email = request.form["email"]
    password = request.form["psw"]
    password_repeat = request.form.get("psw-repeat")
    if password_repeat == password:
        list_admin = functions.connexion_admin(username, password, True)
        # print(list_admin)
        if [username] in list_admin:
            errorMessage = "Username already existe!"
        else:
            functions.insert_administrator(username, password, email)
            errorMessage = "Well done, you've signed up!"
    else:
        errorMessage = "The passwords are not match!"
    DeconnexionDB()

    return redirect(url_for("get_homepage", errorMessage=errorMessage))

#---------------------- Login page ----------------------#


@app.route("/login", methods=["GET", "POST"])
def post_login():
    ConnexionDB()
    username = request.form.get("uname")
    password = request.form.get("psw")
    sql_admin = "select PKId_Admin from administrators where Admin_Name = %s "
    admin_ID = functions.recuperation_id(sql_admin, (username,))
    bonID, lis_admin = functions.connexion_admin(username, password)
    if bonID == True:
        resp = make_response(redirect(url_for("get_home")))
        session["username"] = username
        return redirect(url_for("get_home"))
    elif [username] in lis_admin:
        errorMessage = "The username existe but the password is wrong!"
    else:
        errorMessage = "The passwords are not match!"
    DeconnexionDB()

    return redirect(url_for("get_homepage", errorMessage=errorMessage))

#------------------------ Admin page ---------------------------#


@app.route('/home', methods=['GET'])
def get_home():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        return render_template('pages/home.html', username=username)

#----------------- Apidae tables interface --------------------#


@app.route('/tableApidae', methods=['GET', 'POST'])
def get_tableApidae():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_cooltogo_from_apidae_for_display, engine)

        return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableApidae', index=False)], username=username)

#------------------ Valid tables interface --------------------#


@app.route('/tableValide', methods=['GET', 'POST'])
def get_tableValide():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'errorMessage' in request.args:
            errorMessage = request.args.get('errorMessage')
        else:
            errorMessage = ""
        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_cooltogo_validated_for_display, engine)
        return render_template('pages/tableValide.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableValid', index=False)], username=username, errorMessage=errorMessage)

#------------------ Manual entry interface --------------------#


@app.route('/manualEntry', methods=['GET'])
def get_manualEntry():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        ConnexionDB()
        DB_Protocole.cur.execute(
            DB_Table_Definitions.select_niveau_de_fraicheur_tous)
        data_liste_fraicheur = DB_Protocole.cur.fetchall()
        DeconnexionDB()
        return render_template('pages/manualEntry.html', liste_niveau_fraicheur=data_liste_fraicheur, username=username)

#---------------------- New data valid ------------------------#


@app.route('/new_data_valid', methods=['GET', 'POST'])
def get_new_data_valid():
    lieu_event = request.form["lieu_event"]
    name = request.form["name"]
    niveau_fraicheur = request.form["niveau_fraicheur"]
    type_ = request.form["type"]
    adresse1 = request.form["adresse1"]
    adresse2 = request.form["adresse2"]
    codePostal = request.form["code_postal"]
    City = request.form["City"]
    telephone = request.form["telephone"]
    email = request.form["email"]
    site_web = request.form["site_web"]
    Description_Teaser = request.form["Description_Teaser"]
    Description = request.form["description"]
    styleUrl = request.form["styleUrl"]
    styleHash = request.form["styleHash"]
    Images = request.form["Images"]
    Categories = request.form["Categories"]
    Accessibilite = request.form["Accessibilité"]
    Payant = request.form["Payant"]
    public = ""
    first = True
    if "senior" in request.form:
        public += "senior"
        first = False
    if "enfant" in request.form:
        if first:
            public += "enfant"
            first = False
        else:
            public += ",enfant"
    if "jeune" in request.form:
        if first:
            public += "jeune"
            first = False
        else:
            public += ",jeune"
    if "adulte" in request.form:
        if first:
            public += "adulte"
            first = False
        else:
            public += ",adulte"
    if "solidaire" in request.form:
        if first:
            public += "solidaire"
            first = False
        else:
            public += ",solidaire"
    plus_d_infos = request.form["plus_d_infos"]
    Date_debut = request.form["Date_début"]
    Date_fin = request.form["Date_fin"]
    adresse_to_geolocalize = ""
    if adresse1 != "None":
        adresse_to_geolocalize += adresse1
    if adresse2 != "None":
        adresse_to_geolocalize += " " + adresse2
    geolocator = Nominatim(user_agent="cooltogo_api_backend")
    location = geolocator.geocode(
        adresse_to_geolocalize+" "+codePostal+" "+City)
    if location == None:
        x_lat = None
        y_lon = None
    else:
        x_lat = location.latitude
        y_lon = location.longitude
    ConnexionDB()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.select_max_id_from_cooltogo_validated)
    id_max = DB_Protocole.cur.fetchone()[0]
    if id_max == None:
        id_max = "1"
    else:
        id_max = str(id_max+1)
    id_apidae = "ManualEntry_"+id_max
    functions.insert_cooltogo_validated(id_apidae,
                                        lieu_event,
                                        x_lat,
                                        y_lon,
                                        name,
                                        niveau_fraicheur,
                                        adresse1,
                                        adresse2,
                                        codePostal,
                                        City,
                                        telephone,
                                        email,
                                        site_web,
                                        Description_Teaser,
                                        Description,
                                        Images,
                                        public,
                                        styleUrl,
                                        styleHash,
                                        type_,
                                        Categories,
                                        Accessibilite,
                                        Payant,
                                        plus_d_infos,
                                        Date_debut,
                                        Date_fin)
    DeconnexionDB()
    return redirect(url_for("get_tableValide"))

#-------------------- Validated lieu ------------------------#


@app.route('/validate_lieu/<id>')
def get_validate_lieu(id):
    ConnexionDB()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.select_cooltogo_from_apidae_one_id, [id])
    data = DB_Protocole.cur.fetchone()
    functions.insert_cooltogo_validated(data[1],
                                        data[3],
                                        data[6],
                                        data[7],
                                        data[4],
                                        "",
                                        data[8],
                                        data[9],
                                        data[10],
                                        data[11],
                                        data[12],
                                        data[13],
                                        data[14],
                                        data[15],
                                        data[15],
                                        data[16],
                                        data[17],
                                        "",
                                        "",
                                        data[5],
                                        data[18],
                                        data[19],
                                        data[20],
                                        data[21],
                                        data[22],
                                        data[23])
    DeconnexionDB()
    return redirect(url_for("get_tableApidae"))

#------------ Add new administator interface ---------------#


@app.route('/add_admin', methods=['GET'])
def get_add_admin():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'errorMessage' in request.args:
            errorMessage = request.args.get('errorMessage')
        else:
            errorMessage = ""

        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_adminitrators_for_display, engine)
        return render_template('pages/Administators.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableAdmin', index=False)], username=username, errorMessage=errorMessage)

#------------ Add admin interface after adding -------------#


@app.route("/new_admin", methods=["POST"])
def post_Administator():
    ConnexionDB()
    username = request.form["adm_uname"]
    email = request.form["adm_email"]
    password = request.form["adm_psw"]
    password_repeat = request.form.get("adm_psw-repeat")
    engine = make_engine()
    if password_repeat == password:
        list_admin = functions.connexion_admin(username, password, True)
        if [username] in list_admin:
            errorMessage = "Username already existe !"
        else:
            functions.insert_administrator(username, password, email)
            errorMessage = "Well done login please !"
    else:
        errorMessage = "The password inputs are differents !"
    DeconnexionDB()
    return redirect(url_for("get_add_admin", errorMessage=errorMessage))

#--------------- Remove an administator ------------------#


@app.route('/delete_admin/<id>')
def get_delete_admin(id):
    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.delete_administrators, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    errorMessage = "Admin deleted successfully !"
    return redirect(url_for("get_add_admin", errorMessage=errorMessage))

#-------------------- Remove a lieu ------------------------#


@app.route('/remove_lieu/<id>')
def get_remove_lieu(id):
    ConnexionDB()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_from_cooltogo_validated_with_id, [id])
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_lien_niveau_de_fraicheur_cooltogo_validated, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_tableValide"))

#----------------- Project Informations --------------------#


@app.route('/projectInformation', methods=['GET', 'POST'])
def get_projectInformation():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_projet_information, engine)
        return render_template('pages/projectInformation.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableProjet', index=False)], username=username)

#------------------- New Project --------------------#


@app.route('/new_project_info', methods=['GET', 'POST'])
def get_new_project_info():
    ConnexionDB()
    project_ID = request.form["project_ID"]
    api_key = request.form["api_key"]
    functions.insert_projet(project_ID, api_key)
    DeconnexionDB()
    return redirect(url_for("get_projectInformation"))

#--------------- Lancement(launch) d'extraction des selection --------------#


@app.route('/launch_selection_extract/<id>')
def get_launch_selection_extract(id):
    ConnexionDB()
    engine = make_engine()
    DB_Protocole.cur.execute(DB_Table_Definitions.select_projet_with_id, [id])
    data = DB_Protocole.cur.fetchone()
    df = apex.retrieve_selection_list(id, data[0], data[1])
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_selection_with_project_id, [id])
    DB_Protocole.conn.commit()
    df.to_sql('selection', con=engine, index=False, if_exists='append')
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))

#---------------- Remove project id -----------------#


@app.route('/delete_projet/<id>')
def get_delete_projet(id):
    ConnexionDB()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_cooltogo_from_apidae_with_project_id, [id])
    DB_Protocole.conn.commit()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_selection_with_project_id, [id])
    DB_Protocole.conn.commit()
    DB_Protocole.cur.execute(DB_Table_Definitions.delete_projet_with_id, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_projectInformation"))

#----------------- Apidae Selection --------------------#


@app.route('/apidaeSelection', methods=['GET', 'POST'])
def get_apidaeSelection():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_selection_information, engine)
        return render_template('pages/apidaeSelection.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableSelection', index=False)], username=username)

#------------------- Edit Selection --------------------#


@app.route('/edit_selection/<id>', methods=['GET', 'POST'])
def get_edit_selection(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        ConnexionDB()
        DB_Protocole.cur.execute(
            DB_Table_Definitions.select_selection_with_id, [id])
        data = DB_Protocole.cur.fetchone()
        DeconnexionDB()
        return render_template('pages/editSelection.html', id_selection=id, selection=data[0], categories=data[1], selection_type=data[2], username=username)


#------------------- New Selection --------------------#

@app.route('/edit_selection_post', methods=['GET', 'POST'])
def get_edit_selection_post():
    ConnexionDB()
    id_selection = request.form["id"]
    lieu_event = request.form["lieu_event"]
    functions.edit_selection(id_selection, lieu_event)
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))

#--------------- Lancement(launch) d'extraction --------------#


@app.route('/launch_extract/<id>')
def get_launch_extract(id):
    ConnexionDB()
    engine = make_engine()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.select_selection_projet, [id])
    data = DB_Protocole.cur.fetchone()
    df = apex.retrive_data_by_selectionId(data[0], data[1], data[2])
    DB_Protocole.cur.execute(
        DB_Table_Definitions.delete_cooltogo_from_apidae_with_selection_id, [id])
    DB_Protocole.conn.commit()
    df_in_db = pd.read_sql_table("cooltogo_from_apidae", engine)
    df_to_insert = df[~df.id_apidae.isin(df_in_db.id_apidae.values)]
    df_to_insert.to_sql('cooltogo_from_apidae', con=engine,
                        index=False, if_exists='append')
    DB_Protocole.cur.execute(DB_Table_Definitions.insert_selection_extraction, [
                             id, int(len(df_to_insert.index))])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))

#---------------- Remove Selection id -----------------#


@app.route('/delete_selection/<id>')
def get_delete_selection(id):
    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.delete_selection, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))

#------------------ Edit lieu valid --------------------#


@app.route('/edit_lieu_valide/<id>')
def get_edit_data(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        ConnexionDB()
        DB_Protocole.cur.execute(
            DB_Table_Definitions.select_cooltogo_validate_with_id, [id])
        data = DB_Protocole.cur.fetchall()
        DB_Protocole.cur.execute(
            DB_Table_Definitions.select_lien_niveau_de_fraicheur_cooltogo_validated, [id])
        data_niveau_fraicheur = DB_Protocole.cur.fetchone()
        DB_Protocole.cur.execute(
            DB_Table_Definitions.select_niveau_de_fraicheur_tous)
        data_liste_fraicheur = DB_Protocole.cur.fetchall()
        if data[0][16] == None:
            publics = None
        else:
            publics = data[0][16].split(",")
        DeconnexionDB()
        return render_template('pages/EditLieuValid.html', id_apidae=data[0][1], lieu_event=data[0][2], latitude=data[0][3], longitude=data[0][4], name=data[0][5], niveau_fraicheur=data_niveau_fraicheur, liste_niveau_fraicheur=data_liste_fraicheur, adresse1=data[0][6], adresse2=data[0][7], code_postal=data[0][8], city=data[0][9], telephone=data[0][10], email=data[0][11], ite_web=data[0][12], description_teaser=data[0][13], description=data[0][14], images=data[0][15], publics=publics, styleUrl=data[0][17], styleHash=data[0][18], type=data[0][19], categories=data[0][20], accessibilite=data[0][21], payant=data[0][22], plus_d_infos=data[0][23], date_debut=data[0][24], date_fin=data[0][25])

#------------------ Edit DATA valid -------------------#


@app.route('/edit_data_valid', methods=['GET', 'POST'])
def get_edit_data_valid():
    id_apidae = request.form["id_apidae"]
    lieu_event = request.form["lieu_event"]
    latitude = request.form["latitude"]
    longitude = request.form["longitude"]
    name = request.form["name"]
    niveau_fraicheur = request.form["niveau_fraicheur"]
    type_ = request.form["type"]
    adresse1 = request.form["adresse1"]
    adresse2 = request.form["adresse2"]
    codePostal = request.form["code_postal"]
    City = request.form["city"]
    telephone = request.form["telephone"]
    email = request.form["email"]
    site_web = request.form["site_web"]
    Description_Teaser = request.form["description_teaser"]
    Description = request.form["description"]
    styleUrl = request.form["styleUrl"]
    styleHash = request.form["styleHash"]
    Images = request.form["images"]
    Categories = request.form["categories"]
    Accessibilite = request.form["accessibilite"]
    Payant = request.form["payant"]
    public = ""
    first = True
    if "senior" in request.form:
        public += "senior"
        first = False
    if "enfant" in request.form:
        if first:
            public += "enfant"
            first = False
        else:
            public += ",enfant"
    if "jeune" in request.form:
        if first:
            public += "jeune"
            first = False
        else:
            public += ",jeune"
    if "adulte" in request.form:
        if first:
            public += "adulte"
            first = False
        else:
            public += ",adulte"
    if "solidaire" in request.form:
        if first:
            public += "solidaire"
            first = False
        else:
            public += ",solidaire"
    plus_d_infos = request.form["plus_d_infos"]
    Date_debut = request.form["date_debut"]
    Date_fin = request.form["date_fin"]
    geolocator = Nominatim(user_agent="cooltogo_api_backend")
    location = geolocator.geocode(
        adresse1+" "+adresse2+" "+codePostal+" "+City)
    if location == None:
        x_site = request.form["latitude"]
        if x_site == "None":
            x_lat = None
        else:
            x_lat = x_site
        y_site = request.form["longitude"]
        if y_site == "None":
            y_lon = None
        else:
            y_lon = y_site
    else:
        x_lat = location.latitude
        y_lon = location.longitude
    ConnexionDB()
    errorMessage = functions.update_cooltogo_validated(
        id_apidae,
        lieu_event,
        x_lat,
        y_lon,
        name,
        niveau_fraicheur,
        adresse1,
        adresse2,
        codePostal,
        City,
        telephone,
        email,
        site_web,
        Description_Teaser,
        Description,
        Images,
        public,
        styleUrl,
        styleHash,
        type_,
        Categories,
        Accessibilite,
        Payant,
        plus_d_infos,
        Date_debut,
        Date_fin)

    DeconnexionDB()
    return redirect(url_for("get_tableValide", errorMessage=errorMessage))

#------------------- extract locations --------------------#


@app.route('/extract_locations')
def get_extract_locations():
    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.select_cooltogo_validated)
    data = DB_Protocole.cur.fetchall()
    DeconnexionDB()
    list_feature = []
    for value in data:
        list_feature.append(functions.create_dict_for_lieu_validated(value))
    dict_for_extract = dict()
    dict_for_extract.update({"type": "FeatureCollection"})
    dict_for_extract.update({"name": "cool2go"})
    dict_for_extract_2 = {}
    dict_for_extract_2.update({"name": "urn:ogc:def:crs:OGC:1.3:CRS84"})
    dict_for_extract_1 = {}
    dict_for_extract_1.update({"type": "name"})
    dict_for_extract_1.update({"properties": dict_for_extract_2})
    dict_for_extract.update({"crs": dict_for_extract_1})
    dict_for_extract.update({"features": list_feature})
    response = app.response_class(
        response=json.dumps(dict_for_extract, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response

#-------------- Niveau de fraicheur ---------------#


@app.route('/coolness_values', methods=['GET'])
def get_coolness_values():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        engine = make_engine()
        df = pd.read_sql(
            DB_Table_Definitions.select_niveau_de_fraicheur_for_diplay, engine)
        return render_template('pages/coolness_values.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableCoolnessValues', index=False)], username=username)

#------------ Nouveau niveau fraicheur -----------#


@app.route("/new_coolness_value", methods=["POST"])
def post_new_coolness_value():
    ConnexionDB()
    coolness_value = request.form["coolness_value"]
    DB_Protocole.cur.execute(
        DB_Table_Definitions.insert_niveau_de_fraicheur, [coolness_value])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_coolness_values"))

# -------------------------------------------------------------


@app.route("/change_coolness_status/<id>", methods=['GET', 'POST'])
def post_change_coolness_status(id):
    ConnexionDB()
    DB_Protocole.cur.execute(
        DB_Table_Definitions.change_niveau_de_fraicheur_status, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_coolness_values"))

#-------------------- Message button ----------------------#


@app.route('/message', methods=['GET'])
def get_message():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'errorMessage' in request.args:
            errorMessage = request.args.get('errorMessage')
        else:
            errorMessage = ""
        engine = make_engine()
        df = pd.read_sql(DB_Table_Definitions.select_message_list, engine)
        return render_template('pages/message.html', tables=[df.to_html(classes='table table-bordered', table_id='dataTableMessage', index=False)], errorMessage=errorMessage, susername=username)


@app.route("/new-message", methods=["POST"])
def post_new_message():
    ConnexionDB()
    message = request.form["message"]
    if 'start_date' in request.form:
        start_date = request.form['start_date']
    else:
        start_date = None
    if 'end_date' in request.form:
        end_date = request.form['end_date']
    else:
        end_date = None
    DB_Protocole.cur.execute(DB_Table_Definitions.insert_message, [
                             message, start_date, end_date])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_message", errorMessage="Nouveau message créé !!"))


@app.route('/edit_message/<id>')
def get_edit_message(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        ConnexionDB()
        DB_Protocole.cur.execute(DB_Table_Definitions.select_message, [id])
        data = DB_Protocole.cur.fetchone()
        DeconnexionDB()
        message = data[1]
        start_date = data[2]
        end_date = data[3]
        return render_template('pages/message_edit.html', id=id, message=message, start_date=start_date, end_date=end_date, username=username)


@app.route("/edit-message_save", methods=["POST"])
def post_edit_message_save():
    ConnexionDB()
    id = request.form["id"]
    message = request.form["message"]
    if 'start_date' in request.form:
        start_date = request.form['start_date']
    else:
        start_date = None
    if 'end_date' in request.form:
        end_date = request.form['end_date']
    else:
        end_date = None
    DB_Protocole.cur.execute(DB_Table_Definitions.update_message, [
                             message, start_date, end_date, id])
    DB_Protocole.conn.commit()
    DeconnexionDB()

    return redirect(url_for("get_message"))


@app.route('/publish_message/<id>')
def get_publish_message(id):

    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.select_message, [id])
    data = DB_Protocole.cur.fetchone()
    DeconnexionDB()

    message = data[1]
    start_date = data[2]
    end_date = data[3]
    list_feature = []

    dict_for_extract = dict()
    dict_for_extract.update({"type": "message"})
    dict_for_extract.update({"message": message})
    dict_for_extract.update({"Date de début": start_date})
    dict_for_extract.update({"Date de fin": end_date})

    response = app.response_class(
        response=json.dumps(dict_for_extract, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response
#--------------- Remove a message ------------------#
@app.route('/delete_message/<id>')
def get_delete_message(id):
    ConnexionDB()
    DB_Protocole.cur.execute(DB_Table_Definitions.delete_message, [id])
    DB_Protocole.conn.commit()
    DeconnexionDB()
    errorMessage = "Message deleted successfully !"

    return redirect(url_for("get_message", errorMessage=errorMessage))

#---------------------------------------------------#
#                      The End                      #
#---------------------------------------------------#


if __name__ == '__main__':
    app.run(debug=True)
