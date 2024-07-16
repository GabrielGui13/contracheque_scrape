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