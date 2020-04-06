from flask import Flask, render_template, request, redirect, url_for, make_response
import DB_func as func  # my function transforming dataframe to sql
import apidae_extraction as apex  # my function retrieving data from apiade
from flask import *


app = Flask(__name__)

@app.route('/tables')
def get_welcome_page():
    #df_light = apex.retrieve_data_by_id_light(apex.project_ID,apex.api_KEY,apex.select_id)
    #df = apex.retrieve_data_by_id(apex.project_ID,apex.api_KEY,apex.select_id)
    df_multiple = apex.retrive_data_by_multiple_selectionId(apex.project_ID,apex.api_KEY,["86750","86749","86751","86752","86753","86960","86961","86962","86963"]) #
    return render_template ('dashboard.html', tables=[df_multiple.to_html(classes='data table-stripped')])

if __name__ == '__main__':
    app.run(debug=True)