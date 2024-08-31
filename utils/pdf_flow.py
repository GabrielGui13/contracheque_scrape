from selenium import webdriver
from utils.functions import convert_month, convert_seconds_to_formatted_time

def pdf_flow():
  print(f"Forneça os dados do usuário a baixar os contracheques:\n")
  matricula= input("Matricula: ")
  cpf= input("Matricula: ")
  vinculo= input("Matricula: ")
  numpens= input("N.º Pensionista: ")
  mes_first= input("Mês inicial (1 a 12): ")
  ano_first= input("Ano inicial: ")
  mes_last= input("Mês final (1 a 12): ")
  ano_last= input("Ano final: ")
  
  # put a while and check validations for each one
  
  # http://servicos.searh.rn.gov.br/searh/copag/contra_cheque_pensionistas.asp
  # https://templated.io/blog/how-to-convert-html-to-pdf-with-python/
  # https://stackoverflow.com/questions/76281743/is-there-a-way-to-have-already-typed-text-after-the-input-in-python
  
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
  driver:WebDriver = webdriver.Chrome(options=options)
  driver.maximize_window()
  
  driver.get('http://servicos.searh.rn.gov.br/searh/copag/contra_cheque_pensionistas.asp')
  box_form = driver.find_element(By.ID, 'frmDados')
  
  box_matricula = driver.find_element(By.ID, 'matricula')
  box_vinculo = driver.find_element(By.ID, 'vinculo')
  box_cpf = driver.find_element(By.ID, 'cpf')
  box_numpens = driver.find_element(By.ID, 'numpens')
  box_mes = driver.find_element(By.ID, 'mes')
  box_mes.click()
  box_ano = driver.find_element(By.ID, 'ano')
  
  box_matricula.send_keys(str(matricula))
  box_vinculo.send_keys(str(vinculo))
  box_cpf.send_keys(str(cpf))
  box_numpens.send_keys(str(numpens))
  box_mes_choice = driver.find_element(By.XPATH, f"/html/body/div[1]/div[2]/div/div/div[2]/form/div[5]/select/option[{convert_month(mes_first)}]")
  box_mes_choice.click()
  box_ano.send_keys(str(df['ano'][i]))
  
  box_form.submit()
  
  