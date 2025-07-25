import plotly.graph_objects as go

# Data prep

data = {
    "1960": [
        ("94910", "Religious organisations", 1922),
        ("84115", "Public Social Welfare Centers", 1066),
        ("84114", "Municipal government", 1058),
        ("68321", "Real estate syndicate activities", 1021),
        ("49410", "Road freight transport", 869),
    ],
    "1970": [
        ("1500", "Mining of metal ores", 8036),
        ("1300", "Extraction of metal ores", 3850),
        ("56301", "Cafés and bars", 1636),
        ("86220", "Medical specialists", 1519),
        ("49410", "Road freight transport", 1379),
    ],
    "1980": [
        ("1500", "Mining of metal ores", 7577),
        ("68201", "Residential property rental", 4443),
        ("68203", "Non-residential property rental", 3803),
        ("86220", "Medical specialists", 3788),
        ("1300", "Extraction of metal ores", 3465),
    ],
    "1990": [
        ("1500", "Mining of metal ores", 10259),
        ("70200", "Management consultancy", 7955),
        ("70220", "Other business consultancy", 7874),
        ("68201", "Residential property rental", 7270),
        ("43320", "Joinery", 6974),
    ],
    "2000": [
        ("70200", "Management consultancy", 21687),
        ("70220", "Other business consultancy", 21521),
        ("82990", "Other business services", 16535),
        ("43320", "Joinery", 14223),
        ("81300", "Landscaping services", 13137),
    ],
    "2010": [
        ("82990", "Other business services", 64370),
        ("70200", "Management consultancy", 49335),
        ("70220", "Other business consultancy", 49001),
        ("85599", "Other forms of education", 35846),
        ("81300", "Landscaping services", 28876),
    ],
    "2020": [
        ("82990", "Other business services", 133082),
        ("70200", "Management consultancy", 61463),
        ("85599", "Other forms of education", 56418),
        ("70220", "Other business consultancy", 54206),
        ("43211", "Electrical installation", 38272),
    ],
}

unique_sector_names = [
    "Religious organisations",
    "Public Social Welfare Centers",
    "Municipal government",
    "Real estate syndicate activities",
    "Road freight transport",
    "Mining of metal ores",
    "Extraction of metal ores",
    "Cafés and bars",
    "Medical specialists",
    "Residential property rental",
    "Non-residential property rental",
    "Management consultancy",
    "Other business consultancy",
    "Joinery",
    "Other business services",
    "Landscaping services",
    "Other forms of education",
    "Electrical installation",
]

colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
    "#aec7e8",
    "#ffbb78",
    "#98df8a",
    "#ff9896",
    "#c5b0d5",
    "#c49c94",
    "#f7b6d2",
    "#dbdb8d",
]
sector_color_map = dict(zip(unique_sector_names, colors))

decades_sorted = list(data.keys())

# list of counts per decade
sector_traces = {sector: [0] * len(decades_sorted) for sector in unique_sector_names}
for i, decade in enumerate(decades_sorted):
    for _, desc, count in data[decade]:
        if desc in sector_traces:
            sector_traces[desc][i] = count

# Chart

fig = go.Figure()

# Add one trace per sector
for sector, y_vals in sector_traces.items():
    text_labels = [f"{sector}: {val}" if val > 0 else "" for val in y_vals]
    fig.add_trace(
        go.Bar(
            name=sector,
            x=decades_sorted,
            y=y_vals,
            marker_color=sector_color_map[sector],
            text=text_labels,
            textposition="outside",
        )
    )
 
fig.update_layout(
    title="Top 5 Industries per Decade",
    xaxis_title="Decade",
    yaxis_title="Number of Companies",
    barmode="group",
    height=850,
    width=1700,
    legend_title="Sector",
    yaxis=dict(type="log"),
)

# Dropdown filters

buttons_decades = []
# Show all decades
buttons_decades.append(
    dict(
        label="All Decades",
        method="update",
        args=[
            {
                "x": [decades_sorted] * len(unique_sector_names),
                "y": [sector_traces[s] for s in unique_sector_names],
                "text": [
                    [f"{s}: {val}" if val > 0 else "" for val in sector_traces[s]]
                    for s in unique_sector_names
                ],
            },
            {
                "xaxis": {
                    "title": "Decade",
                    "categoryorder": "array",
                    "categoryarray": decades_sorted,
                },
                "yaxis": {"type": "log", "title": "Number of Companies (Log Scale)"},
            },
        ],
    )
)

# Buttons for individual decades
for idx, decade in enumerate(decades_sorted):
    x_vals = [
        [decade] if sector_traces[s][idx] > 0 else [] for s in unique_sector_names
    ]
    y_vals = [
        [sector_traces[s][idx]] if sector_traces[s][idx] > 0 else []
        for s in unique_sector_names
    ]
    text_vals = [
        [f"{s}: {sector_traces[s][idx]}"] if sector_traces[s][idx] > 0 else []
        for s in unique_sector_names
    ]

    buttons_decades.append(
        dict(
            label=decade,
            method="update",
            args=[
                {"x": x_vals, "y": y_vals, "text": text_vals},
                {
                    "xaxis": {"title": "Industry", "categoryorder": "trace"},
                    "yaxis": {
                        "type": "log",
                        "title": "Number of Companies (Log Scale)",
                    },
                },
            ],
        )
    )

fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=buttons_decades,
            x=1.15,
            y=1.15,
            xanchor="left",
            yanchor="top",
        )
    ]
)

# Export to HMTL
fig.write_html("Belgium_Industry_Trends.html")
print("Chart saved as Belgium_Industry_Trends.html")
