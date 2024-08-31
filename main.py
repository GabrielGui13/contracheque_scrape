from utils.excel_flow import write_excel_flow
from utils.functions import detect_all_duplicate_excel, detect_duplicate_excel, alert_box
from time import sleep
import pyautogui

def main():
  print("Olá! Bem-vindo ao sistema de automação de extração das planilhas de consulta de contracheque de pensionistas!\n")
  
  print("Aperte CTRL + C a qualquer momento para encerrar.\n")
  
  while True:
    print("\nQual funcionalidade você deseja utilizar?")
    print("1- Extração de contracheque de pensionistas para planilhas")
    print("2- Baixar PDF dos contracheques de uma pessoa")
    print("3- Sair")
    
    choice = int(input(""))
    
    if choice == 1:
      write_excel_flow()
      break
    elif choice == 2:
      print("Funcionalidade em construção!")
      continue
    elif choice == 3:
      print("Obrigado por utilizar o sistema de automação de contracheques de pensionistas!")
      break
    else:
      print("Opção inválida! Tente novamente.")
      continue

try:
  main()
except Exception as error:
  print("\nOcorreu algum erro! Por favor tente novamente.")
  print(f"Erro: {error}")
  alert_box("Erro", f"Ocorreu algum erro! Por favor tente novamente.\n\nErro: {error}", "OK")
finally:
  print("\nAperte qualquer botão para encerrar o processo.", end=" ")
  input()