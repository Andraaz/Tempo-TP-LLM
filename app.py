from flask import Flask, render_template, request, jsonify
from backend import reponse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():                                                                                                                                                            
    text_input_1 = request.form.get('text_input_1')
    text_input_2 = request.form.get('text_input_2')
    text_input_yml = request.form.get('text_input_3')

    if text_input_1:
        result_1 = reponse.reponse_gpt(text_input_1)
    else : 
        result_1 = ""

    if text_input_2:
        result_2 = reponse.reponse_gpt_2(text_input_2)
    else : 
        result_2 = ""

    print("Input 1 ", text_input_1)
    print("TEST INPUT : ", text_input_yml)
    if text_input_yml:
        result_yml = reponse.reponse_gpt_3(text_input_yml)
    else : 
        result_yml = ""
    print("Resultat : ", result_yml)
    return jsonify(result_1=result_1, result_2=result_2, result_3=result_yml)

if __name__ == '__main__':
    app.run(debug=True)
