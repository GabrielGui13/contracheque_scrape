from utils.scrape import scrape
from utils.excel import read_excel, find_excel, write_excel, write_not_found_excel_clone
from utils.functions import detect_all_duplicate_excel, detect_duplicate_excel
from time import sleep

def main():
  print("Olá! Bem-vindo ao sistema de automação de extração das planilhas de consulta de contracheque de pensionistas!\n")
  
  print("Aperte CTRL + C a qualquer momento para encerrar.\n")
  
  all_excel = []
  
  while(True):
    try_find_excel = find_excel("entrada")
    
    if len(try_find_excel) == 0:
      print("Nenhuma planilha encontrada!\n")
      print("Adicione as planilhas desejadas em '/planilhas/entrada' e tente novamente.")
      return
    else:
      print("Planilhas encontradas:")
      for i in range(len(try_find_excel)):
        print(f"{i + 1} - {try_find_excel[i]}")
    
      while True:
        print("\nDeseja adicionar todas as planilhas? (s/n):", end=" ")
        choice = input()
        
        if choice.lower() == 's':
          found_duplicates = detect_all_duplicate_excel(try_find_excel)
     
          if len(found_duplicates) != 0:
            print("\nOps, alguma(s) planilha(s) de entrada encontrada(s) já extraída(s) ou com o(s) mesmo(s) nome(s):")
      
            for i in range(len(found_duplicates)):
              print(f"* {found_duplicates[i]['in']} => {found_duplicates[i]['out']}")

            while True:
              print("\nDeseja adicionar a(s) planilha(s) mesmo assim? (s/n):", end=" ")
              override_choice = input()
              if override_choice.lower() == 's':
                all_excel = try_find_excel
                break
              elif override_choice.lower() == 'n':
                print("Remova a(s) planilha(s) de preferência nas pastas de entrada ou de saída e tente novamente!")
                return
              else:
                print("Opção inválida! Tente novamente.")
                continue
      
            break
          else:				
            all_excel = try_find_excel
            break
        elif choice.lower() == 'n':
          while True:
            print("Digite o número da planilha que deseja adicionar:", end=" ")
            choice = input()

            if not choice.isnumeric() or int(choice) < 0 or int(choice) > len(try_find_excel):
              print("Número da planilha inválido! Tente novamente.\n")
              continue
            
            found_duplicate = detect_duplicate_excel(try_find_excel[int(choice) - 1])
      
            if found_duplicate["detected"] == True:
              print(f"\nOps, a planilha '{found_duplicate['in']}' foi encontrada já extraída ou com o mesmo nome:")
              print(f"* {found_duplicate['in']} => {found_duplicate['out']}")
       
              while True:
                print(f"\nDeseja adicionar '{found_duplicate['in']}' mesmo assim? (s/n):", end=" ")
                override_choice = input()
                if override_choice.lower() == 's':
                  all_excel.append(try_find_excel[int(choice) - 1])
                  break
                elif override_choice.lower() == 'n':
                  print("Remova a planilha nas pastas de entrada ou de saída e tente novamente!")
                  return
                else:
                  print("Opção inválida! Tente novamente.")
                  continue

              break
            else:
              all_excel.append(try_find_excel[int(choice) - 1])
              break
          break
        else:
          print("Opção inválida! Tente novamente.")
      break
  
  print("\nDescanse e aguarde um pouco, estamos preparando a extração...\n")
  sleep(1)
  print("Atenção! Uma tela do seu navagador deverá abrir automaticamente.\n")
  sleep(1)
  print("A extração iniciará em 3 segundos...")
  sleep(1)
  print(3)
  sleep(1)
  print(2)
  sleep(1)
  print(1)
  
  sleep(1)
  print("\nAguarde, estamos realizando a extração dos dados...\n")
  sleep(1)
    
  # try:
  for i in range(len(all_excel)):
    df = read_excel(all_excel[i])
    scraped_data = scrape(df, all_excel[i])
    excel_done = write_excel(scraped_data[0], all_excel[i])
    print(f"Você pode encontrá-la em '{excel_done}'\n")
    
    excel_not_done = write_not_found_excel_clone(scraped_data[1], all_excel[i])
    
    if excel_not_done.strip() != '':
      print(f"Para os casos não encontrados, você pode encontrá-los em '{excel_not_done}'")
    
  sleep(2)
  print("\nExtração finalizada com sucesso! Obrigado por utilizar nosso sistema!\n")

try:
  main()
except Exception as error:
  print("\nOcorreu algum erro! Por favor tente novamente.")
  print(f"Erro: {error}")
finally:
  print("\nAperte qualquer botão para encerrar o processo.", end=" ")
  input()