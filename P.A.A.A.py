import os
import re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk

# Baixar pacotes necessários do NLTK
nltk.download('punkt')

def ler_arquivos(caminhos):
    conteudos = []
    for caminho in caminhos:
        if os.path.exists(caminho):
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
                conteudos.append((caminho, conteudo))
                print(f'Conteúdo do arquivo {caminho}:')
                print(conteudo)
                print('-' * 40)
        else:
            print(f'O arquivo {caminho} não existe.')
    return conteudos

def extrair_numeros(conteudo):
    # Usar expressão regular para encontrar todos os números no texto
    return [float(num) for num in re.findall(r'\b\d+\.?\d*\b', conteudo)]

def analisar_conteudo(conteudo):
    num_caracteres = len(conteudo)
    num_palavras = len(word_tokenize(conteudo))
    
    palavras = word_tokenize(conteudo.lower())
    freq_dist = FreqDist(palavras)
    
    # Extração de palavras-chave com base em frequência
    palavras_comuns = freq_dist.most_common(5)
    
    return {
        'num_caracteres': num_caracteres,
        'num_palavras': num_palavras,
        'palavras_comuns': palavras_comuns,
        'numeros': extrair_numeros(conteudo)
    }

def realizar_operacao(numeros):
    if not numeros:
        print("Nenhum número encontrado para realizar operações.")
        return
    
    print(f'Números encontrados: {numeros}')
    operacao = input("Escolha uma operação (soma, subtracao, multiplicacao, divisao): ").strip().lower()
    
    if operacao == 'soma':
        resultado = sum(numeros)
    elif operacao == 'subtracao':
        if len(numeros) < 2:
            print("Pelo menos dois números são necessários para subtração.")
            return
        resultado = numeros[0]
        for num in numeros[1:]:
            resultado -= num
    elif operacao == 'multiplicacao':
        resultado = 1
        for num in numeros:
            resultado *= num
    elif operacao == 'divisao':
        if len(numeros) < 2:
            print("Pelo menos dois números são necessários para divisão.")
            return
        resultado = numeros[0]
        for num in numeros[1:]:
            if num == 0:
                print("Não é possível dividir por zero.")
                return
            resultado /= num
    else:
        print("Operação inválida.")
        return

    print(f'Resultado da operação ({operacao}): {resultado}')

def gerar_resumo(conteudos):
    resumo = ""
    for caminho, conteudo in conteudos:
        analise = analisar_conteudo(conteudo)
        resumo += (f'Análise do arquivo {caminho}:\n'
                   f'  Número de caracteres: {analise["num_caracteres"]}\n'
                   f'  Número de palavras: {analise["num_palavras"]}\n'
                   f'  Palavras mais comuns:\n')
        for palavra, frequencia in analise['palavras_comuns']:
            resumo += f'    {palavra}: {frequencia}\n'
        
        if analise['numeros']:
            print(f'Arquivo {caminho} contém números: {analise["numeros"]}')
            realizar_operacao(analise['numeros'])
        
        resumo += '-' * 40 + '\n'
    
    return resumo

def main():
    arquivos = ['arquivo1.txt', 'arquivo2.txt', 'arquivo3.txt']  # Lista dos caminhos dos arquivos
    conteudos = ler_arquivos(arquivos)
    resumo = gerar_resumo(conteudos)

    print('Resumo dos arquivos:')
    print(resumo)

if __name__ == "__main__":
    main()