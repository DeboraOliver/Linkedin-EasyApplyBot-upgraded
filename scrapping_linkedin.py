'''
o objetivo desse programa é completar a falta de informação de um outro arquivo
'''

import pandas as pd
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# REMOVER NaN

df = pd.read_csv("joblist.csv")
#df = pd.read_csv("joblist.csv", usecols=[1])
jobID_raw = df['1596074050'].dropna()
print(jobID_raw)
# LISTAR APENAS A COLUNA DE IDs

jobID = jobID_raw.tolist()
#print(jobID)

# csv
filename = "empregos.csv"
f = open(filename, "w")

headers = "id,vaga,empresa,regiao,data,link\n"  # csv sao definidos pelo \n
f.write(headers)

# GERAR UM LOOP

for id in jobID:
    try:
        ID_jobs = str(int(id))
        print(ID_jobs)

        url = "https://www.linkedin.com/jobs/view/" + ID_jobs
        print(url)

        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()  # fecha o pedido anterior qndo eu terminar

        # html parsing
        page_soup = soup(page_html, "html.parser")
        # print(page_soup)

        # VAGA
        vaga_raw = page_soup.find("h1", {"class": "topcard__title"})
        vaga = vaga_raw.text.strip()

        # EMPRESA
        empresa_raw = page_soup.find("a", {"class": "topcard__org-name-link topcard__flavor--black-link"})
        empresa = empresa_raw.text.strip()

        # Região
        regiao_raw = page_soup.find("span", {"class": "topcard__flavor topcard__flavor--bullet"})
        regiao = regiao_raw.text.strip()

        # Concorrencia
        # candidates_raw = page_soup.find("span", {"class": "topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption"})
        # candidates = candidates_raw.text.strip()

        # Data que postaram o job
        data_raw = page_soup.find("span", {"class": "topcard__flavor--metadata posted-time-ago__text"})
        data = data_raw.text.strip()

        print("job_id: " + str(ID_jobs))
        print("Vaga: " + vaga)
        print("Empresa: " + empresa)
        print("Região: " + regiao)
        print("Data da postagem: " + data)
        # print("Concorrência: " + candidates)
        print("Link: " + url)

        f.write(ID_jobs + "," + vaga(",", "|") + "," + empresa.replace(",", "|") + "," + regiao.replace(",","|") + "," + data + "," + url + "\n")
        #f.close()
    # f.write(ID_jobs + "," + vaga + "," + empresa.replace(",", "|") + "," + regiao.replace(",","|") + "," + data + "," + candidates + "," + url + "\n")
    except:#ignorandoos erros
        pass

f.close()
