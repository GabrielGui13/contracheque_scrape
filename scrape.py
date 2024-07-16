import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep 
from utils.functions import convertMonth

df = pd.read_excel('planilhabase/planilhabase.xlsx')

df.rename(columns={'Matrícula(com o dígito)': 'matricula'}, inplace=True)
df.rename(columns={'Vínculo': 'vinculo'}, inplace=True)
df.rename(columns={'CPF(do(a) Pensionista)': 'cpf'}, inplace=True)
df.rename(columns={'N.º Pensionista': 'numpens'}, inplace=True)
df.rename(columns={'Mês': 'mes'}, inplace=True)
df.rename(columns={'ano': 'ano'}, inplace=True)

driver = webdriver.Chrome()
driver.get('http://servicos.searh.rn.gov.br/searh/copag/contra_cheque_pensionistas.asp')

box_form = driver.find_element(By.ID, 'frmDados')

box_matricula = driver.find_element(By.ID, 'matricula')
box_vinculo = driver.find_element(By.ID, 'vinculo')
box_cpf = driver.find_element(By.ID, 'cpf')
box_numpens = driver.find_element(By.ID, 'numpens')
box_mes = driver.find_element(By.ID, 'mes')
box_mes.click()
box_ano = driver.find_element(By.ID, 'ano')

box_matricula.send_keys(str(df.matricula[0]))
box_vinculo.send_keys(str(df['vinculo'][0]))
box_cpf.send_keys(str(df['cpf'][0]))
box_numpens.send_keys(str(df['numpens'][0]))
box_mes_choice = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/form/div[5]/select/option[{convertMonth(df['mes'][0])}]')
box_mes_choice.click()
# box_mes.send_keys(convertMonth(df['mes'][0]))
box_ano.send_keys(str(df['ano'][0]))

box_form.submit()
sleep(5)

input()
driver.quit()

# for i in range(len(df)):
# 	print(i)