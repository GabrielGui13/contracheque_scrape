import pandas as pd

def readExcel(name):
	df = pd.read_excel(f'planilhas/{name}.xlsx')

	df.rename(columns={'Matrícula(com o dígito)': 'matricula'}, inplace=True)
	df.rename(columns={'Vínculo': 'vinculo'}, inplace=True)
	df.rename(columns={'CPF(do(a) Pensionista)': 'cpf'}, inplace=True)
	df.rename(columns={'N.º Pensionista': 'numpens'}, inplace=True)
	df.rename(columns={'Mês': 'mes'}, inplace=True)
	df.rename(columns={'ano': 'ano'}, inplace=True)
  
	return df

def writeExcel(dictionary):
  df = pd.DataFrame(dictionary)
  
  df.rename(columns={'nome': 'NOME'}, inplace=True)
  df.rename(columns={'cpf': 'CPF'}, inplace=True)
  df.rename(columns={'matricula': 'MATRÍCULA'}, inplace=True)
  df.rename(columns={'vinculo': 'VINC.'}, inplace=True)
  df.rename(columns={'numpens': 'Nº PENSIONISTA'}, inplace=True)
  df.rename(columns={'total_vantagens': 'TOTAL DE VANTAGENS'}, inplace=True)
  df.rename(columns={'liquido': 'LIQUIDO A RECEBER'}, inplace=True)
  df.rename(columns={'codigo': 'CÓDIGO'}, inplace=True)
  df.rename(columns={'discriminacao': 'DISCRIMINAÇÃO'}, inplace=True)
  df.rename(columns={'vantagens': 'VANTAGENS'}, inplace=True)
  df.rename(columns={'margem_consignavel': 'MARGEM CONSIGNÁVEL'}, inplace=True)
  
  print(df)
  
  df.to_excel('planilhas/planilhafinal.xlsx', index=False) 