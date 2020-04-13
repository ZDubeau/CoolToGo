from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, json
from flask_restful import Api

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from geopy.geocoders import Nominatim

import DB_Protocole
from DB_Protocole import ConnexionDB, DeconnexionDB, make_engine
import DB_Functions as functions   # insert database related code here
import apidae_extraction as apex  # my function retrieving data from apiade


app = Flask(__name__)

api = Api(app) 
#to allow angular to your python app
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

#-------------------------- Homepage ---------------------------#

@app.route('/', methods=['GET'])
def get_homepage():
    ConnexionDB()
    sql_nb_admin = "SELECT count(*) FROM administrators"
    DB_Protocole.cur.execute(sql_nb_admin)
    nb_admin = DB_Protocole.cur.fetchone()[0]
    inscription = False
    if nb_admin == 0:
        inscription = True
    DeconnexionDB()
    return render_template('homepage.html', inscription=inscription)

#------------------------ Admin page ---------------------------#

@app.route('/home', methods=['GET'])
def get_home():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')
    
    return render_template('pages/home.html', pseudo=pseudo)

#----------------- Apidae tables interface --------------------#

@app.route('/tableApidae', methods=['GET', 'POST'])
def get_tableApidae():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')
    
    engine = make_engine()
    df = pd.read_sql("SELECT *,'' as a FROM cooltogo_from_apidae WHERE id_apidae NOT IN (SELECT DISTINCT id_apidae FROM cooltogo_validated) ORDER BY id ASC", engine)
    
    return render_template('pages/tableApidae.html',tables=[df.to_html(classes=['table table-bordered'], table_id='dataTableApidae',index=False)], pseudo=pseudo)

#------------------ Valid tables interface --------------------#

@app.route('/tableValide', methods=['GET', 'POST'])
def get_tableValide():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')

    if 'errorMessage' in request.args :
        errorMessage = request.args.get('errorMessage')
    else :
        errorMessage = ""

    engine = make_engine()
    df = pd.read_sql("SELECT *, '' as Edit, '' as Del FROM cooltogo_validated ORDER BY id ASC", engine)
    
    return render_template('pages/tableValide.html',tables=[df.to_html(classes='table table-bordered', table_id='dataTableValid',index=False)], pseudo=pseudo, errorMessage=errorMessage)

#------------------ Manual entry interface --------------------#

@app.route('/manualEntry', methods=['GET'])
def get_manualEntry():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')
    ConnexionDB()
    sql_liste_niveau_de_fraicheur = "SELECT id,niveau_de_fraicheur FROM niveau_de_fraicheur WHERE active ORDER BY niveau_de_fraicheur ASC"
    DB_Protocole.cur.execute(sql_liste_niveau_de_fraicheur)
    data_liste_fraicheur = DB_Protocole.cur.fetchall()
    DeconnexionDB()
    return render_template('pages/manualEntry.html',liste_niveau_fraicheur=data_liste_fraicheur, pseudo=pseudo)

#---------------------- New data valid ------------------------#

@app.route('/new_data_valid', methods=['GET','POST'])
def get_new_data_valid():

    lieu_event = request.form["lieu_event"]
    name = request.form["name"]
    niveau_fraicheur = request.form["niveau_fraicheur"]
    type_ = request.form["type"]
    adresse1 = request.form["adresse1"]
    adresse2 = request.form["adresse2"]
    codePostal = request.form["code_postal"]
    City = request.form["City"]
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
        if first :
            public += "enfant"
            first = False
        else :
            public += ",enfant"
    if "jeune" in request.form:
        if first :
            public += "jeune"
            first = False
        else :
            public += ",jeune"
    if "adulte" in request.form:
        if first :
            public += "adulte"
            first = False
        else :
            public += ",adulte"
    if "solidaire" in request.form:
        if first :
            public += "solidaire"
            first = False
        else :
            public += ",solidaire"

    plus_d_infos = request.form["plus_d_infos"]
    Date_debut = request.form["Date_début"]
    Date_fin = request.form["Date_fin"]

    adresse_to_geolocalize = ""
    if adresse1 != "None" :
        adresse_to_geolocalize += adresse1
    if adresse2 != "None" :
        adresse_to_geolocalize += " " + adresse2
    geolocator = Nominatim(user_agent="cooltogo_api_backend")
    location = geolocator.geocode(adresse_to_geolocalize+" "+codePostal+" "+City)

    if location == None:
        x_lat = None
        y_lon = None
    else :
        x_lat = location.latitude
        y_lon = location.longitude 

    ConnexionDB()
    sql_max_id = "SELECT MAX(id) FROM cooltogo_validated"
    DB_Protocole.cur.execute(sql_max_id)
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
    engine = make_engine()
    df = pd.read_sql("SELECT *, '' as Edit ,'' as a FROM cooltogo_validated ORDER BY id ASC", engine)
    
    return redirect(url_for("get_tableValide"))

#-------------------- Message button ----------------------#

@app.route('/message', methods=['GET'])
def get_message():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')

    engine = make_engine()
    df = pd.read_sql("SELECT message, published_on AS Published_date, active FROM message", engine)

    return render_template('pages/message.html',tables=[df.to_html(classes='table table-bordered', table_id='dataTableMessage',index=False)], pseudo=pseudo)

@app.route("/new-message", methods=["POST"])
def post_new_message():
    ConnexionDB()
    message = request.form["message"]
    sql_set_all_message_to_false = "UPDATE message SET active = False"
    DB_Protocole.cur.execute(sql_set_all_message_to_false)
    DB_Protocole.conn.commit()
    sql_insert_message = "INSERT INTO message (message, published_on, active) VALUES ('"+message+"',NOW(),True)"
    DB_Protocole.cur.execute(sql_insert_message)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_message"))

#------------ Add new administator interface ---------------#

@app.route('/add_admin', methods=['GET'])
def get_add_admin():

    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')

    if 'errorMessage' in request.args :
        errorMessage = request.args.get('errorMessage')
    else :
        errorMessage = ""

    engine = make_engine()
    df = pd.read_sql("SELECT PKId_Admin as Id, Admin_Name as Name, Admin_email as Email,'' as Action FROM administrators ORDER BY PKId_Admin ASC", engine)
    
    return render_template('pages/Administators.html',tables=[df.to_html(classes='table table-bordered', table_id='dataTableAdmin',index=False)],pseudo=pseudo,errorMessage=errorMessage)

#------------ Add admin interface after adding -------------#

@app.route("/new_admin", methods=["POST"])
def post_Administator():
    ConnexionDB()
    pseudo = request.form["adm_uname"]
    email = request.form["adm_email"]
    password = request.form["adm_psw"]
    password_repeat = request.form.get("adm_psw-repeat")
    engine = make_engine()
    
    if password_repeat == password:
        list_admin = functions.connexion_admin(pseudo, password, True)
        if [pseudo] in list_admin :
            errorMessage="L'utilisateur existe déjà !"
        else:
            functions.insert_administrator(pseudo, password,email)
            errorMessage="Bravo utilisateur inscrit !"
    else:
        errorMessage="The password inputs are diffrents !"
    DeconnexionDB()
    return redirect(url_for("get_add_admin",errorMessage=errorMessage))

#--------------- Remove an administator ------------------#

@app.route('/delete_admin/<id>')
def get_delete_admin(id):
    ConnexionDB()
    sql_delete_admin = "DELETE FROM administrators WHERE PKId_Admin="+id
    DB_Protocole.cur.execute(sql_delete_admin)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    errorMessage="Admin deleted successfully !"
    return redirect(url_for("get_add_admin",errorMessage=errorMessage))

#---------------------- Login page ----------------------#

@app.route("/login", methods=["GET","POST"])
def post_login():
    ConnexionDB()
    pseudo = request.form.get("uname")
    password = request.form.get("psw")
    sql_admin="select PKId_Admin from administrators where Admin_Name = %s "
    admin_ID = functions.recuperation_id(sql_admin,(pseudo,))

    bonID, lis_admin = functions.connexion_admin(pseudo, password)    
    if bonID == True:
        resp = make_response(redirect(url_for("get_home")))
        print("resp :", resp)

        resp.set_cookie('id', str(admin_ID))
        resp.set_cookie('pseudo', pseudo)
        return redirect(url_for("get_home"))
    elif [pseudo] in lis_admin:
        errorMessage="The username existe but the password is wrong!"
    else:
        errorMessage="The passwords are not match!"
        
    DeconnexionDB()
    return redirect(url_for("get_homepage",errorMessage=errorMessage))

#---------------------- Inscription ----------------------#

@app.route("/inscription", methods=["POST"])
def post_inscription():
    ConnexionDB()
    pseudo = request.form["uname"]
    email = request.form["email"]
    password = request.form["psw"]
    password_repeat = request.form.get("psw-repeat")

    if password_repeat == password:
        list_admin = functions.connexion_admin(pseudo, password, True)
        #print(list_admin)
        if [pseudo] in list_admin :
            errorMessage="Username already existe!"
        else:
            functions.insert_administrator(pseudo, password,email)
            errorMessage="Well done, you've signed up!"
    else:
        errorMessage="The passwords are not match!"
    DeconnexionDB()
    return redirect(url_for("get_homepage",errorMessage=errorMessage))

#-------------------- Validated lieu ------------------------#

@app.route('/validate_lieu/<id>')
def get_validate_lieu(id):
    ConnexionDB()
    sql_select_data = "SELECT * FROM cooltogo_from_apidae WHERE id="+id
    DB_Protocole.cur.execute(sql_select_data)
    data = DB_Protocole.cur.fetchone()
    functions.insert_cooltogo_validated(data[1],
                                        data[3],
                                        data[6],
                                        data[7],
                                        data[4],
                                        None,
                                        data[8],
                                        data[9],
                                        data[10],
                                        data[11],
                                        data[12],
                                        data[12],
                                        data[13],
                                        data[14],
                                        "",
                                        "",
                                        data[5],
                                        data[15],
                                        data[16],
                                        data[17],
                                        data[18],
                                        data[19],
                                        data[20])
    DeconnexionDB()
    engine = make_engine()
    df = pd.read_sql("SELECT *,'' as a FROM cooltogo_from_apidae WHERE id_apidae NOT IN (SELECT DISTINCT id_apidae FROM cooltogo_validated) ORDER BY id ASC", engine)
    
    return redirect(url_for("get_tableApidae"))

#-------------------- Remove a lieu ------------------------#

@app.route('/remove_lieu/<id>')
def get_remove_lieu(id):
    ConnexionDB()
    sql_delete_valid = "DELETE FROM cooltogo_validated WHERE id="+id
    DB_Protocole.cur.execute(sql_delete_valid)
    sql_delete_lien_niveau_fraicheur = "DELETE FROM lien_niveau_de_fraicheur_cooltogo_validated WHERE id_cooltogo_validated = "+id
    DB_Protocole.cur.execute(sql_delete_lien_niveau_fraicheur)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_tableValide"))

@app.route('/apidaeSelection', methods=['GET', 'POST'])
def get_apidaeSelection():
    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')
    engine = make_engine()
    df = pd.read_sql("SELECT s.id as id, s.selection as selection, s.description as description, s.selection_type as Lieu_Event, max(se.selection_extraction_date) AS Last_Extract,'' as Launch, '' as Del  FROM selection AS s LEFT JOIN selection_extraction AS se ON s.id = se.selection_id GROUP BY s.id, selection, description ORDER BY s.id ASC", engine)
    return render_template('pages/apidaeSelection.html',tables=[df.to_html(classes='table table-bordered', table_id='dataTableSelection',index=False)], pseudo=pseudo)

@app.route('/new_selection', methods=['GET','POST'])
def get_new_selection():
    ConnexionDB()
    selection_name = request.form["selection"]
    description = request.form["description"]
    lieu_event = request.form["lieu_event"]
    functions.insert_selection(selection_name,description,lieu_event)
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))


@app.route('/launch_extract/<id>')
def get_launch_extract(id):
    ConnexionDB()
    engine = make_engine()

    sql_select_data = "SELECT selection FROM selection WHERE id="+id
    DB_Protocole.cur.execute(sql_select_data)
    functions = DB_Protocole.cur.fetchone()[0]
    df = apex.retrive_data_by_selectionId(apex.project_ID,apex.api_KEY,functions)

    sql_delete_extract_selection = "DELETE FROM cooltogo_from_apidae WHERE id_selection='"+id+"'"
    DB_Protocole.cur.execute(sql_delete_extract_selection)
    DB_Protocole.conn.commit()

    df_in_db = pd.read_sql_table("cooltogo_from_apidae", engine)
    df_to_insert = 	df[~df.id_apidae.isin(df_in_db.id_apidae.values)]
   
    df_to_insert.to_sql('cooltogo_from_apidae',con=engine, index=False, if_exists='append')
    sql_last_extract = "INSERT INTO selection_extraction (selection_id,selection_extraction_date) VALUES ("+id + ",NOW())"
    DB_Protocole.cur.execute(sql_last_extract)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    
    return redirect(url_for("get_apidaeSelection"))


@app.route('/delete_selection/<id>')
def get_delete_selection(id):
    ConnexionDB()
    sql_delete_selection = "DELETE FROM selection WHERE id="+id
    DB_Protocole.cur.execute(sql_delete_selection)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_apidaeSelection"))

@app.route('/edit_lieu_valide/<id>')
def get_edit_data(id):
    ConnexionDB()
    sql_select_data = "SELECT * FROM cooltogo_validated WHERE id="+id
    DB_Protocole.cur.execute(sql_select_data)
    data = DB_Protocole.cur.fetchall()
    sql_niveau_de_fraicheur = "SELECT id_niveau_de_fraicheur FROM lien_niveau_de_fraicheur_cooltogo_validated WHERE id_cooltogo_validated="+id
    DB_Protocole.cur.execute(sql_niveau_de_fraicheur)
    data_niveau_fraicheur = DB_Protocole.cur.fetchone()
    sql_liste_niveau_de_fraicheur = "SELECT id,niveau_de_fraicheur FROM niveau_de_fraicheur WHERE active ORDER BY niveau_de_fraicheur ASC"
    DB_Protocole.cur.execute(sql_liste_niveau_de_fraicheur)
    data_liste_fraicheur = DB_Protocole.cur.fetchall()
    publics = data[0][13].split(",")
    DeconnexionDB()
    return render_template('pages/EditLieuValid.html',id_apidae=data[0][1],lieu_event=data[0][2],latitude=data[0][3],longitude=data[0][4],name=data[0][5],niveau_fraicheur=data_niveau_fraicheur,liste_niveau_fraicheur=data_liste_fraicheur,adresse1=data[0][6],adresse2=data[0][7],code_postal=data[0][8],city=data[0][9],description_teaser=data[0][10],description=data[0][11],images=data[0][12],publics = data[0][13].split(","),styleUrl=data[0][14],styleHash=data[0][15],type=data[0][16],categories=data[0][17],accessibilite=data[0][18],payant=data[0][19],plus_d_infos=data[0][20],date_debut=data[0][21],date_fin=data[0][22])

@app.route('/edit_data_valid' , methods=['GET', 'POST'])
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
        if first :
            public += "enfant"
            first = False
        else :
            public += ",enfant"
    if "jeune" in request.form:
        if first :
            public += "jeune"
            first = False
        else :
            public += ",jeune"
    if "adulte" in request.form:
        if first :
            public += "adulte"
            first = False
        else :
            public += ",adulte"
    if "solidaire" in request.form:
        if first :
            public += "solidaire"
            first = False
        else :
            public += ",solidaire"

    plus_d_infos = request.form["plus_d_infos"]
    Date_debut = request.form["date_debut"]
    Date_fin = request.form["date_fin"]

    geolocator = Nominatim(user_agent="cooltogo_api_backend")
    location = geolocator.geocode(adresse1+" "+adresse2+" "+codePostal+" "+City)

    if location == None:
        x_site = request.form["latitude"]
        if x_site == "None" :
            x_lat = None
        else :
            x_lat = x_site
        y_site = request.form["longitude"]
        if y_site == "None" :
            y_lon = None
        else :
            y_lon = y_site
    else :
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

    return redirect(url_for("get_tableValide",errorMessage=errorMessage))

@app.route('/extract_locations')
def get_extract_locations():
    ConnexionDB()
    sql_select_data = "SELECT * FROM cooltogo_validated"
    DB_Protocole.cur.execute(sql_select_data)
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
        response=json.dumps(dict_for_extract,indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/coolness_values', methods=['GET'])
def get_coolness_values():
    user_ID = request.cookies.get('id')
    pseudo = request.cookies.get('pseudo')
    engine = make_engine()
    df = pd.read_sql("SELECT id,niveau_de_fraicheur AS Fraicheur, active, '' AS Change FROM niveau_de_fraicheur", engine)
    return render_template('pages/coolness_values.html',tables=[df.to_html(classes='table table-bordered', table_id='dataTableCoolnessValues',index=False)], pseudo=pseudo)

@app.route("/new_coolness_value", methods=["POST"])
def post_new_coolness_value():
    ConnexionDB()
    coolness_value = request.form["coolness_value"]
    sql_insert_message = "INSERT INTO niveau_de_fraicheur (niveau_de_fraicheur) VALUES ('"+coolness_value+"')"
    DB_Protocole.cur.execute(sql_insert_message)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_coolness_values"))

@app.route("/change_coolness_status/<id>", methods=['GET','POST'])
def post_change_coolness_status(id):
    ConnexionDB()
    sql_toggle_active = "UPDATE niveau_de_fraicheur SET active = NOT active WHERE id ="+id
    DB_Protocole.cur.execute(sql_toggle_active)
    DB_Protocole.conn.commit()
    DeconnexionDB()
    return redirect(url_for("get_coolness_values"))

#---------------------------------------------------#
#                      The End                      #
#---------------------------------------------------#

if __name__ == '__main__':
    app.run(debug=True)