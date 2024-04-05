from flask import Flask, render_template, request

from wtforms import StringField, SelectField, TextAreaField, validators, Form

  
import json
from libs.sql_connection import *
  
 
class SearchInputs(Form):   
    dropdown = SelectField('Searching Criteria', choices = [('Chapter_no', 'chapter_no'),
                                                            ('Verse_no', 'verse_no'),
                                                            ('Shloka', 'shloka'),
                                                            ('English_translation', 'english_translation'),
                                                              ('Explanation', 'explanation') ],
                                                            validators=[validators.DataRequired()])
    keyword = StringField("Keyword", validators=[validators.DataRequired()])

 
app = Flask(__name__)
 
 
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods = ['POST', 'GET'])
def search():
    form = SearchInputs(request.form)
    
    if request.method == 'POST' and form.validate():
        dropdown = form.dropdown.data
        keyword = form.keyword.data

        print(dropdown, keyword)
        

        QUERY = f"SELECT * FROM bhagvadgita WHERE LOWER({dropdown}) LIKE '%{keyword}%' LIMIT 20"
 
        try: 
            df = read_bhagvadgita(QUERY)
            df.reset_index(inplace=True) 
            return render_template('search.html', form = form, dataframe = json.loads(df.to_json(orient = 'records')))

        except: 
             print('there is a problem.') 
    return render_template('search.html', form = form)

    


  
@app.route('/latest')
def latest():
    df = read_bhagvadgita('SELECT * FROM BHAGVADGITA ORDER BY BHAGVADGITA_ID ASC LIMIT 700')
    df.reset_index(inplace = True)

    return render_template('latest.html', dataframe = json.loads(df.to_json(orient = 'records')))

class Bhagvadgita(Form):
    chapter_no = StringField('Chapter number of the shloka: ', validators=[validators.Length(min=3, max=50), validators.DataRequired()])
    verse_no = StringField('Verse number of the shloka: ', validators=[validators.Length(min=3, max=50), validators.DataRequired()])
    shloka = TextAreaField('Shloka of the bhagvadgita: ', validators=[validators.Length(min=10), validators.DataRequired()])
    english_translation = TextAreaField('English translation of the shloka: ', validators=[validators.Length(min=10), validators.DataRequired()])
    explanation= TextAreaField('Explanation of the shloka:', validators=[validators.Length(min=10), validators.DataRequired()])
    



if __name__ == '__main__':
    app.run(port=700, debug=True)