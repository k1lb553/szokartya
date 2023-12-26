import random, string
import datetime
import pandas as pd

""" ÖTLETEK:
Az egyes nem tudott szavakat külön adatbázis-táblába rakni:
    pl minden új szót amit egy 20 napos időintervallumon belül tanutam, rakja bele egy táblába
    Ennek a táblának legyen egy "lejárati dátuma", amikor ismételni kell őket.
    így nem kéne minden nap 3-féle paklit átnézni, azokat elég lenne hétvégente

"""




knowledge = {
    0: "Unassigned",
    1 : "(1day)Today",
    2 : "(2day)Next day",
    3: "(3day)Next next day",
    4: "One week",
    5: "One month",
    6: "3 months",
    7: "6 months",
    8: "Never repeat"
}

szo1 = {"hu":"alma",
       "en":"apple",
        "tudas_lvl":4,
        "T_datum":  0,
        "T_db":     0,
        "N_datum":  0,
        "N_db":     0,
        "ism_datum":0
}
szo2 = {"hu":"fal",
       "en":"wall",
        "tudas_lvl":0,
        "T_datum":  0,
        "T_db":     0,
        "N_datum":  0,
        "N_db":     0,
        "ism_datum":0
}
szolista = [szo1,szo2]

def test_me(szoArray, newwords=2):
    for a in range(newwords):
        if szo_aktualis(szoArray[a]):           #ha a szó a mai napra szól
            if checkszo(szoArray[a]):           #ha a szóra adott válasz helyes:
                print("A szót  tudtad")
                ismetlesi_datum(szoArray[a])    #ismétlési dátum kitalálása
                szoArray[a]["tudas_lvl"] +=1
                szoArray[a]["T_datum"] = curr_date
                szoArray[a]["T_db"] += 1


            else:
                print("A szót nem tudtad")
                ismetlesi_datum(szoArray[a])
                szoArray[a]["tudas_lvl"] -=1
                szoArray[a]["N_datum"] = curr_date
                szoArray[a]["N_db"] +=1


            print(szoArray[a])

def szo_aktualis(elem):
    if elem["T_datum"] == 0 or elem["ism_datum"] == curr_date: #az elem új szó, vagy mára jár le
        return True
    else:
        return False

def checkszo(lista_elem):
    user_valasz = input("Adja meg a "+lista_elem["hu"]+" szó angol jelentését: ")
    if user_valasz == lista_elem["en"]:
        return True
    else:
        return False


def ismetlesi_datum(elem): #a projet agya
    print(elem["tudas_lvl"])
    if elem["tudas_lvl"] <= 1:      #ma
        elem["ism_datum"]=curr_date

    if elem["tudas_lvl"] ==2:           #holnap
        enddate = curr_now + pd.DateOffset(days=1)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]

    if elem["tudas_lvl"] == 3:  # holnapután
        enddate = curr_now + pd.DateOffset(days=2)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]

    if elem["tudas_lvl"] == 4:  # 7 nap múlva
        enddate = curr_now + pd.DateOffset(days=7)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]

    if elem["tudas_lvl"] == 5:  # 31 nap múlva
        enddate = curr_now + pd.DateOffset(days=31)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]

    if elem["tudas_lvl"] == 6:  # 93 nap múlva
        enddate = curr_now + pd.DateOffset(days=93)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]

    if elem["tudas_lvl"] == 7:  # 186 nap múlva
        enddate = curr_now + pd.DateOffset(days=186)
        elem["ism_datum"] = [enddate.year, enddate.month, enddate.day]


kerdez = "y" or input("Akarsz kikérdezni? (y/n): ")
if kerdez=="y":
    test_me(szolista)



