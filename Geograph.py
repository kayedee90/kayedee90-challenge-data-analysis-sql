import pandas as pd
import plotly.express as px
import json

# ------------------------
# 1. Data Preparation
# ------------------------
data = [
    # 1960
    ("1960", "Antwerpen", 1577), ("1960", "West-Vlaanderen", 1290), ("1960", "Oost-Vlaanderen", 1052),
    ("1960", "Vlaams-Brabant", 1043), ("1960", "Henegouwen", 773), ("1960", "Liège", 721),
    ("1960", "Limburg", 547), ("1960", "Namur", 315), ("1960", "Luxembourg", 202), ("1960", "Brabant wallon", 188),
    ("1960", "Brussel", 2215),

    # 1970
    ("1970", "Antwerpen", 2252), ("1970", "West-Vlaanderen", 1802), ("1970", "Oost-Vlaanderen", 1778),
    ("1970", "Liège", 1398), ("1970", "Vlaams-Brabant", 1289), ("1970", "Henegouwen", 1096),
    ("1970", "Limburg", 841), ("1970", "Brabant wallon", 533), ("1970", "Namur", 470), ("1970", "Luxembourg", 313),
    ("1970", "Brussel", 2089),

    # 1980
    ("1980", "Antwerpen", 6600), ("1980", "West-Vlaanderen", 5252), ("1980", "Oost-Vlaanderen", 5128),
    ("1980", "Liège", 3780), ("1980", "Vlaams-Brabant", 3652), ("1980", "Henegouwen", 3251),
    ("1980", "Limburg", 2666), ("1980", "Brabant wallon", 1932), ("1980", "Namur", 1507), ("1980", "Luxembourg", 834),
    ("1980", "Brussel", 4151),

    # 1990
    ("1990", "Antwerpen", 14610), ("1990", "Oost-Vlaanderen", 10827), ("1990", "West-Vlaanderen", 9867),
    ("1990", "Vlaams-Brabant", 7864), ("1990", "Limburg", 6134), ("1990", "Liège", 5700),
    ("1990", "Henegouwen", 5600), ("1990", "Brabant wallon", 3912), ("1990", "Namur", 2869), ("1990", "Luxembourg", 1521),
    ("1990", "Brussel", 5774),

    # 2000
    ("2000", "Antwerpen", 29322), ("2000", "Oost-Vlaanderen", 21462), ("2000", "West-Vlaanderen", 19316),
    ("2000", "Vlaams-Brabant", 16242), ("2000", "Limburg", 12959), ("2000", "Henegouwen", 12757),
    ("2000", "Liège", 11187), ("2000", "Brabant wallon", 7733), ("2000", "Namur", 6129), ("2000", "Luxembourg", 3007),
    ("2000", "Brussel", 7809),

    # 2010
    ("2010", "Antwerpen", 52987), ("2010", "Oost-Vlaanderen", 37407), ("2010", "West-Vlaanderen", 32470),
    ("2010", "Vlaams-Brabant", 29352), ("2010", "Limburg", 22528), ("2010", "Liège", 18987),
    ("2010", "Henegouwen", 18451), ("2010", "Brabant wallon", 13206), ("2010", "Namur", 9086), ("2010", "Luxembourg", 3647),
    ("2010", "Brussel", 12469),

    # 2020
    ("2020", "Antwerpen", 58441), ("2020", "Oost-Vlaanderen", 44208), ("2020", "Vlaams-Brabant", 41214),
    ("2020", "West-Vlaanderen", 36589), ("2020", "Limburg", 24810), ("2020", "Liège", 21288),
    ("2020", "Henegouwen", 18952), ("2020", "Brabant wallon", 12075), ("2020", "Namur", 9512), ("2020", "Luxembourg", 3906),
    ("2020", "Brussel", 11545)
]


df = pd.DataFrame(data, columns=["decade", "province", "count"])

# ------------------------
# 2. Mapping NL -> GeoJSON Names
# ------------------------
province_mapping = {
    "Antwerpen": "Antwerp",
    "Oost-Vlaanderen": "East Flanders",
    "West-Vlaanderen": "West Flanders",
    "Vlaams-Brabant": "Flemish Brabant",
    "Henegouwen": "Hainaut",
    "Brabant wallon": "Walloon Brabant",
    "Liège": "Liege",
    "Namur": "Namur",
    "Luxembourg": "Luxembourg",
    "Limburg": "Limburg",
    "Brussel": "Brussels"
}
df["geo_name"] = df["province"].map(province_mapping)

# ------------------------
# 3. Load GeoJSON (be.json)
# ------------------------
with open("be.json", "r", encoding="utf-8") as f:
    belgium_geojson = json.load(f)

# ------------------------
# 4. Create Choropleth with Dropdown
# ------------------------
decades = sorted(df["decade"].unique())

fig = px.choropleth(
    df[df["decade"] == decades[0]],
    geojson=belgium_geojson,
    locations="geo_name",
    featureidkey="properties.name",
    color="count",
    color_continuous_scale="Reds",
    hover_name="province",  # NL naam
    hover_data={"count": True},
    title="Company Distribution per Province in Belgium"
)

# Dropdown menu
buttons = []
for decade in decades:
    decade_data = df[df["decade"] == decade]
    buttons.append(dict(
        method="restyle",
        label=decade,
        args=[{"z": [decade_data["count"]],
               "locations": [decade_data["geo_name"]]}]
    ))

fig.update_layout(
    updatemenus=[dict(
        buttons=buttons,
        direction="down",
        showactive=True,
        x=0.1,
        y=1.1,
        xanchor="left",
        yanchor="top"
    )]
)

fig.update_geos(fitbounds="locations", visible=False)

# Save HTML
fig.write_html("Belgium_Province_Map_Dropdown.html")
print("Map saved as Belgium_Province_Map_Dropdown.html")
