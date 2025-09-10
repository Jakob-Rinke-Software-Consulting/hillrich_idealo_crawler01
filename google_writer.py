import pygsheets
import os
import time
import threading


TABLEHEAD = ["Name", "Buy Price Brutto", "Current Amazon Price Brutto", "30 day Average", "90 day Average",
              "BSR", "Rating Count", "Amazon Link", "Idealo Link", "Marge", "Marge %", "Marge 90", "Marge 30",
              "Kategorie", "Buybox", "Anzahl Verkäufe"
              ]

#authorization
try:
    gc = pygsheets.authorize(service_file=os.getcwd()+'/settings/client_secret.json')
    try:
        sh= gc.open_by_url("https://docs.google.com/spreadsheets/d/17rnjj27F7vYxbNSo6-QSw8dPy_q5U7F9c0LwDTOSQ-s/edit?usp=sharing")
        print("Spreadsheet opened successfully.")
    except:
        print("Spreadsheet not found, creating a new one.")
        sh = gc.create('Idealo_Scraper')
        sh.share('htmljakob@gmail.com', role='writer')
except:
    gc = None
    print("Authorization failed.")

sheet_lock = threading.Lock()

def add_to_sheet(data_col):
    if gc is None:
        return
    date = time.strftime("%d-%m-%Y")
    with sheet_lock:
        try:
            wks = sh.worksheet_by_title(date)
        except:
            wks = sh.add_worksheet(date)
            try:
                wks.append_table(TABLEHEAD)
            except:
                pass
        try:
            wks.append_table(data_col)
        except:
            pass
    

if __name__ == "__main__":
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
