from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from time import time
from utils.functions import convertMonth
from utils.excel import readExcel, writeExcel

df = readExcel(name='planilhabase')

driver:WebDriver = webdriver.Chrome()
driver.maximize_window()

initial_time = time()
pessoas = []

for i in range(len(df)):
  driver.get('http://servicos.searh.rn.gov.br/searh/copag/contra_cheque_pensionistas.asp')
  box_form = driver.find_element(By.ID, 'frmDados')
  
  box_matricula = driver.find_element(By.ID, 'matricula')
  box_vinculo = driver.find_element(By.ID, 'vinculo')
  box_cpf = driver.find_element(By.ID, 'cpf')
  box_numpens = driver.find_element(By.ID, 'numpens')
  box_mes = driver.find_element(By.ID, 'mes')
  box_mes.click()
  box_ano = driver.find_element(By.ID, 'ano')
  
  box_matricula.send_keys(str(df.matricula[i]))
  box_vinculo.send_keys(str(df['vinculo'][i]))
  box_cpf.send_keys(str(df['cpf'][i]))
  box_numpens.send_keys(str(df['numpens'][i]))
  box_mes_choice = driver.find_element(By.XPATH, f'/html/body/div[1]/div[2]/div/div/div[2]/form/div[5]/select/option[{convertMonth(df['mes'][i])}]')
  box_mes_choice.click()
  box_ano.send_keys(str(df['ano'][i]))
  
  box_form.submit()
  
  comp_nome:WebElement = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[1]/font/b/font').text
  comp_cpf = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[3]/font[2]/font').text
  comp_matricula = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[2]/font/font[2]').text
  comp_vinculo = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[3]/font/font[2]').text
  comp_numpens = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[4]/font[2]/font').text
  comp_total_vantagens = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[2]/div/font/font[2]/b').text
  comp_liquido = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[4]/p/font/font[2]/b').text
  
  comp_disc_rows = driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr')
  
  pessoa = {
		"nome": str(comp_nome),
		"cpf": (comp_cpf),
		"matricula": (comp_matricula),
		"vinculo": int(comp_vinculo),
		"numpens": int(comp_numpens),
		"total_vantagens": str(comp_total_vantagens),
		"liquido": str(comp_liquido),
		"codigo": [],
		"discriminacao": [],
		"vantagens": [],
		"compet": []
	}
  
  for j in range(1, len(comp_disc_rows) - 1):
    codigo_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[1]/font/b/font/font"
    discriminacao_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[2]/font/b/font/font"
    vantagens_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[3]/font/b/font/font"
    compet_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[5]/font/b/font/font"
    
    codigo = driver.find_element(By.XPATH, codigo_xpath).text
    discriminacao = driver.find_element(By.XPATH, discriminacao_xpath).text
    vantagens = driver.find_element(By.XPATH, vantagens_xpath).text
    compet = driver.find_element(By.XPATH, compet_xpath).text
    
    pessoa["codigo"].append(codigo)
    pessoa["discriminacao"].append(discriminacao)
    pessoa["vantagens"].append(vantagens)
    pessoa["compet"].append(compet)
    
  pessoas.append(pessoa)

writeExcel(pessoas)

print("Tempo de execução:", f'{time() - initial_time:.2f} segundos')

input()
driver.quit()