import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import json
import requests  # pip install requests
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

#def load_lottieurl(url: str):
    #r = requests.get(url)
    #if r.status_code != 200:
        #return None
    #return r.json()

lottie_coding = load_lottiefile("lottiefiles/finance.json")  # replace link to local lottie file
#lottie_hello = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_M9p23l.json")

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="PNBP PPPK", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="Rekap PNBP September 2021.xlsx",
        engine="openpyxl",
        sheet_name="Rekapitulasi Denda PNBP",
        #skiprows=3,
        usecols="A:D",
        nrows=136,
    )
    df.dropna(inplace=True) 
    # Add 'hour' column to dataframe
    # df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

df1 = pd.read_excel(
    "Rekap PNBP September 2021.xlsx",
    sheet_name="Rekapitulasi Denda PNBP",
    #skiprows=3,
    usecols="A:F",
    nrows=136, 
)
#df1.dropna(inplace=True)
        
# ---- SIDEBAR ----
st.sidebar.header("PNBP Satker PPPK Tahun 2021")
pnbp = st.sidebar.selectbox(
    "Silahkan Pilih Jenis PNBP:",
    df["Jenis_PNBP"].unique()
)

#OAA = st.sidebar.multiselect(
    #"OAA:",
    #options=df["KAPA_atau_OAA"].unique(),
    #default=df["KAPA_atau_OAA"].unique(),
#)

#OAI = st.sidebar.multiselect(
    #"OAI:",
    #options=df["OAI"].unique(),
    #default=df["OAI"].unique()
#)

df_selection = df.query(
    "Jenis_PNBP == @pnbp"
)

# ---- MAINPAGE ----
#st.title(":bar_chart: PNBP Satker PPPK Tahun 2021")
#st.markdown("##")
#st.title = ':bar_chart: <p style="font-family:Courier; color:Blue; font-size: 20px;">PNBP Satker PPPK Tahun 2021</p>'

#st.markdown(st.title, unsafe_allow_html=True)

# TOP KPI's
total_denda = int(df_selection["Rupiah"].sum())
#average_rating = round(df_selection["Rating"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
rata_denda = int(df_selection["Rupiah"].mean())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Jumlah PNBP :")
    st.subheader(f"Rp {total_denda:,}")
with middle_column:
    #st.subheader('')
    st_lottie(
        lottie_coding,
        speed=3,
        reverse=False,
        loop=True,
        quality="low", # medium ; high
        renderer="svg", # canvas
        height=100,
        width=200,
        key=None,
    )
    #st.subheader("Average Rating:")
    #st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Rata-rata PNBP :")
    st.subheader(f"Rp {rata_denda:,}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Bulan"]).sum()[["Rupiah"]].sort_values(by="Rupiah")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x=sales_by_product_line.index,
    y="Rupiah",
    #orientation="h",
    title="<b>PNBP</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
    #width = 800,
    #height = 600,
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_product_sales)

# SALES BY KODE BILING [BAR CHART]
sales_by_kode_biling = (
    df_selection.groupby(by=["Bulan"]).sum()[["Satuan"]].sort_values(by="Satuan")
)
fig_kode_biling = px.bar(
    sales_by_kode_biling,
    x=sales_by_kode_biling.index,
    y="Satuan",
    #orientation="h",
    title="<b>Kode Biling</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_kode_biling),
    template="plotly_white",
    #width = 1000,
    #height = 600,
)
fig_kode_biling.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

#st.plotly_chart(fig_kode_biling)

# SALES BY HOUR [BAR CHART]
#sales_by_hour = df_selection.groupby(by=["Big_4"]).sum()[["Fee_Jasa"]]
#fig_hourly_sales = px.bar(
    #sales_by_hour,
    #x=sales_by_hour.index,
    #y="Fee_Jasa",
    #title="<b>Big 4</b>",
    #color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    #template="plotly_white",
#)
#fig_hourly_sales.update_layout(
    #xaxis=dict(tickmode="linear"),
    #plot_bgcolor="rgba(0,0,0,0)",
    #yaxis=(dict(showgrid=False)),
#)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_product_sales, use_container_width=True)
right_column.plotly_chart(fig_kode_biling, use_container_width=True)

st.markdown("""---""")

# PERHITUNGAN PERSENTASE PNBP
total_pnbp = int(df1["Rupiah"].sum())
target_pnbp = round(df1.iloc[0, 5])
x = total_pnbp / target_pnbp 
persen_pnbp = str(round(x*100)) + '%'

#target_pnbp = int(df1["Target"].sum())
#df1.dropna(inplace=True)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Target PNBP :")
    st.subheader(f"Rp {target_pnbp:,}")
with middle_column:
    st.subheader("Total PNBP :")
    st.subheader(f"Rp {total_pnbp:,}")
with right_column:
    st.subheader("Persentase PNBP :")
    st.subheader(f"Rp {persen_pnbp} :trophy:")   

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)