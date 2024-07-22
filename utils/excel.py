import pandas as pd
from os import listdir
from datetime import datetime, UTC

def find_excel(io):
  files = listdir(f"./planilhas/{io}")
  filtered_files = []
  
  for i in files:
    if i.endswith('.xlsx') and not i.startswith('~'):
      filtered_files.append(i)  
  
  return filtered_files

def read_excel(name):
  df = pd.read_excel(f'./planilhas/entrada/{name}')
  
  df.rename(columns={'Matrícula(com o dígito)': 'matricula'}, inplace=True)
  df.rename(columns={'Vínculo': 'vinculo'}, inplace=True)
  df.rename(columns={'CPF(do(a) Pensionista)': 'cpf'}, inplace=True)
  df.rename(columns={'N.º Pensionista': 'numpens'}, inplace=True)
  df.rename(columns={'Mês': 'mes'}, inplace=True)
  df.rename(columns={'ano': 'ano'}, inplace=True)
  
  return df

def write_excel(dictionary, name):
  df = pd.DataFrame(dictionary)
  
  # df["margem_consignavel"] = pd.to_numeric(df["margem_consignavel"])
  # df["total_vantagens"] = pd.to_numeric(df["total_vantagens"])
  # df["liquido"] = pd.to_numeric(df["liquido"])
  
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
  
  # # Iterate over each column in the dataframe
  # for column in df.columns:
  #     if df[column].dtype == 'string':  # Only process columns with object/string type
  #         # Check if the string begins with $  should be expanded ot other currencies as well but $ for now
  #         if df[column].str.startswith('R$').any():
  #             # Remove $ and commas from the values and convert to float with precision of 2
  #             df[column] = pd.to_numeric(df[column].str.replace('$', '').str.replace(',', '').str.replace(' ', ''))
  
  time_now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

  excel_name = f'./planilhas/saida/{time_now}_finalizado_{name}'
    
  df.to_excel(excel_name, index=False)
  
  return excel_name

def write_not_found_excel_clone(dictionary, name):
  if len(dictionary) > 0:
    df = pd.DataFrame(dictionary)
    
    time_now = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    excel_name = f'./planilhas/saida/{time_now}_erros_{name}'
      
    df.to_excel(excel_name, index=False)
    
    return excel_name
  
  return ''