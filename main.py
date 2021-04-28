import os
import numpy as np
import pandas as pd
from cleaner import Cleaner
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

THIS_FOLDER = os.getcwd()
my_file = os.path.join(THIS_FOLDER,"sentencas_mod.csv")
my_file1 = os.path.join(THIS_FOLDER,"sentencas_original.csv")

with open(my_file) as file:
    dataset = pd.read_csv(my_file)
    dataset_original = pd.read_csv(my_file1).drop(columns=['Timestamp'])

def performance_modelo(dataset,model):
    Sentenca = dataset.iloc[:,1]
    Intencoes = dataset.iloc[:,0]
    cleaner = Cleaner()
    Sentenca_cleaned = [cleaner.clean_text(x) for x in Sentenca]
    Sentenca_counts = CountVectorizer().fit_transform(Sentenca_cleaned)
    X_train, X_test, y_train, y_test = train_test_split(Sentenca_counts, Intencoes,test_size=0.15, random_state=1)
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    accuracy_score_model = accuracy_score(y_test, y_pred)
    return print(f"A acurácia do model é de {accuracy_score_model*100:.1f}%")


model = MultinomialNB()
dataset_original =  dataset_original

#Descomentar a linha abaixo para ver a performance do modelo
#performance_modelo(dataset_original,model)

def salva_csv(dataframe):
    dataframe.to_csv('sentencas_mod.csv',index=False)

def checa_input_int(input_resp=str):
    while True:
        try:
            resposta = int(input_resp)
            break
        except:
            print("Essa resposta não é valida")
            input_resp = input()
    return resposta


def interpretacao_sentenca(counts_da_nova_sentenca,nova_sentenca):
    global dataset
    proba = model.predict_proba(counts_da_nova_sentenca[0])[0]
    result = np.where(proba>=0.5)
    if len(result[0]) > 0:
        #checa_input_int(f"A sua intenção é: {model.predict(counts_da_nova_sentenca[0])[0]}? Digite 1 para confirmar ou 0 para negar")
        print(f"A sua intenção é: {model.predict(counts_da_nova_sentenca[0])[0]}? Digite 1 para confirmar ou 0 para negar")
        confirmacao = checa_input_int(input())
        if int(confirmacao) == 1:
            dataset = dataset.append({"Intenção":model.predict(counts_da_nova_sentenca[0])[0],"Sentença":nova_sentenca},ignore_index=True)
            salva_csv(dataset)
            print("Obrigado!")
        else:
            intencoes_selection = '[1]Consultar saldo da conta [2]Interagir com a luz ou o ar-condicionado [3]Obter informações relativas ao clima [4]Digitei Abobrinha'
            print(f"Poderia me informar qual dessas era sua intenção?{intencoes_selection}")
            resp_intencao = checa_input_int(input())
            if int(resp_intencao) != 4:
                dataset = dataset.append({"Intenção":model.classes_[int(resp_intencao)-1],"Sentença":nova_sentenca},ignore_index=True)
                salva_csv(dataset)
    else:
        print("Não Entendi...Qual era sua intenção?")
        intencoes_selection = '[1]Consultar saldo da conta [2]Interagir com a luz ou o ar-condicionado [3]Obter informações relativas ao clima [4]Digitei Abobrinha'
        print(f"{intencoes_selection}")
        resp_intencao = checa_input_int(input())
        if int(resp_intencao) in [1,2,3]:
            dataset = dataset.append({"Intenção":model.classes_[int(resp_intencao)-1],"Sentença":nova_sentenca},ignore_index=True)
            salva_csv(dataset)
        
        
def main(dataset,model):
    Sentenca = dataset.iloc[:,1]
    Intencoes = dataset.iloc[:,0]
    cleaner = Cleaner()
    Sentenca_cleaned = [cleaner.clean_text(x) for x in Sentenca]
    vectorizer = CountVectorizer()
    Sentenca_counts = vectorizer.fit_transform(Sentenca_cleaned)
    model.fit(Sentenca_counts,Intencoes)
    print("Digite um comando:")
    nova_sentenca = input()
    nova_sentenca_clean = cleaner.clean_text(nova_sentenca)
    #nova_sentenca = "liga a luz"
    counts_da_nova_sentenca = vectorizer.transform([cleaner.clean_text(nova_sentenca_clean)])
    interpretacao_sentenca(counts_da_nova_sentenca,nova_sentenca)



model = MultinomialNB()
dataset =  dataset

main(dataset,model)