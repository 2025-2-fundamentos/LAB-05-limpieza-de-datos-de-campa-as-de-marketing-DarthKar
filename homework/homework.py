"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.
    
     

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months
    """
    
    import os
    import zipfile
    import pandas as pd

    carpeta = "files\input"
    dataframes = []

    for archivo in os.listdir(carpeta):
        if archivo.endswith(".zip"):
            ruta_zip = os.path.join(carpeta, archivo)
            with zipfile.ZipFile(ruta_zip, 'r') as z:
                for nombre in z.namelist():
                    if nombre.endswith(".csv"):
                        with z.open(nombre) as f:
                            df = pd.read_csv(f)
                            df["origen_zip"] = archivo  
                            dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)

    client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    client['credit_default'] = client['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
    client['mortgage'] = client['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
    client['education'] = client['education'].str.replace('.', '_')
    client['education'] = client['education'].replace('unknown', pd.NA)
    client['job'] = client['job'].str.replace('.', '')
    client['job'] = client['job'].str.replace('-', '_')

    campaign = df[['client_id', 'number_contacts','contact_duration', 'previous_campaign_contacts',
     'previous_outcome', 'campaign_outcome']].copy()
    campaign['previous_outcome'] = campaign['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
    campaign['campaign_outcome'] = campaign['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
    campaign['last_contact_date'] = pd.to_datetime(
    '2022-' + df['month'].astype(str) + '-' + df['day'].astype(str),
    format='%Y-%b-%d',
    errors='coerce'
    )
    economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    
    ruta = "files/output/"
    os.makedirs(ruta, exist_ok=True)
    campaign.to_csv(f'{ruta}campaign.csv', index=False)
    economics.to_csv(f'{ruta}economics.csv', index=False)
    client.to_csv(f'{ruta}client.csv', index = False)


if __name__ == "__main__":
    clean_campaign_data()
