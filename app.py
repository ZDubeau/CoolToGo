"""----------------------------
Creation date : 2020-06-11
Last update : 2020-07-28
----------------------------"""

from wtforms.validators import InputRequired, Email, Length, Regexp, AnyOf
from wtforms import Form, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify, json, g, abort, session, send_from_directory
from flask_restful import Api
from celery import Celery
import redis
import requests
import socket
import os
from IPython.display import HTML
import pandas as pd
from pandas import DataFrame
from geopy.geocoders import BANFrance
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderQuotaExceeded
from geopy.extra.rate_limiter import RateLimiter
from pathlib import Path
import psycopg2
import psycopg2.extras
import logging
from LoggerModule.FileLogger import FileLogger as FileLogger
import DB_Functions as functions   # insert database related code here
import Table_admin as admin
import Table_Apidae as apidae
import Table_category as ctg
import Table_project as prj
import Table_selection as slc
import Table_message as msg
import Table_freshness as fresh
import Table_profil as prf
import Table_ManualEntry as me
import Table_relation_selection_category as slc_ctg
import Table_relation_eltref_prf as elt_prf
import Table_relation_eltref_ctg as elt_ctg
import Table_elementReference as eltRef
import Table_relation_category_apidae_edited as ctg_apidae_edited
import Table_relation_profil_apidae_edited as prf_apidae_edited
import Table_relation_category_data_from_apidae as ctg_apidae
import Table_relation_profil_data_from_apidae as prf_apidae
# import Table_relation_selection_profil as slc_prf
from DB_Connexion import DB_connexion
import urllib.parse
import api as ctg_api


if os.getenv("FLASK_ENV") == "development":
    FileLogger.InitLoggerByFile(
        os.getenv("FileLogger_path"), os.getenv("FileLogger_name"))


UPLOAD_FOLDER = 'tmp'
RESULT_FOLDER = 'tmp/result'
DOWNLOAD_FOLDER = 'tmp/download'
ALLOWED_EXTENSIONS = {'xls'}

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['CELERY_BROKER_URL'] = os.getenv("CELERY_BROKER_URL")
app.config['CELERY_RESULT_BACKEND'] = os.getenv("CELERY_RESULT_BACKEND")

POOL = redis.ConnectionPool(host=os.getenv(
    "REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
r = redis.StrictRedis(connection_pool=POOL)

#*********************** Register - new version **************************#


class RegistrationForm(Form):
    username = StringField(
        '', validators=[validators.input_required(), validators.Length(min=4, max=25)])
    email = StringField(
        '', validators=[validators.input_required(), validators.Email()])
    password = PasswordField('', validators=[validators.input_required(), validators.Regexp(
        '^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{6,})', message='Le mot de passe doit être composé de 6 caractères dont 1 lettre minuscule, 1 letter majuscule, 1 chiffre et un caractère spécial')])
    confirm = PasswordField('', validators=[validators.input_required()])

#*********************** Login - new version **************************#


class LoginForm(Form):
    username = StringField('username', [validators.Length(
        min=6, max=15, message='Nom d\'utilisteur incorrect')])
    password = PasswordField('password', [validators.Length(
        min=6, max=12, message='Mot de passe incorrect'), AnyOf(['secret', 'password'])])


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


# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery = Celery(app.name,
                broker=app.config['CELERY_BROKER_URL'],
                backend=app.config['CELERY_RESULT_BACKEND'],
                redis_max_connections=1,
                BROKER_TRANSPORT_OPTIONS={'max_connections': 2},
                broker_pool_limit=None)
# celery.conf.update(app.config)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#-------------------------------------------------------------------#
#                            Celery Tasks                           #
#-------------------------------------------------------------------#


@celery.task
def asynchronous_extract_for_selection(id):
    data_from_apidae = apidae.Data_from_apidae(id)
    data_from_apidae.Execute()
    del data_from_apidae


@celery.task
def asynchronous_selection_extract(id):
    selection = slc.Selection(id)
    selection.Execute()
    del selection
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(
        slc.select_selection_with_id_project, [id])
    del connexion
    for line in data:
        asynchronous_extract_for_selection.apply_async(
            args=[line[0]], countdown=2)


@celery.task
def file_elementReference_treatment(dfjson):
    df = pd.read_json(dfjson, typ='frame', orient='table',
                      convert_dates=False, convert_axes=False)
    elt_Ref = eltRef.elementReference(dataframe=df)
    elt_Ref.Execute()
    del elt_Ref

#____________________________________ Homepage ____________________________________#


@app.route('/', methods=['GET'])
def get_homepage():
    session.clear()
    form = RegistrationForm(request.form)
    modal_inscription = False
    modal_login = False
    connexion = DB_connexion()
    nb_admin = connexion.Query_SQL_fetchone(admin.nombre_admin)[0]
    del connexion
    inscription = False
    if nb_admin == 0:
        inscription = True
    return render_template('homepage.html', inscription=inscription, form=form, modal_inscription=modal_inscription, modal_login=modal_login)

#__________________________________ registration __________________________________#


@app.route('/inscription', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            print(fieldName, err)
    if request.method == 'POST' and form.validate():
        list_admin = functions.connexion_admin(
            form.username.data, form.password.data, True)
        if [form.username.data] in list_admin:
            ErrorMessage = "Nom d'utilisateur déjà existant!"
        else:
            functions.insert_administrator(
                form.username.data, form.password.data, form.email.data)
            ErrorMessage = "Merci de votre inscription!"
            # flash('Thanks for registering')
    modal_inscription = False
    connexion = DB_connexion()
    nb_admin = connexion.Query_SQL_fetchone(admin.nombre_admin)[0]
    del connexion
    inscription = False
    if nb_admin == 0:
        inscription = True
        modal_inscription = True
    return render_template('homepage.html', inscription=inscription, form=form, modal_inscription=modal_inscription)

# ???????????????????????????????????????????????????????????????????????????????????????????????????????
@app.route('/login_1', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    modal_login = False
    if form.validate_on_submit():
        modal_login = True
        return 'Formulaire soumis avec succès !'
    return render_template('get_homepage', form=form)

#____________________________________ Login page __________________________________#


@app.route("/login", methods=["GET", "POST"])
def post_login():
    username = request.form.get("uname")
    password = request.form.get("psw")
    admin_ID = functions.recuperation_id(admin.select_id_admin, (username,))
    bonID, list_admin = functions.connexion_admin(username, password)
    if bonID == True:
        resp = make_response(redirect(url_for("get_home")))
        session["username"] = username
        return redirect(url_for("get_home"))
    elif [username] in list_admin:
        ErrorMessage = "The username existe but the password is wrong!"
    else:
        ErrorMessage = "The passwords are not match!"

    return redirect(url_for("get_homepage", ErrorMessage=ErrorMessage))

#_____________________________________ Admin page ___________________________________#


@app.route('/home', methods=['GET'])
def get_home():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        return render_template('pages/home.html', username=username)

# ________________________________Element Reference _________________________________#


@app.route('/element_reference', methods=['GET'])
def get_elementReference():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            eltRef.select_elementRef, connexion.connexion())
        del connexion
        return render_template('pages/elementRef.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataelementreference', index=False)], username=username)


@app.route('/add_element_reference', methods=['POST'])
def get_add_eltRef():
    file = request.files['file']
    id_eltRef = request.form["id_eltRef"]
    if file and allowed_file(file.filename):
        filename = os.path.join(
            os.getcwd(), app.config['UPLOAD_FOLDER'], "elementreference." + file.filename.rsplit('.', 1)[1].lower())
        Path(os.path.join(
            os.getcwd(), app.config['UPLOAD_FOLDER'])).mkdir(parents=True, exist_ok=True)
        file.save(filename)
        elt_Ref = eltRef.elementReference(filename)
        df = elt_Ref.df
        file_elementReference_treatment.apply_async(
            args=[df.to_json(orient='table')], countdown=2)
        del elt_Ref
        errorMessage = "Fichier ajouté au projet"
    else:
        errorMessage = "Fichier non valide"
    os.remove(filename)
    return redirect(url_for("get_elementReference", errorMessage=errorMessage))


@app.route('/delete_elt_ref_not_used', methods=['GET'])
def get_delete_elt_ref_not_used():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        connexion.Delete_SQL(eltRef.delete_elementRef_not_used)
        del connexion
        errorMessage = "Ménage effectué!"
        return redirect(url_for("get_elementReference", errorMessage=errorMessage))

#______________________________ Apidae tables interface _____________________________#


@app.route('/tableApidae', methods=['GET', 'POST'])
def get_tableApidae():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            apidae.select_apidae_display_apidae_extract, connexion.connexion())
        del connexion
        return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableApidae', index=False)], username=username)
        # df = pd.read_sql(
        #     apidae.select_apidae_all_data_with_data_edited, connexion.connexion())
        # del connexion
        # return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableApidaejsonmode', index=False)], username=username)


@app.route('/tableManualEntry', methods=['GET', 'POST'])
def get_tableManualEntry():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            apidae.select_apidae_display_manual_entry, connexion.connexion())
        del connexion
        return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableManualEntry', index=False)], username=username)
        # df = pd.read_sql(
        #     apidae.select_apidae_all_data_with_data_edited, connexion.connexion())
        # del connexion
        # return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableApidaejsonmode', index=False)], username=username)


@app.route('/tableAllLocationsData', methods=['GET', 'POST'])
def get_tableAllLocationsData():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            apidae.select_apidae_display, connexion.connexion())
        del connexion
        return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableApidae', index=False)], username=username)
        # df = pd.read_sql(
        #     apidae.select_apidae_all_data_with_data_edited, connexion.connexion())
        # del connexion
        # return render_template('pages/tableApidae.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableApidaejsonmode', index=False)], username=username)


@app.route('/edit_category_profil/<id>', methods=['GET'])
def get_edit_category_profil(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(apidae.select_apidae_edit, [id])
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category_for_apidae_id, [id])
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_profil_for_apidae_id, [id])
        del connexion
    return render_template('pages/apidae_edit.html', id_data_from_apidae=id, id_apidae=data[1], titre=data[2], profil_c2g=data[3], category_c2g=data[4], categories=data_ctg, profiles=data_prf, username=username)

# ???????????????????????????????????????????????????????????????????????
@app.route('/edit_category_profil_manual_entry/<id>', methods=['GET'])
def get_edit_category_profil_manual(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(apidae.select_apidae_edit, [id])
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category_for_apidae_id, [id])
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_profil_for_apidae_id, [id])
        del connexion
    return redirect(url_for('get_tableManualEntry', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableManualEntry', index=False)], id_data_from_apidae=id, id_apidae=data[1], titre=data[2], profil_c2g=data[3], category_c2g=data[4], categories=data_ctg, profiles=data_prf, username=username))


@app.route('/remove_manual_entry/<id>', methods=['GET'])
def get_delete_manual_entry(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        connexion.Delete_SQL(apidae.delete_manual_entry, [id])
        del connexion
        ErrorMessage = "Entré manuelle est supprimé !"
        return redirect(url_for("get_tableManualEntry", ErrorMessage=ErrorMessage))


@app.route("/edit_category_profil_save", methods=["POST"])
def post_edit_category_profil():
    save_edit = request.form["id"]
    connexion = DB_connexion()
    list_of_id = connexion.Query_SQL_fetchall(
        apidae.select_apidae_all_id_for_same_id_apidae, [save_edit])
    for id_data_from_apidae in list_of_id:
        id_for_update = id_data_from_apidae[0]
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category_for_apidae_id, [id_for_update])
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_profil_for_apidae_id, [id_for_update])
        for line in data_ctg:
            try:
                category = request.form["categories-"+str(line[0])]
                if line[2] is None:
                    connexion.Insert_SQL(ctg_apidae_edited.insert_relation_category_apidae_edited, [
                        line[0], id_for_update])
            except KeyError:
                if line[2] is not None:
                    connexion.Delete_SQL(ctg_apidae_edited.delete_relation_category_apidae_edited, [
                        line[0], id_for_update])
        for line in data_prf:
            try:
                profil = request.form["profiles-"+str(line[0])]
                if line[2] is None:
                    connexion.Insert_SQL(prf_apidae_edited.insert_relation_profil_apidae_edited, [
                        line[0], id_for_update])
            except KeyError:
                if line[2] is not None:
                    connexion.Delete_SQL(prf_apidae_edited.delete_relation_profil_apidae_edited, [
                        line[0], id_for_update])
    del connexion
    return redirect(url_for("get_tableApidae"))

#_____________________________ Valid tables interface _______________________________#


# @app.route('/tableValide', methods=['GET', 'POST'])
# def get_tableValide():
#     if "username" not in session:
#         return redirect(url_for("get_homepage"))
#     else:
#         username = session["username"]
#         if 'ErrorMessage' in request.args:
#             ErrorMessage = request.args.get('ErrorMessage')
#         else:
#             ErrorMessage = ""
#         connexion = DB_connexion()
#         df = pd.read_sql(
#             DB_Table_Definitions.select_cooltogo_validated_for_display, connexion.connexion())
#         del connexion
#         return render_template('pages/tableValide.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableValid', index=False)], username=username, ErrorMessage=ErrorMessage)

#________________________________ Manual Entry ____________________________________#


@app.route('/ManualEntry', methods=['GET'])
def get_manualEntry():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category)
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_user_profil)
        del connexion
        return render_template('pages/manualEntry.html', categories=data_ctg, profiles=data_prf, username=username)


@app.route('/ManualEntryValide', methods=['GET', 'POST'])
def post_manualEntry():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        type_apidae = request.form["type_apidae"]
        title = request.form["titre"]
        address = request.form["adresse"]
        codePostal = request.form["code_postal"]
        city = request.form["ville"]
        altitude = request.form["altitude"]
        tel = request.form["telephone"]
        mail = request.form["email"]
        url = request.form["site_web"]
        accessibility = request.form["accessibilite"]
        paying = request.form["payant"]
        image = request.form["image"]
        opening = request.form["ouverture"]
        date_start = request.form["date_debut"]
        date_end = request.form["date_fin"]
        description = request.form["description"]
        environment = request.form["environment"]
        geolocator = BANFrance(
            domain='api-adresse.data.gouv.fr', timeout=10)
        try:
            geocode = RateLimiter(
                geolocator.geocode, min_delay_seconds=2, max_retries=4, error_wait_seconds=10.0, swallow_exceptions=True, return_value_on_exception=None)
            location = geocode(address)
            if location == None:
                lat = None
                lng = None
                FileLogger.log(
                    logging.DEBUG, f"{address} resolved with latitute {location.latitude} and longitute {location.longitude}")
            else:
                lat = location.latitude
                lng = location.longitude
                FileLogger.log(
                    logging.DEBUG, f"{address} not resolved !!!!")
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderQuotaExceeded) as e:
            FileLogger.log(logging.ERROR, "Error: geocode failed on input %s with message %s" %
                           (address, str(e)))
        id_apidae = 1000000000 + \
            connexion.Query_SQL_fetchone(
                apidae.select_count_manual_entry)[0] + 1
        id_data_from_apidae = connexion.Insert_SQL_fetchone(apidae.insert_apidae, {
            'id_apidae': id_apidae,  # mandatory
            'id_selection': 0,  # mandatory
            'type_apidae': type_apidae,  # needed
            'titre': title,  # needed
            'profil_c2g': '',
            'categorie_c2g': '',
            'adresse1': address,  # needed
            'adresse2': '',  # needed
            'code_postal': codePostal,  # needed
            'ville': city,  # needed
            'altitude':  altitude,  # needed
            'latitude': lat,  # needed
            'longitude': lng,  # needed
            'telephone': tel,  # needed
            'email': mail,  # needed
            'site_web':  url,  # needed
            'description_courte': '',  # needed
            'description_detaillee':  description,  # needed
            'image': image,  # needed
            'publics': '',
            'tourisme_adapte': accessibility,  # needed
            'payant': paying,  # needed
            'animaux_acceptes': '',
            'environnement': environment,  # needed
            'equipement': '',
            'services': '',
            'periode': '',
            'activites': '',
            'ouverture': opening,  # needed
            'date_debut': date_start,  # needed
            'date_fin': date_end,  # needed
            'typologie': '',
            'bons_plans': '',
            'dispositions_speciales': '',
            'service_enfants': '',
            'service_cyclistes': '',
            'nouveaute_2020': ''})[0]
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category)
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_user_profil)
        for line in data_ctg:
            try:
                category = request.form["categories-"+str(line[0])]
                connexion.Insert_SQL(ctg_apidae.insert_relation_category_apidae, [
                    line[0], id_data_from_apidae])
            except KeyError:
                continue
        for line in data_prf:
            try:
                profil = request.form["profiles-"+str(line[0])]
                connexion.Insert_SQL(prf_apidae.insert_relation_profil_apidae, [
                    line[0], id_data_from_apidae])
            except KeyError:
                continue
        del connexion
        return redirect(url_for("get_manualEntry", ErrorMessage="Nouvelle entrée a été ajouté dans la table manualEntry !"))

#________________________Add new administator interface_______________________#


@app.route('/add_admin', methods=['GET'])
def get_add_admin():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        df = pd.read_sql(
            admin.select_admin_for_display, connexion.connexion())
        del connexion
        return render_template('pages/Administators.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableAdmin', index=False)], username=username, ErrorMessage=ErrorMessage)

# Add admin interface after adding


@app.route("/new_admin", methods=["POST"])
def post_Administator():
    username = request.form["adm_uname"]
    email = request.form["adm_email"]
    password = request.form["adm_psw"]
    password_repeat = request.form.get("adm_psw-repeat")
    if password_repeat == password:
        list_admin = functions.connexion_admin(username, password, True)
        if [username] in list_admin:
            ErrorMessage = "Username already existe !"
        else:
            functions.insert_administrator(username, password, email)
    else:
        ErrorMessage = "The password inputs are differents !"
    return redirect(url_for("get_add_admin", ErrorMessage=ErrorMessage))

# Remove an administator


@app.route('/delete_admin/<id>')
def get_delete_admin(id):
    connexion = DB_connexion()
    connexion.Delete_SQL(admin.delete_admin, [id])
    del connexion
    ErrorMessage = "Admin deleted successfully !"
    return redirect(url_for("get_add_admin", ErrorMessage=ErrorMessage))
# ________________________________________________________________________
# @app.route('/remove_lieu/<id>')
# def get_remove_lieu(id):
#     connexion = DB_connexion()
#     DB_Protocole.cur.execute(
#         DB_Table_Definitions.delete_from_cooltogo_validated_with_id, [id])
#     DB_Protocole.cur.execute(
#         DB_Table_Definitions.delete_lien_niveau_de_fraicheur_cooltogo_validated, [id])
#     DB_Protocole.conn.commit()
#     del connexion
#     return redirect(url_for("get_tableValide"))

#----------------- Project Informations --------------------#


@app.route('/projectInformation', methods=['GET', 'POST'])
def get_projectInformation():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        df = pd.read_sql(
            prj.select_project_information, connexion.connexion())
        del connexion
        return render_template('pages/projectInformation.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableProjet', index=False)], username=username, ErrorMessage=ErrorMessage)

#------------------- New Project --------------------#


@app.route('/new_project_info', methods=['GET', 'POST'])
def get_new_project_info():
    project_ID = request.form["project_ID"]
    api_key = request.form["api_key"]
    connexion = DB_connexion()
    nb_project = connexion.Query_SQL_rowcount(
        prj.select_project_with_project_ID, [project_ID])
    del connexion
    errormessage = 'Projet déjà dans la base de donnée !!!'
    if nb_project == 0:
        id_project = functions.insert_project(project_ID, api_key)
        asynchronous_selection_extract.apply_async(
            args=[id_project], countdown=2)
        errormessage = ''
    return redirect(url_for("get_projectInformation", ErrorMessage=errormessage))

#--------------- Lancement(launch) d'extraction des selection --------------#


@app.route('/launch_selection_extract/<id>')
def get_launch_selection_extract(id):
    asynchronous_selection_extract.apply_async(
        args=[id], countdown=2)
    return redirect(url_for("get_apidaeSelection"))

#---------------- Remove project id -----------------#


@app.route('/delete_projet/<id>')
def get_delete_projet(id):
    connexion = DB_connexion()
    connexion.Delete_SQL(apidae.delete_apidae_project_id, [id])
    connexion.Delete_SQL(slc.delete_selection_with_project_id, [id])
    connexion.Delete_SQL(prj.delete_project_with_id, [id])
    del connexion
    return redirect(url_for("get_projectInformation"))

#----------------- Apidae Selection --------------------#


@app.route('/apidaeSelection', methods=['GET', 'POST'])
def get_apidaeSelection():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            slc.select_selection_information, connexion.connexion())
        del connexion
        return render_template('pages/apidaeSelection.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableSelection', index=False)], username=username)

#------------------- Edit Selection --------------------#


@app.route('/edit_selection/<id>', methods=['GET', 'POST'])
def get_edit_selection(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(slc.select_selection_with_id, [id])
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category_for_selection_id, [id])
        # data_prf = connexion.Query_SQL_fetchall(
        #     prf.select_profil_for_selection_id, [id])
        del connexion
        return render_template('pages/editSelection.html', id_selection=id, selection=data[0], description=data[1], categories=data_ctg, username=username)

#------------------- New category _ Selection --------------------#


@app.route('/edit_selection_post', methods=['POST'])
def get_edit_selection_post():
    selection = request.form["id"]
    connexion = DB_connexion()
    data_ctg = connexion.Query_SQL_fetchall(
        ctg.select_category_for_selection_id, [selection])
    # data_prf = connexion.Query_SQL_fetchall(
    #     prf.select_profil_for_selection_id, [selection])
    for line in data_ctg:
        try:
            category = request.form["categories-"+str(line[0])]
            if line[2] is None:
                connexion.Insert_SQL(slc_ctg.insert_relation_selection_category, [
                                     selection, line[0]])
        except KeyError:
            if line[2] is not None:
                connexion.Delete_SQL(slc_ctg.delete_relation_selection_category, [
                                     selection, line[0]])
    # for line in data_prf:
    #     try:
    #         profil = request.form["profil-"+str(line[0])]
    #         if line[2] is None:
    #             connexion.Insert_SQL(slc_prf.insert_relation_selection_profil, [
    #                                  selection, line[0]])
    #     except KeyError:
    #         if line[2] is not None:
    #             connexion.Delete_SQL(slc_prf.delete_relation_selection_profil, [
    #                                  selection, line[0]])
    del connexion
    return redirect(url_for("get_apidaeSelection"))

#--------------- Lancement(launch) d'extraction --------------#


@app.route('/launch_extract/<id>')
def get_launch_extract(id):
    asynchronous_extract_for_selection.apply_async(args=[id], countdown=2)
    return redirect(url_for("get_apidaeSelection"))

#---------------- Remove Selection id -----------------#


# @app.route('/delete_selection/<id>')
# def get_delete_selection(id):
#     connexion = DB_connexion()

#     DB_Protocole.cur.execute(slc.delete_selection, [id])
#     DB_Protocole.conn.commit()
#     del connexion
#     return redirect(url_for("get_apidaeSelection"))


#------------------ Edit lieu valid --------------------#


# @app.route('/edit_lieu_valide/<id>')
# def get_edit_data(id):
#     if "username" not in session:
#         return redirect(url_for("get_homepage"))
#     else:
#         username = session["username"]
#         connexion = DB_connexion()
#         DB_Protocole.cur.execute(
#             DB_Table_Definitions.select_cooltogo_validate_with_id, [id])
#         data = DB_Protocole.cur.fetchall()
#         DB_Protocole.cur.execute(
#             DB_Table_Definitions.select_lien_niveau_de_fraicheur_cooltogo_validated, [id])
#         data_niveau_fraicheur = DB_Protocole.cur.fetchone()
#         DB_Protocole.cur.execute(
#             DB_Table_Definitions.select_niveau_de_fraicheur_tous)
#         data_liste_fraicheur = DB_Protocole.cur.fetchall()
#         if data[0][16] == None:
#             publics = None
#         else:
#             publics = data[0][16].split(",")
#         del connexion redis.exceptions.ConnectionError: max number of clients reached
#     lieu_event = request.form["lieu_event"]
#     latitude = request.form["latitude"]
#     longitude = request.form["longitude"]
#     name = request.form["name"]
#     niveau_fraicheur = request.form["niveau_fraicheur"]
#     type_ = request.form["type"]
#     adresse1 = request.form["adresse1"]
#     adresse2 = request.form["adresse2"]
#     codePostal = request.form["code_postal"]
#     City = request.form["city"]
#     telephone = request.form["telephone"]
#     email = request.form["email"]
#     site_web = request.form["site_web"]
#     Description_Teaser = request.form["description_teaser"]
#     Description = request.form["description"]
#     Images = request.form["images"]
#     Categories = request.form["categories"]
#     Accessibilite = request.form["accessibilite"]
#     Payant = request.form["payant"]
#     public = ""
#     first = True
#     if "senior" in request.form:
#         public += "senior"
#         first = False
#     if "enfant" in request.form:
#         if first:
#             public += "enfant"
#             first = False
#         else:
#             public += ",enfant"
#     if "jeune" in request.form:
#         if first:
#             public += "jeune"
#             first = False
#         else:
#             public += ",jeune"
#     if "adulte" in request.form:
#         if first:
#             public += "adulte"
#             first = False
#         else:
#             public += ",adulte"
#     if "solidaire" in request.form:
#         if first:
#             public += "solidaire"
#             first = False
#         else:
#             public += ",solidaire"
#     plus_d_infos = request.form["plus_d_infos"]
#     Date_debut = request.form["date_debut"]
#     Date_fin = request.form["date_fin"]
#     geolocator = Nominatim(user_agent="cooltogo_api_backend")
#     location = geolocator.geocode(
#         adresse1+" "+adresse2+" "+codePostal+" "+City)
#     if location == None:
#         x_site = request.form["latitude"]
#         if x_site == "None":
#             x_lat = None
#         else:
#             x_lat = x_site
#         y_site = request.form["longitude"]
#         if y_site == "None":
#             y_lon = None
#         else:
#             y_lon = y_site
#     else:
#         x_lat = location.latitude
#         y_lon = location.longitude
#     connexion = DB_connexion()
#     ErrorMessage = functions.update_cooltogo_validated(
#         id_apidae,
#         lieu_event,
#         x_lat,
#         y_lon,
#         name,
#         niveau_fraicheur,
#         adresse1,
#         adresse2,
#         codePostal,
#         City,
#         telephone,
#         email,
#         site_web,
#         Description_Teaser,
#         Description,
#         Images,
#         public,
#         styleUrl,
#         styleHash,
#         type_,
#         Categories,
#         Accessibilite,
#         Payant,
#         plus_d_infos,
#         Date_debut,
#         Date_fin)

#     del connexion
#     return redirect(url_for("get_tableValide", ErrorMessage=ErrorMessage))

#_________________________extract locations__________________________#

@app.route('/extract_locations')
def get_extract_locations():
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchall(apidae.select_apidae)
    list_feature = []
    for value in data:
        data_one_id = connexion.Query_SQL_fetchone(
            apidae.select_apidae_1_id, [value[0]])
        dict_for_apidae, dict_for_geometry = functions.create_dict_for_lieu_validated(
            data_one_id)
        list_feature.append(dict_for_apidae)
    del connexion
    dict_for_extract = dict()
    dict_for_extract.update({"type": "FeatureCollection"})
    # dict_for_extract.update({"name": "cool2go"})
    # dict_for_extract_2 = {}
    # dict_for_extract_2.update({"name": "urn:ogc:def:crs:OGC:1.3:CRS84"})
    dict_for_extract_1 = {}
    dict_for_extract_1.update({"type": "name"})
    # dict_for_extract_1.update({"properties": dict_for_extract_2})
    # dict_for_extract.update({"crs": dict_for_extract_1})
    # dict_for_extract.update({"type": "Feature", })
    dict_for_extract.update({"features": list_feature})
    response = app.response_class(
        response=json.dumps(dict_for_extract, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )

    return response

#_____________________________Freshness______________________________#


@app.route('/coolness_values', methods=['GET'])
def get_coolness_values():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        df = pd.read_sql(
            fresh.select_freshness_level_for_diplay, connexion.connexion())
        del connexion
        return render_template('pages/coolness_values.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableCoolnessValues', index=False)], username=username)


@app.route("/new_coolness_value", methods=["POST"])
def post_new_coolness_value():
    connexion = DB_connexion()
    coolness_value = request.form["coolness_value"]
    score_freshness = request.form['score_freshness']
    connexion.Insert_SQL(fresh.insert_freshness_level, [
                         coolness_value, score_freshness])
    del connexion
    return redirect(url_for("get_coolness_values"))


@app.route("/change_coolness_status/<id>", methods=['GET', 'POST'])
def post_change_coolness_status(id):
    connexion = DB_connexion()
    connexion.Update_SQL(fresh.change_freshness_level_status, [id])
    del connexion
    return redirect(url_for("get_coolness_values"))

#_______________________Message button_________________________#


@app.route('/message', methods=['GET'])
def get_message():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        df = pd.read_sql(msg.select_message_list, connexion.connexion())
        del connexion
        return render_template('pages/message.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableMessage', index=False)], ErrorMessage=ErrorMessage, susername=username)


@app.route("/new-message", methods=["POST"])
def post_new_message():
    message = request.form["message"]
    if 'start_date' in request.form:
        start_date = request.form['start_date']
    else:
        start_date = None
    if 'end_date' in request.form:
        end_date = request.form['end_date']
    else:
        end_date = None
    connexion = DB_connexion()
    connexion.Insert_SQL(msg.insert_message, [
        message, start_date, end_date])
    del connexion
    return redirect(url_for("get_message", ErrorMessage="Nouveau message créé !!"))


@app.route('/edit_message/<id>')
def get_edit_message(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(
            DB_Table_Definitions.select_message, [id])
        del connexion
        message = data[1]
        start_date = data[2]
        end_date = data[3]
        return render_template('pages/message_edit.html', id=id, message=message, start_date=start_date, end_date=end_date, username=username)


@app.route("/edit-message_save", methods=["POST"])
def post_edit_message_save():
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
    connexion = DB_connexion()
    connexion.Update_SQL(msg.update_message, [
                         message, start_date, end_date, id])
    del connexion
    return redirect(url_for("get_message"))


@app.route('/publish_message/<id>')
def get_publish_message(id):
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchone(msg.select_message, [id])
    del connexion
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


@app.route('/delete_message/<id>')
def get_delete_message(id):
    connexion = DB_connexion()
    connexion.Delete_SQL(msg.delete_message, [id])
    del connexion
    ErrorMessage = "Message deleted successfully !"

    return redirect(url_for("get_message", ErrorMessage=ErrorMessage))

#__________________________Category___________________________#


@app.route('/category', methods=['GET'])
def get_category():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        df = pd.read_sql(ctg.select_category, connexion.connexion())
        del connexion
        return render_template('pages/category.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableCategory', index=False)], ErrorMessage=ErrorMessage, username=username)


@app.route("/new_category", methods=["POST"])
def post_category():
    category = request.form["category"]
    connexion = DB_connexion()
    rowcount = connexion.Query_SQL_rowcount(ctg.select_category_with_description,
                                            {"category_name": category})
    if rowcount > 0:
        ErrorMessage = "La catégorie existe déjà !"
    else:
        connexion.Insert_SQL(ctg.insert_category, {"category_name": category})
        ErrorMessage = ""
    del connexion
    return redirect(url_for("get_category", ErrorMessage=ErrorMessage))


@app.route('/edit_category/<id>')
def get_edit_category(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(ctg.select_category_with_id, [id])
        category = data[1]
        df = pd.read_sql(ctg.select_category, connexion.connexion())
        df_eltref_ctg = pd.read_sql(
            elt_ctg.select_relation_eltref_category, connexion.connexion(), params={"id_category": id})
        del connexion
    return render_template('pages/category_edit.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableCategory', index=False)], tables_elt_ctg=[df_eltref_ctg.to_html(classes='table table-bordered table-hover', table_id='dataEltCtg', index=False)], id=id, category=category)


@app.route("/edit_category_save", methods=["POST"])
def post_edit_category():
    id = request.form["id"]
    category = request.form["category"]
    connexion = DB_connexion()
    connexion.Update_SQL(ctg.update_category, [
        category, id])
    del connexion
    return redirect(url_for("get_category"))


@app.route("/new_element_for_category", methods=["POST"])
def post_element_for_category():
    id = request.form["id"]
    element_de_reference = request.form["element_de_reference"]
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchone(
        eltRef.select_elementRef_with_id_in_apidae, [element_de_reference])
    if data is not None:
        id_element_de_reference = data[0]
        data2 = connexion.Query_SQL_fetchone(
            elt_ctg.select_relation_eltref_category_with_category_element_reference, [id, id_element_de_reference])
        if data2 is None:
            connexion.Insert_SQL(elt_ctg.insert_relation_eltref_category, [
                id, id_element_de_reference])
    del connexion
    return redirect(url_for("get_edit_category", id=id))


@app.route('/delete_eltref_for_category/<id>/<id_category>')
def get_delete_eltref_for_category(id, id_category):
    try:
        connexion = DB_connexion()
        connexion.Delete_SQL(elt_ctg.delete_relation_eltref_category, [id])
        del connexion
        ErrorMessage = ""
    except Exception as e:
        ErrorMessage = e
    return redirect(url_for("get_edit_category", id=id_category, ErrorMessage=ErrorMessage))


@app.route('/delete_category/<id>')
def get_delete_category(id):
    try:
        connexion = DB_connexion()
        connexion.Delete_SQL(ctg.delete_category, [id])
        del connexion
        ErrorMessage = ""
    except Exception as e:
        ErrorMessage = e
    return redirect(url_for("get_category", ErrorMessage=ErrorMessage))

#________________________User Profil_________________________#


@app.route('/profil', methods=['GET'])
def get_profil():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'ErrorMessage' in request.args:
            ErrorMessage = request.args.get('ErrorMessage')
        else:
            ErrorMessage = ""
        connexion = DB_connexion()
        df = pd.read_sql(prf.select_user_profil, connexion.connexion())
        del connexion
        return render_template('pages/profil.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableProfil', index=False)], ErrorMessage=ErrorMessage, username=username)


@app.route("/new_profil", methods=["POST"])
def post_profil():
    profil = request.form["profil"]
    connexion = DB_connexion()
    rowcount = connexion.Query_SQL_rowcount(prf.select_user_profil_with_description,
                                            {"profil": profil})
    if rowcount > 0:
        ErrorMessage = "Le profil existe déjà !"
    else:
        connexion.Insert_SQL(prf.insert_user_profil, {"profil": profil})
        ErrorMessage = ""
    del connexion
    return redirect(url_for("get_profil", ErrorMessage=ErrorMessage))


@app.route('/edit_profil/<id>')
def get_edit_profil(id):
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        if 'id' in request.args:
            id = request.args.get('id')
        connexion = DB_connexion()
        data = connexion.Query_SQL_fetchone(
            prf.select_user_profil_with_id, [id])
        df = pd.read_sql(prf.select_user_profil, connexion.connexion())
        df_eltref_prf = pd.read_sql(
            elt_prf.select_relation_eltref_profil, connexion.connexion(), params={"id_profil": id})
        del connexion
        profil = data[1]
    return render_template('pages/profil_edit.html', tables=[df.to_html(classes='table table-bordered table-hover', table_id='dataTableProfil', index=False)], tables_elt_prf=[df_eltref_prf.to_html(classes='table table-bordered table-hover', table_id='dataEltPrf', index=False)], id=id, profil=profil)


@app.route("/edit_profil_save", methods=["POST"])
def post_edit_profil():
    id = request.form["id"]
    profil = request.form["profil"]
    connexion = DB_connexion()
    connexion.Insert_SQL(prf.update_user_profil, [
        profil, id])
    del connexion
    return redirect(url_for("get_profil"))


@app.route("/new_element_for_profil", methods=["POST"])
def post_element_for_profil():
    id = request.form["id"]
    element_de_reference = request.form["element_de_reference"]
    connexion = DB_connexion()
    data = connexion.Query_SQL_fetchone(
        eltRef.select_elementRef_with_id_in_apidae, [element_de_reference])
    if data is not None:
        id_element_de_reference = data[0]
        data2 = connexion.Query_SQL_fetchone(
            elt_prf.select_relation_eltref_profil_with_profil_element_reference, [id, id_element_de_reference])
        if data2 is None:
            connexion.Insert_SQL(elt_prf.insert_relation_eltref_profil, [
                id, id_element_de_reference])
    del connexion
    return redirect(url_for("get_edit_profil", id=id))


@app.route('/delete_eltref_for_profil/<id>/<id_profil>')
def get_delete_eltref_for_profil(id, id_profil):
    try:
        connexion = DB_connexion()
        connexion.Delete_SQL(elt_prf.delete_relation_eltref_profil, [id])
        del connexion
        ErrorMessage = ""
    except Exception as e:
        ErrorMessage = e
    return redirect(url_for("get_edit_profil", id=id_profil, ErrorMessage=ErrorMessage))


@app.route('/delete_profil/<id>')
def get_delete_profil(id):
    try:
        connexion = DB_connexion()
        connexion.Delete_SQL(prf.delete_user_profil, [id])
        del connexion
        ErrorMessage = ""
    except Exception as e:
        ErrorMessage = e
    return redirect(url_for("get_profil", ErrorMessage=ErrorMessage))

#----------------------------------------------------------#
#                      api for front-end                   #
#----------------------------------------------------------#


@app.route('/api', methods=['GET', 'POST'])
def get_api():
    if "username" not in session:
        return redirect(url_for("get_homepage"))
    else:
        username = session["username"]
        connexion = DB_connexion()
        data_ctg = connexion.Query_SQL_fetchall(
            ctg.select_category)
        data_prf = connexion.Query_SQL_fetchall(
            prf.select_user_profil)
        del connexion
        return render_template('pages/api.html', username=username, categories=data_ctg, profiles=data_prf)


@app.route('/api/categories', methods=['GET'])
def categories():

    c = ctg_api.query_database_for_list_of_categories()
    response = app.response_class(
        response=json.dumps(c, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/profiles', methods=['GET'])
def profiles():
    p = ctg_api.query_database_for_list_of_profiles()
    response = app.response_class(
        response=json.dumps(p, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/api/locations', methods=['POST'])
def locations():
    """
    the post request will be sent with a JSON body
    which defined the categories and profiles
    we want to filter the locations by
    formatted like:
    {
        categories: ['category1', 'category2', ...],
        profiles: ['profile1', 'profile2', ...]
    }
    """
    # try:
    req_data = request.get_json()
    nb = 0
    l = dict()
    if req_data is None:
        categories = []
        profiles = []
    else:
        if ('categories' in req_data) and ('profiles' in req_data):
            categories = req_data['categories']
            profiles = req_data['profiles']
            # filter all locations by the categories and profiles defined in the req_data
            nb, l = ctg_api.query_database_for_list_of_filtered_locations(
                tuple(categories), tuple(profiles))
        elif 'categories' in req_data:
            categories = req_data['categories']
            profiles = []

        elif 'profiles' in req_data:
            categories = []
            profiles = req_data['profiles']
        else:
            categories = []
            profiles = []

    dict_for_extract = dict()
    dict_for_extract.update({"status": 200})
    dict_for_extract.update({"locations_returned": nb})
    dict_for_extract_2 = {}
    dict_for_extract_2.update({"categories": categories})
    dict_for_extract_2.update({"profiles": profiles})
    dict_for_extract.update({"query": dict_for_extract_2})
    # dict_for_extract.update({"categories": categories, "profiles": profiles})
    dict_for_extract_1 = dict()
    dict_for_extract_1.update({"type": "FeatureCollection"})
    dict_for_extract_1.update({"name": "cool2go"})
    dict_for_extract_1.update({"features": l})
    dict_for_extract.update({"data": dict_for_extract_1})
    # except:
    #     dict_for_extract = dict()
    #     dict_for_extract.update({"status": 503})
    #     dict_for_extract_1 = dict()
    #     dict_for_extract_1.update({"type": "FeatureCollection"})
    #     dict_for_extract_1.update({"name": "cool2go"})
    #     dict_for_extract_1.update({"error": "error error"})
    #     dict_for_extract.update({"data": dict_for_extract_1})

    response = app.response_class(
        response=json.dumps(dict_for_extract, indent=3, sort_keys=False),
        status=200,
        mimetype='application/json'
    )
    return response


#---------------------------------------------------#
#                      The End                      #
#---------------------------------------------------#
if __name__ == '__main__':
    app.run(debug=True)
