import tkinter as tk
from tkinter import messagebox
import requests
import re

def remover_caracteres_nao_numericos(valor):
    return re.sub(r'\D', '', valor)

def buscar_cnpj(cnpj):
    url = f'https://minhareceita.org/{cnpj}'
    lista_cnaes = ['4623108', '4623199', '4632001', '4637107', '4639701', '4639702', '4646002', '4647801', '4649408', '4635499', '4637102', '4637199', '4644301','4632003', '4691500', '4693100', '3240099', '4649499', '8020000', '4711301', '4711302', '4712100', '4721103', '4721104', '4729699', '4761003', '4789005', '4771701', '4771702', '4771703', '4772500', '4763601']

    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            dados = resposta.json()
            cnae_codigo = str(dados.get('cnae_fiscal', []))
            print(cnae_codigo)
            if cnae_codigo in lista_cnaes:
                return cnae_codigo, "Não paga"
            else:
                return cnae_codigo, "Paga" 
        else:
            print(f"Falha na solicitação. Status code: {resposta.status_code}")
            return None
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None

def consultar_cnpj():
    cnpj = campo_texto.get("1.0", tk.END).strip()
    cnpj_limpo = remover_caracteres_nao_numericos(cnpj)
    
    if len(cnpj_limpo) != 14:
        resultado_label.config(text="Por favor, insira um CNPJ válido.", fg="red")
        return
    
    cnae, resultado = buscar_cnpj(cnpj_limpo)
    
    if resultado is not None:
        resultado_label.config(text=f"O CNPJ {cnpj_limpo} tem o CNAE {cnae} e  {resultado}", fg="black")
    else:
        resultado_label.config(text="Não foi possível obter informações sobre este CNPJ.", fg="red")

root = tk.Tk()
root.title("Consultor de cnae")
root.geometry("800x600")

label = tk.Label(root, text="Digite o cnpj que deseja procurar", font=("Arial", 12))
label.pack(pady=5)

campo_texto = tk.Text(root, height=2, width=50, font=("Arial", 16))
campo_texto.pack(pady=5)

btn = tk.Button(root, text="Consultar", command=consultar_cnpj)
btn.pack(pady=5)

resultado_label = tk.Label(root, text="", wraplength=400, font=("Arial", 12))
resultado_label.pack(pady=10)

root.mainloop()