from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)

class CPF:
    def __init__(self):
        self.estados = {
            1: ["GO", "MT", "MS", "TO"],
            2: ["AC", "AP", "AM", "PA", "RO", "RR"],
            3: ["CE", "MA", "PI"],
            4: ["AL", "PB", "PE", "RN"],
            5: ["BA", "SE"],
            6: ["MG"],
            7: ["RJ", "ES"],
            8: ["SP"],
            9: ["PR", "SC"],
            0: ["RS"]
        }

    def formatar_cpf(self, cpf):
        """Formata o CPF no padrão xxx.xxx.xxx-xx"""
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def gerar_cpf(self, estado=None, formatar=False):
        """Gera um CPF válido"""
        while True:
            cpf = [randint(0, 9) for _ in range(9)]  # Gera os 9 primeiros números do CPF

            if estado:
                for x in self.estados:
                    if estado in self.estados[x]:
                        cpf[8] = x  # Atribui o código do estado ao último número do CPF
                        break

            if not all(c == cpf[0] for c in cpf):  # Verifica se não são todos iguais
                break

        # Cálculo do primeiro dígito verificador (X)
        soma1 = sum(cpf[i] * (10 - i) for i in range(9))
        digito1 = (soma1 * 10) % 11
        digito1 = digito1 if digito1 < 10 else 0

        # Cálculo do segundo dígito verificador (Y)
        soma2 = sum(cpf[i] * (11 - i) for i in range(9)) + digito1 * 2
        digito2 = (soma2 * 10) % 11
        digito2 = digito2 if digito2 < 10 else 0

        # Adiciona os dois dígitos verificadores
        cpf.append(digito1)
        cpf.append(digito2)

        # Converte a lista para uma string
        cpf_str = "".join(map(str, cpf))

        # Formata o CPF, se necessário
        if formatar:
            cpf_str = self.formatar_cpf(cpf_str)

        return cpf_str

def validar_cpf(cpf: str) -> bool:
    # Remove qualquer caractere não numérico
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Não permite CPFs "famosos" como 111.111.111-11, 222.222.222-22, etc.
    if cpf == cpf[0] * 11:
        return False

    # Validação do primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # Validação do segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # Verifica se os dígitos verificadores são iguais aos informados
    if int(cpf[9]) == digito1 and int(cpf[10]) == digito2:
        return True
    return False

@app.route("/Geradores/projeto-cpf/templates/", methods=["GET", "POST"])
def index():
    estado = None
    cpf_gerado = None
    resultado = None
    resultado_tipo = ""
    cpf = request.form.get("cpf", "")  # Inicializa como string vazia caso não haja CPF

    if request.method == "POST":
        if "cpf" in request.form:  # Verifica se o formulário de validação de CPF foi enviado
            cpf = request.form["cpf"]
            if validar_cpf(cpf):
                resultado = f"CPF {cpf} é válido!"
                resultado_tipo = "valido"  # Define o tipo como "valido"
            else:
                resultado = f"CPF {cpf} é inválido!"
                resultado_tipo = "invalido"  # Define o tipo como "invalido"
        elif "estado" in request.form:  # Verifica se o formulário de estado foi enviado
            estado = request.form["estado"]
            cpf_obj = CPF()
            cpf_gerado = cpf_obj.gerar_cpf(estado, True)  # Gera o CPF com formatação
            resultado = None  # Limpa o resultado de validação ao gerar o CPF
            resultado_tipo = ""

    return render_template("index.html", resultado=resultado, cpf=cpf, estado=estado, cpf_gerado=cpf_gerado, resultado_tipo=resultado_tipo)

if __name__ == "__main__":
    app.run(debug=True)
