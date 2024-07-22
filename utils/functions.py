from os import listdir
from utils.excel import find_excel
import pyautogui

def convert_month(month):
  monthDictionary = {
    "janeiro": 1,
    "fevereiro": 2,
    "março": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
  }
  
  return monthDictionary[month]

def detect_all_duplicate_excel(entry_excel):
  output_excel = find_excel("saida")
  detected_excel = []
 
  for i in range(len(entry_excel)):
    for j in range(len(output_excel)):
      if output_excel[j].endswith(entry_excel[i]):
        detected_excel.append({
          "in": entry_excel[i],
          "out": output_excel[j],
        })
        break
      
  return detected_excel

def detect_duplicate_excel(entry_excel):
  output_excel = listdir('./planilhas/saida')
  
  for i in range(len(output_excel)):
    if output_excel[i].endswith(entry_excel):
      return {
        "detected": True,
        "in": entry_excel,
        "out": output_excel[i],
      }
  
  return {
    "detected": False,
    "in": entry_excel,
    "out": None,
  }

def convert_seconds_to_formatted_time(sec):
  hours = sec // 3600
  minutes = (sec % 3600) // 60
  seconds = (sec % 3600) % 60
  
  return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def alert_box(title, message, button):
  pyautogui.alert(text=message, title=title, button=button)