from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators


class FormCpf(FlaskForm):
    cpf = StringField('Digite o CPF.', {validators.Length(min=11, max=16)})
    botao_submit_cpf = SubmitField('Buscar')
