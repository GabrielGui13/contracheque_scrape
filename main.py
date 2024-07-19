from utils.scrape import scrape
from utils.excel import readExcel, findExcel, writeExcel

def main():
  print("Olá! Bem-vindo ao sistema de automação")
  
  all_excel = findExcel()
  
  print()
 
  for i in range(len(all_excel)):
    df = readExcel(all_excel[i])
    scraped_data = scrape(df, all_excel[i])
    writeExcel(scraped_data, all_excel[i])
 
main()
