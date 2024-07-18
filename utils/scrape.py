import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from time import time
from utils.functions import convertMonth
from utils.excel import readExcel, writeExcel

def scrape(df):	
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
		comp_margem_consignavel = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[1]/div/font/b/font[2]/font').text
		comp_total_vantagens = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[2]/div/font/font[2]/b').text
		comp_liquido = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[4]/p/font/font[2]/b').text
		comp_periodo = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[3]/p/font/font[2]').text
		
		comp_disc_rows = driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr')
		
		pessoa = {
			"nome": str(comp_nome),
			"cpf": (comp_cpf),
			"matricula": (comp_matricula),
			"vinculo": int(comp_vinculo),
			"numpens": int(comp_numpens),
			"margem_consignavel": str(comp_margem_consignavel),	
			"total_vantagens": str(comp_total_vantagens),
			"liquido": str(comp_liquido),
			"periodo": str(comp_periodo)
		}
		
		pessoa_van = {
			"codvan": [],
			"discriminacaovan": [],
			"valorvan": [],
		}
		vanqt = 0
		
		pessoa_des = {
			"coddes": [],
			"discriminacaodes": [],
			"valordes": [],
			"desqt": 0
		}
		desqt = 0
		
		for j in range(1, len(comp_disc_rows) - 1):
			codigo_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[1]/font/b/font/font"
			discriminacao_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[2]/font/b/font/font"
			vantagens_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[3]/font/b/font/font"
			descontos_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[4]/font/b/font/b/font/font"
			# /html/body/table[3]/tbody/tr[4]/td[4]/font/b/font/b/font/font

			codigo = driver.find_element(By.XPATH, codigo_xpath).text
			discriminacao = driver.find_element(By.XPATH, discriminacao_xpath).text
			valorvan = driver.find_element(By.XPATH, vantagens_xpath).text
			valordes = driver.find_element(By.XPATH, descontos_xpath).text

			if int(codigo) == 913 or int(codigo) == 534 or int(codigo) == 508:
				pessoa_des["coddes"].append(codigo)
				pessoa_des["discriminacaodes"].append(discriminacao)
				pessoa_des["valordes"].append(valordes)
				desqt+=1
			elif valorvan != ' ':      
				pessoa_van["codvan"].append(codigo)
				pessoa_van["discriminacaovan"].append(discriminacao)
				pessoa_van["valorvan"].append(valorvan)
				vanqt+=1

		for v in range(vanqt):
			pessoa[f"CODVAN {v + 1}"] = pessoa_van["codvan"][v]
			pessoa[f"DISCRIMINAÇÃO VAN {v + 1}"] = pessoa_van["discriminacaovan"][v]
			pessoa[f"VALORVAN {v + 1}"] = pessoa_van["valorvan"][v]

		for d in range(desqt):
			pessoa[f"CODDES {d + 1}"] = pessoa_des["coddes"][d]
			pessoa[f"DISCRIMINAÇÃO DES {d + 1}"] = pessoa_des["discriminacaodes"][d]
			pessoa[f"VALORDES {d + 1}"] = pessoa_des["valordes"][d]

		pessoas.append(pessoa)

	print("Tempo de execução:", f'{time() - initial_time:.2f} segundos')

	driver.quit()
	
	return pessoas
