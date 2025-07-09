from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Função para calcular os dígitos verificadores do CNPJ
def calcular_dv(cnpj_base, pesos):
    soma = sum([int(cnpj_base[i]) * pesos[i] for i in range(len(cnpj_base))])
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto

# Função para gerar um CNPJ válido
def gerar_cnpj():
    # Geração da base do CNPJ: 8 primeiros números (raiz do CNPJ)
    cnpj_base = ''.join([str(random.randint(0, 9)) for _ in range(8)])

    # Adicionando os 4 primeiros números do CNPJ, por exemplo "0001"
    cnpj_base += '0001'

    # Cálculo do primeiro dígito verificador
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv1 = calcular_dv(cnpj_base, pesos_1)

    # Cálculo do segundo dígito verificador
    cnpj_base_com_dv1 = cnpj_base + str(dv1)
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv2 = calcular_dv(cnpj_base_com_dv1, pesos_2)

    # Construção do CNPJ final
    cnpj = cnpj_base + str(dv1) + str(dv2)

    # Formatação do CNPJ no formato 00.000.000/0001-00
    cnpj_formatado = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'

    return cnpj_formatado

# Função para validar um CNPJ
def validar_cnpj(cnpj):
    # Remover caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verificar se o CNPJ tem 14 caracteres
    if len(cnpj) != 14:
        return False

    # CNPJ's falsos que possuem todos os números iguais
    if cnpj == cnpj[0] * len(cnpj):
        return False

    # Separar a base do CNPJ (sem os dois últimos dígitos verificadores)
    cnpj_base = cnpj[:12]

    # Cálculo do primeiro dígito verificador
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv1 = calcular_dv(cnpj_base, pesos_1)

    # Cálculo do segundo dígito verificador
    cnpj_base_com_dv1 = cnpj_base + str(dv1)
    pesos_2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    dv2 = calcular_dv(cnpj_base_com_dv1, pesos_2)

    # Verificar se os dígitos verificadores calculados são iguais aos fornecidos
    if int(cnpj[12]) == dv1 and int(cnpj[13]) == dv2:
        return True
    return False

@app.route("/", methods=["GET", "POST"])
def index():
    mensagem = ""
    cnpj_gerado = None

    if request.method == "POST":
        cnpj_input = request.form.get("cnpj")
        if 'gerar' in request.form:
            cnpj_gerado = gerar_cnpj()
        elif 'validar' in request.form:
            if validar_cnpj(cnpj_input):
                mensagem = f'O CNPJ {cnpj_input} é válido!'
            else:
                mensagem = f'O CNPJ {cnpj_input} é inválido!'

    return render_template("cnpj.html", mensagem=mensagem, cnpj_gerado=cnpj_gerado)

if __name__ == "__main__":
    app.run(debug=True)
