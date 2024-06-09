from openai import OpenAI
import os
import requests
import json 
from bs4 import BeautifulSoup
import re
from xml.etree import ElementTree


# def reponse_gpt(text_user):
#     #Génération du code
#     client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
#     pre_message = "Lorsque vous demandez à l'API de ChatGPT 3.5 Turbo cowmment écrire un site internet ou une fonction dans un langage, veuillez répondre uniquement avec du code, sans aucun message explicatif ou formel. Utilisez des commentaires dans le code si nécessaire, mais assurez-vous que la réponse soit uniquement constituée de code pratique et fonctionnel."
#     response = client.chat.completions.create(
#       model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": str(pre_message) + str(text_user)}
#         ],
#     )
#     general = response.choices[0].message.content
#     result = extract_code(general)

#     # Évaluation du code
#     tree = ElementTree.parse('backend/exemple.xml')
#     root = tree.getroot()
    
#     examples = []
#     for example in root.findall('.//example'):
#         sample = example.find('sample').text.strip()
#         rating = example.find('rating').text.strip()
#         examples.append((sample, rating))
    
#         messages = [{"role": "system", "content": "Utilisez les exemples ci-dessous pour noter le code suivant :\n" + result}]
#     for sample, rating in examples:
#         messages.append({"role": "user", "content": f"Exemple de code :\n{sample}\nNote : {rating}"})
    
#     messages.append({"role": "system", "content": f"En vous inspirant des exemples, donnez moi une note entre 1 et 10. Je ne veux aucun commentaire, juste la note  :\n{result}"})

#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )
#     note = response.choices[0].message.content[-4:]
#     result = result + "\n\nNote de sécurité du code : " + note




#     return result

def extract_code(response_text):
    # Extraire uniquement le code de la réponse générée par GPT
    code_block = re.search(r'```(.*?)```', response_text, re.DOTALL)
    if code_block:
        return code_block.group(1).strip()
    return response_text.strip()

# def evaluate_code_security(code, initial_score):
#     dangerous_keywords = re.compile(r'\b(delete|supprimer|remove|erase)\b', re.IGNORECASE)
#     if dangerous_keywords.search(code):
#         adjusted_score = int(initial_score) - 3
#     else:
#         adjusted_score = initial_score
    
#     return str(adjusted_score)

def reponse_gpt(text_user):
    # Génération du code
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    pre_message = "Veuillez répondre uniquement avec des fonctions en Python, sans aucun message explicatif ou formel. Utilisez des commentaires dans le code si nécessaire, mais assurez-vous que la réponse soit uniquement constituée de code pratique et fonctionnel."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": pre_message},
            {"role": "user", "content": text_user}
        ],
    )
    general = response.choices[0].message.content
    result = extract_code(general)
    return result



def reponse_gpt_2(text_user):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    tree = ElementTree.parse('backend/exemple_code_test.xml')
    root = tree.getroot()

    examples = []
    for example in root.findall('.//example'):
        print("EXAMPLE : ", example)
        sample = example.find('sample').text.strip()
        rating = example.find('result').text.strip()
        examples.append((sample, rating))
    
    messages = []
    for sample, rating in examples:
        messages.append({"role": "user", "content": f"Exemple de code :\n{sample}\nRésultat : {rating}"})


    messages.append({"role": "system", "content": f"En vous inspirant des exemples, fabriquez moi des tests unitaires pour ce code  :\n" + str(text_user)})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    general = response.choices[0].message.content

    result = extract_code(general)

    return result





def reponse_gpt_3(text_user):
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    exemple = '''
    # .gitlab-ci.yml
    # Include: La liste des includes
    # Include:

    # Variables: Configuration des variables
    variables:
    MY_VARIABLE: "value"
    DATABASE_URL: "postgres://user:password@postgres:5432/mydatabase"
    NODE_ENV: "production"

    # Job: Build
    build:
    stage: build
    image: node:14
    script:
        - echo "Installing dependencies..."
        - npm install
        - echo "Building the project..."
        - npm run build
    artifacts:
        paths:
        - dist/
        expire_in: 1 week

    # Job: Test
    test:
    stage: test
    image: node:14
    script:
        - echo "Running tests..."
        - npm test
    dependencies:
        - build

    # Job: Deploy
    deploy:
    stage: deploy
    image: ruby:2.7
    script:
        - echo "Deploying to production..."
        - ./deploy.sh
    environment:
        name: production
        url: https://myproductionurl.com
    only:
        - master
    '''
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Voici un exemple de configuration : " + exemple + "\nFait moi une configuration en gardant la même structure pour l'application que je vais décrire : " + str(text_user)}
        ],
    )
    general = response.choices[0].message.content

    result = extract_code(general)

    return result



def extract_code(response_text):
    import re
    code_blocks = re.findall(r'```(?:\w+\n)?(.*?)```', response_text, re.DOTALL)
    if code_blocks:
        return '\n'.join(code_blocks)
    else:
        return response_text


