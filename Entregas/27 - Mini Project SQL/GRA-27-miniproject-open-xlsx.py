'pip install pymysql'
'conda install -c conda-forge pymysql'
'pip install pandas openpyxl sqlalchemy pymysql'

import pandas as pd
from sqlalchemy import create_engine

'AQUÍ DEBAJO VUESTRO SITIO DONDE TENÉIS EL XLSX:'
file_path = '/Users/gabrielrogetdeaysa/Library/CloudStorage/GoogleDrive-rogetaysa@gmail.com/La meva unitat/IronhackGD/RepoIronhack/Entregas/27 - Mini Project SQL/SQL Test Data.xlsx'

'AQUÍ DEBAJO SUSTITUIR USUARI, CONTRASENYA, HOST Y NOM_BASE_DE_DADES'
"engine = create_engine('mysql+pymysql://usuari:contrasenya@host:3306/nom_base_de_dades')"
engine = create_engine('mysql+pymysql://root:ironhack@MacBook-Air-GRA.local:3306/ironhackgambling')

sheets = {
    'Account': 'Account',
    'Customer': 'Customer',
    'Betting': 'Betting',
    'Product': 'Product',
    'Student_School': 'Student_School',
    'Student': 'Student',
    'School': 'School'
}

for sheet_name, table_name in sheets.items():
    # Llegeix la pestanya de l'Excel en un DataFrame
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Carrega el DataFrame a la base de dades
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    
    print(f"Carregada la pestanya {sheet_name} a la taula {table_name}")

print("Totes les dades s'han carregat correctament a la base de dades.")
