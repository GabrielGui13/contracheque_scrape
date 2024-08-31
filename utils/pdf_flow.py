from selenium import webdriver

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
  
  # http://servicos.searh.rn.gov.br/searh/copag/contra_cheque_pensionistas.asp
  # https://templated.io/blog/how-to-convert-html-to-pdf-with-python/
  # https://stackoverflow.com/questions/76281743/is-there-a-way-to-have-already-typed-text-after-the-input-in-python
  
  options = webdriver.ChromeOptions()
  options.add_experimental_option('excludeSwitches', ['enable-logging'])
 
  driver:WebDriver = webdriver.Chrome(options=options)
  driver.maximize_window()
  
  