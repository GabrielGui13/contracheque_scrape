from selenium import webdriver
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from time import time
from utils.functions import convert_month, convert_seconds_to_formatted_time
from functools import cmp_to_key

def scrape(df, name):
  print(f"Iniciando extração da planilha: {name}\n")
  
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
  driver:WebDriver = webdriver.Chrome(options=options)
  driver.maximize_window()
 
  initial_time = time()
  pessoas = []
  pessoas_sem_registro = []
  van_codes_indexes = []
  
  pessoa_van_template = {
    "nome": "",
    "cpf": "",
    "matricula": "",
    "vinculo": "",
    "numpens": "",
    "margem_consignavel": "",	
    "total_vantagens": "",
    "liquido": "",
    "periodo": "",
    "vanqt": 0,
  }
  
  pessoa_des_template = {
    "CODDES 1": "",
    "DISCRIMINAÇÃO DES 1": "",
    "VALORDES 1": "",
    "CODDES 2": "",
    "DISCRIMINAÇÃO DES 2": "",
    "VALORDES 2": "",
    "CODDES 3": "",
    "DISCRIMINAÇÃO DES 3": "",
    "VALORDES 3": "",
  }
  
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
    
    box_matricula.send_keys(str(df['matricula'][i]))
    box_vinculo.send_keys(str(df['vinculo'][i]))
    box_cpf.send_keys(str(df['cpf'][i]))
    box_numpens.send_keys(str(df['numpens'][i]))
    box_mes_choice = driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div/div/div[2]/form/div[5]/select/option[{convert_month(df['mes'][i])}]")
    box_mes_choice.click()
    box_ano.send_keys(str(df['ano'][i]))
    
    box_form.submit()
    
    comp_disc_rows = driver.find_elements(By.XPATH, '/html/body/table[3]/tbody/tr')
    current_url = driver.current_url
    
    motivo = ''
    if current_url.find('contrachk') == -1:
      if len(current_url.split('&')) == 1:
        motivo = 'Usuário não permite a visualização de seu contracheque.'
      elif len(current_url.split('&')) == 5:
        motivo = 'Registro não encontrado.'
      else:
        motivo = 'Motivo não encontrado ou desconhecido.'
        
      pessoas_sem_registro.append({
        "Matrícula(com o dígito)": df['matricula'][i],
        "Vínculo": df['vinculo'][i],
        "CPF(do(a) Pensionista)": df['cpf'][i],
        "N.º Pensionista": df['numpens'][i],
        "Mês": df['mes'][i],
        "ano": df['ano'][i],
        "Motivo": motivo,
      })
      
      print(f"{i + 1}: CPF => {df['cpf'][i]} e Matrícula => {df['matricula'][i]} não extraído(s). ({motivo})")
      
      continue
    elif len(comp_disc_rows) <= 2:
      motivo = 'Contracheque vazio.'
      
      pessoas_sem_registro.append({
        "Matrícula(com o dígito)": df['matricula'][i],
        "Vínculo": df['vinculo'][i],
        "CPF(do(a) Pensionista)": df['cpf'][i],
        "N.º Pensionista": df['numpens'][i],
        "Mês": df['mes'][i],
        "ano": df['ano'][i],
        "Motivo": motivo,
      })
      
      print(f"{i + 1}: CPF => {df['cpf'][i]} e Matrícula => {df['matricula'][i]} não extraído(s). ({motivo})")
      
      continue
    
    comp_nome:WebElement = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[1]/font/b/font').text
    comp_cpf = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[2]/td[3]/font[2]/font').text
    comp_matricula = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[2]/font/font[2]').text
    comp_vinculo = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[3]/font/font[2]').text
    comp_numpens = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr[1]/td[4]/font[2]/font').text
    comp_margem_consignavel = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[1]/div/font/b/font[2]/font').text
    comp_total_vantagens = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[2]/div/font/font[2]/b').text
    comp_liquido = driver.find_element(By.XPATH, '/html/body/table[4]/tbody/tr/td[4]/p/font/font[2]/b').text
    comp_periodo = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[3]/p/font/font[2]').text
    
    pessoa = {
      "nome": str(comp_nome),
      "cpf": int(comp_cpf),
      "matricula": (comp_matricula),
      "vinculo": int(comp_vinculo),
      "numpens": int(comp_numpens),
      "margem_consignavel": str(comp_margem_consignavel).replace('R$', '').replace('.', '').replace(',', '.').strip(),	
      "total_vantagens": str(comp_total_vantagens).replace('R$', '').replace('.', '').replace(',', '.').strip(),
      "liquido": str(comp_liquido).replace('R$', '').replace('.', '').replace(',', '.').strip(),
      "periodo": str(comp_periodo),
      "vanqt": 0,
    }
    
    pessoa_van = {
      "codvan": [],
      "discriminacaovan": [],
      "valorvan": [],
    }
  
    pessoa_des = {
      "CODDES 1": "",
      "DISCRIMINAÇÃO DES 1": "",
      "VALORDES 1": "",
      "CODDES 2": "",
      "DISCRIMINAÇÃO DES 2": "",
      "VALORDES 2": "",
      "CODDES 3": "",
      "DISCRIMINAÇÃO DES 3": "",
      "VALORDES 3": "",
    }
    
    for j in range(1, len(comp_disc_rows) - 1):
      codigo_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[1]/font/b/font/font"
      discriminacao_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[2]/font/b/font/font"
      vantagens_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[3]/font/b/font/font"
      descontos_xpath = "/html/body/table[3]/tbody/tr[" + str(j + 1) + "]/td[4]/font/b/font/b/font/font"

      codigo = driver.find_element(By.XPATH, codigo_xpath).text
      discriminacao = driver.find_element(By.XPATH, discriminacao_xpath).text
      valorvan = driver.find_element(By.XPATH, vantagens_xpath).text
      valordes = driver.find_element(By.XPATH, descontos_xpath).text
   
      if valorvan != ' ':      
        pessoa_van["codvan"].append(int(codigo))
        pessoa_van["discriminacaovan"].append(discriminacao)
        pessoa_van["valorvan"].append(str(valorvan).replace('R$', '').replace('.', '').replace(',', '.').strip())
        pessoa["vanqt"] = pessoa["vanqt"] + 1
      elif int(codigo) == 913:
        pessoa_des["CODDES 1"] = int(codigo)
        pessoa_des["DISCRIMINAÇÃO DES 1"] = discriminacao
        pessoa_des["VALORDES 1"] = str(valordes).replace('R$', '').replace('.', '').replace(',', '.').strip()
      elif int(codigo) == 534:
        pessoa_des["CODDES 2"] = int(codigo)
        pessoa_des["DISCRIMINAÇÃO DES 2"] = discriminacao
        pessoa_des["VALORDES 2"] = str(valordes).replace('R$', '').replace('.', '').replace(',', '.').strip()
      elif int(codigo) == 508:
        pessoa_des["CODDES 3"] = int(codigo)
        pessoa_des["DISCRIMINAÇÃO DES 3"] = discriminacao
        pessoa_des["VALORDES 3"] = str(valordes).replace('R$', '').replace('.', '').replace(',', '.').strip()
    
    for v in range(pessoa["vanqt"]):
      findable_aux_van_codes_indexes = np.array(van_codes_indexes)
      van_code_index = np.where(findable_aux_van_codes_indexes == pessoa_van["codvan"][v])[0]
      
      if len(van_code_index) != 0:        
        pessoa[f"CODVAN {van_code_index[0] + 1}"] = pessoa_van["codvan"][v]
        pessoa[f"DISCRIMINAÇÃO VAN {van_code_index[0] + 1}"] = pessoa_van["discriminacaovan"][v]
        pessoa[f"VALORVAN {van_code_index[0] + 1}"] = str(pessoa_van["valorvan"][v])
      else:
        van_codes_indexes.append(pessoa_van["codvan"][v])
        new_van_code_index = len(van_codes_indexes)
        
        pessoa[f"CODVAN {new_van_code_index}"] = pessoa_van["codvan"][v]
        pessoa[f"DISCRIMINAÇÃO VAN {new_van_code_index}"] = pessoa_van["discriminacaovan"][v]
        pessoa[f"VALORVAN {new_van_code_index}"] = str(pessoa_van["valorvan"][v])
        
        pessoa_van_template[f"CODVAN {new_van_code_index}"] = ""
        pessoa_van_template[f"DISCRIMINAÇÃO VAN {new_van_code_index}"] = ""
        pessoa_van_template[f"VALORVAN {new_van_code_index}"] = ""
   
    pessoa.update(pessoa_des)
    pessoas.append(pessoa)
    
    print(f"{i + 1}: {pessoa['nome']} ({pessoa['cpf']}) extraído.")
  
  print(f"\nA planilha '{name}' foi extraída com sucesso! Tempo de execução:", f'{convert_seconds_to_formatted_time(time() - initial_time)}\n')

  driver.quit()

  pessoa_van_template.update(pessoa_des_template)
  pessoas.insert(0, pessoa_van_template)
  
  return [pessoas, pessoas_sem_registro]
