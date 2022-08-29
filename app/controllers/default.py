from app import app
from flask import render_template, redirect, request, flash, url_for
from app.forms.formularios import FormCpf
import json

# Trata o CPF retirando os caracteres indesejados
def trata_cpf(cpf):
    cpf = str(cpf)
    caracter = ",.-+/ '=*<;:>!@#$%&*)("
    for x in range(len(caracter)):
        cpf = cpf.replace(caracter[x], "")
    return cpf


# Valida digito verificador
def verificador_cpf(cpf, mult=10):
    verifica = 0
    cpf = list(map(int, cpf))
    for x in cpf:
        x = int(x)
        verifica += x * mult
        if mult == 2:
            break
        mult -= 1
    soma = ((verifica * 10) % 11)
    if soma == 10:
        soma = 0
    return soma


# Acrescenta os caracters separadores do CPF
def padroniza_cpf(cpf):
    cpf_final = ''
    for i, item in enumerate(cpf):
        cpf_final += item
        if i == 2 or i == 5:
            cpf_final += '.'
        if i == 8:
            cpf_final += '-'
    return cpf_final


# Valida os digitos verificadores do CPF
def validacao(soma1, soma2, digi1, digi2):
    if soma1 == digi1 and soma2 == digi2:
        return True
    else:
        return False


def codigo(cpf):
    cpf = list(cpf)
    soma1 = verificador_cpf(cpf)
    soma2 = verificador_cpf(cpf, mult=11)
    digi1 = int(cpf[9])
    digi2 = int(cpf[10])
    cpf_final = padroniza_cpf(cpf)
    valida = validacao(soma1, soma2, digi1, digi2)
    return cpf_final, valida


@app.route("/", methods=['GET', 'POST'])
def home():
    form_cpf = FormCpf()
    cpf = trata_cpf(form_cpf.cpf.data)
    valida = False
    cpf_final = ''
    # Validação dos digitos verificadores
    if form_cpf.validate_on_submit() and 'botao_submit_cpf' in request.form:
        if not cpf.isnumeric():
            valida = False
            flash('Digite só números!', 'alert-danger')
            return redirect(url_for('home'))
        cpf_final, valida = codigo(cpf)
    return render_template('home.html', form_cpf=form_cpf, cpf_final=cpf_final, valida=valida)


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route("/json/<lista>", methods=['GET'] )
def solicitacao(lista):
    lista = lista.split(';')
    resultado = {}
    for cpf in lista:
        cpf = trata_cpf(cpf)
        status, valida = codigo(cpf)
        if cpf not in resultado.keys():
            if valida:
                resultado[cpf] = {"mensage": "CPF válido"}
            else:
                resultado[cpf] = {"mensage": "CPF não válido"}

    return json.dumps(resultado, ensure_ascii = False, allow_nan=True, indent = 6)