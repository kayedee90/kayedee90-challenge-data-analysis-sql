import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import math
import os


# Provincial growth data (1960–2020)
data = [
    ("1960", "Antwerp", 1577), ("1960", "West Flanders", 1290), ("1960", "East Flanders", 1052),
    ("1960", "Flemish Brabant", 1043), ("1960", "Hainaut", 773), ("1960", "Liège", 721),
    ("1960", "Limburg", 547), ("1960", "Namur", 315), ("1960", "Luxembourg", 202), ("1960", "Walloon Brabant", 188),
    ("1960", "Brussels", 2215),

    ("1970", "Antwerp", 2252), ("1970", "West Flanders", 1802), ("1970", "East Flanders", 1778),
    ("1970", "Liège", 1398), ("1970", "Flemish Brabant", 1289), ("1970", "Hainaut", 1096),
    ("1970", "Limburg", 841), ("1970", "Walloon Brabant", 533), ("1970", "Namur", 470), ("1970", "Luxembourg", 313),
    ("1970", "Brussels", 2089),

    ("1980", "Antwerp", 6600), ("1980", "West Flanders", 5252), ("1980", "East Flanders", 5128),
    ("1980", "Liège", 3780), ("1980", "Flemish Brabant", 3652), ("1980", "Hainaut", 3251),
    ("1980", "Limburg", 2666), ("1980", "Walloon Brabant", 1932), ("1980", "Namur", 1507), ("1980", "Luxembourg", 834),
    ("1980", "Brussels", 4151),

    ("1990", "Antwerp", 14610), ("1990", "East Flanders", 10827), ("1990", "West Flanders", 9867),
    ("1990", "Flemish Brabant", 7864), ("1990", "Limburg", 6134), ("1990", "Liège", 5700),
    ("1990", "Hainaut", 5600), ("1990", "Walloon Brabant", 3912), ("1990", "Namur", 2869), ("1990", "Luxembourg", 1521),
    ("1990", "Brussels", 5774),

    ("2000", "Antwerp", 29322), ("2000", "East Flanders", 21462), ("2000", "West Flanders", 19316),
    ("2000", "Flemish Brabant", 16242), ("2000", "Limburg", 12959), ("2000", "Hainaut", 12757),
    ("2000", "Liège", 11187), ("2000", "Walloon Brabant", 7733), ("2000", "Namur", 6129), ("2000", "Luxembourg", 3007),
    ("2000", "Brussels", 7809),

    ("2010", "Antwerp", 52987), ("2010", "East Flanders", 37407), ("2010", "West Flanders", 32470),
    ("2010", "Flemish Brabant", 29352), ("2010", "Limburg", 22528), ("2010", "Liège", 18987),
    ("2010", "Hainaut", 18451), ("2010", "Walloon Brabant", 13206), ("2010", "Namur", 9086), ("2010", "Luxembourg", 3647),
    ("2010", "Brussels", 12469),

    ("2020", "Antwerp", 58441), ("2020", "East Flanders", 44208), ("2020", "Flemish Brabant", 41214),
    ("2020", "West Flanders", 36589), ("2020", "Limburg", 24810), ("2020", "Liège", 21288),
    ("2020", "Hainaut", 18952), ("2020", "Walloon Brabant", 12075), ("2020", "Namur", 9512), ("2020", "Luxembourg", 3906),
    ("2020", "Brussels", 11545),
]

df = pd.DataFrame(data, columns=["Decade", "Province", "Count"])

# Color coding
region_map = {
    "Antwerp": "Flanders", "East Flanders": "Flanders", "West Flanders": "Flanders",
    "Flemish Brabant": "Flanders", "Limburg": "Flanders",
    "Liège": "Wallonia", "Hainaut": "Wallonia", "Namur": "Wallonia",
    "Luxembourg": "Wallonia", "Walloon Brabant": "Wallonia",
    "Brussels": "Brussels"
}
df["Region"] = df["Province"].map(region_map)

# Calculate CAGR (1960 to 2020)
base_year = df[df["Decade"] == "1960"].set_index("Province")["Count"]
final_year = df[df["Decade"] == "2020"].set_index("Province")["Count"]
cagr_data = []
for province in base_year.index:
    start = base_year[province]
    end = final_year[province]
    cagr = ((end / start) ** (1 / 60)) - 1
    cagr_data.append((province, round(cagr * 100, 2)))
cagr_df = pd.DataFrame(cagr_data, columns=["Province", "CAGR"])

# Prepare output folder
os.makedirs("exports", exist_ok=True)


# CHARTS


# Log-scale line chart (Growth over time)
fig1 = px.line(df, x="Decade", y="Count", color="Province", log_y=True,
               title="Growth of Companies by Province (Log Scale)",
               markers=True)
fig1.update_layout(yaxis_title="Company Count (Log Scale)")
fig1.write_image("exports/01_growth_log.png")

# Grouped bar chart (Top provinces per decade)
fig2 = px.bar(df, x="Count", y="Province", color="Region", facet_col="Decade",
              facet_col_wrap=3, orientation="h",
              title="Top Provinces per Decade")
fig2.update_layout(showlegend=True)
fig2.write_image("exports/02_top_provinces.png")

# Stacked area chart (Regional share)
regional_share = df.groupby(["Decade", "Region"])["Count"].sum().reset_index()
total_by_decade = regional_share.groupby("Decade")["Count"].transform("sum")
regional_share["Share"] = regional_share["Count"] / total_by_decade * 100
fig3 = px.area(regional_share, x="Decade", y="Share", color="Region",
               title="Regional Share of Total Companies Over Time")
fig3.update_yaxes(title="Share (%)")
fig3.write_image("exports/03_regional_share.png")

# Brussels paradox (Count vs Density)
province_area = {
    "Antwerp": 2867, "East Flanders": 3007, "West Flanders": 3144,
    "Flemish Brabant": 2106, "Limburg": 2422,
    "Liège": 3862, "Hainaut": 3786, "Namur": 3666,
    "Luxembourg": 4440, "Walloon Brabant": 1091,
    "Brussels": 162
}
density_data = []
for province in final_year.index:
    density = final_year[province] / province_area[province]
    density_data.append((province, final_year[province], density))
density_df = pd.DataFrame(density_data, columns=["Province", "Count_2020", "Density"])

fig4 = go.Figure()
fig4.add_trace(go.Bar(x=density_df["Province"], y=density_df["Count_2020"], name="Company Count"))
fig4.add_trace(go.Scatter(x=density_df["Province"], y=density_df["Density"], mode="lines+markers", name="Density (per km²)", yaxis="y2"))
fig4.update_layout(
    title="Brussels Paradox: Count vs Density",
    yaxis=dict(title="Company Count"),
    yaxis2=dict(title="Density (companies/km²)", overlaying="y", side="right")
)
fig4.write_image("exports/04_brussels_paradox.png")

# CAGR by province
fig5 = px.bar(cagr_df.sort_values("CAGR", ascending=True),
              x="CAGR", y="Province", orientation="h",
              title="CAGR by Province (1960–2020)",
              text="CAGR")
fig5.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
fig5.write_image("exports/05_cagr.png")

# Projection line chart
projection_years = [2020, 2030, 2040]
provinces = ["Antwerp", "East Flanders", "Flemish Brabant"]
proj_data = []
for province in provinces:
    start_value = final_year[province]
    cagr = cagr_df[cagr_df["Province"] == province]["CAGR"].values[0] / 100
    for year in projection_years:
        years_since_2020 = year - 2020
        projected_value = start_value * ((1 + cagr) ** years_since_2020)
        proj_data.append((year, province, projected_value))
proj_df = pd.DataFrame(proj_data, columns=["Year", "Province", "Projected Count"])
fig6 = px.line(proj_df, x="Year", y="Projected Count", color="Province",
               markers=True, title="Future Outlook (Projection to 2040)")
fig6.update_layout(yaxis_title="Company Count")
fig6.write_image("exports/06_projection.png")


# Simple combined dashboard with all charts as separate tabs (export as HTML)

from plotly.subplots import make_subplots

figures = {
    "Growth Over Time (Log Scale)": fig1,
    "Top Provinces per Decade": fig2,
    "Regional Share": fig3,
    "Brussels Paradox": fig4,
    "CAGR by Province": fig5,
    "Projection to 2040": fig6
}

# Save
with open("exports/dashboard.html", "w") as f:
    for title, fig in figures.items():
        f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
