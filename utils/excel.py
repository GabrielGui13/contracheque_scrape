import pandas as pd
from os import listdir, chdir
from datetime import datetime, UTC

def findExcel(io):
  files = listdir(f"./planilhas/{io}")
  filtered_files = []
  
  for i in files:
    if i.endswith('.xlsx'):
      filtered_files.append(i)  
  
  return filtered_files

def readExcel(name):
  df = pd.read_excel(f'./planilhas/entrada/{name}')
  
  df.rename(columns={'Matrícula(com o dígito)': 'matricula'}, inplace=True)
  df.rename(columns={'Vínculo': 'vinculo'}, inplace=True)
  df.rename(columns={'CPF(do(a) Pensionista)': 'cpf'}, inplace=True)
  df.rename(columns={'N.º Pensionista': 'numpens'}, inplace=True)
  df.rename(columns={'Mês': 'mes'}, inplace=True)
  df.rename(columns={'ano': 'ano'}, inplace=True)
  
  return df

def writeExcel(dictionary, name):
  df = pd.DataFrame(dictionary)
  
  df.rename(columns={'nome': 'NOME'}, inplace=True)
  df.rename(columns={'cpf': 'CPF'}, inplace=True)
  df.rename(columns={'matricula': 'MATRÍCULA'}, inplace=True)
  df.rename(columns={'vinculo': 'VINC.'}, inplace=True)
  df.rename(columns={'periodo': 'PERÍODO'}, inplace=True)
  df.rename(columns={'numpens': 'Nº PENSIONISTA'}, inplace=True)
  df.rename(columns={'total_vantagens': 'TOTAL DE VANTAGENS'}, inplace=True)
  df.rename(columns={'liquido': 'LIQUIDO A RECEBER'}, inplace=True)
  df.rename(columns={'codigo': 'CÓDIGO'}, inplace=True)
  df.rename(columns={'discriminacao': 'DISCRIMINAÇÃO'}, inplace=True)
  df.rename(columns={'vantagens': 'VANTAGENS'}, inplace=True)
  df.rename(columns={'margem_consignavel': 'MARGEM CONSIGNÁVEL'}, inplace=True)
  df.drop('vanqt', axis=1, inplace=True)
  df.drop(index=df.index[0], axis=0, inplace=True)
  
  time_now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

  excel_name = f'./planilhas/saida/{time_now}_format_{name}'
    
  df.to_excel(excel_name, index=False)
  
  return excel_name