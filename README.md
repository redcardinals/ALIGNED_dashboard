# Assessing Legal and Institutional Governance Norms in European Democracies [ALIGNED] (v.1.0.2) 

This is the second version of a dashboard, now featuring a real dataset with improved dashboard functionalities and UI.

ALIGNED is still a personal project, has no conflict of interests and is entirely self-funded as the part of doctoral thesis in political sociology.

Since the first version (v1.0.1) was populated with fake data and disclaimers and was built for presentation purposes only, v1.0.1 is not accessibe to public anymore.

When updating the dataset with the newer reports or countries, previous dataset will become publicly available in full.

## Note on Methods
All coding done for v1.0.2 was manual, and it was conducted with the help of two coders. 
Training was provided. 
ICR scores were .81 between 3 coders, indicating high reliability of the method.

Read more at reformtrack.org

### Future coding
Future coding of EC reports may be done with the help of fine tuned LLMs.
NB: This could affect the values for sentences made in the v1.0.2.
In case of LLM coding, exhaustive inter-coder reliability tests will be done (human-machine, machine-machine (in case of testing various models))

## Note on WSA

World-system analysis lense to EU integrations of Serbia is a theoretical lense that I am applying in my PhD. 

However, the dashboard offers neutral readings as well: these are the scores that can be understood in numerous ways - WSA is interpretative, analytical layer that made sense to me.

## Future of ALIGNED

ALIGNED version 1 (with all iterations) will cover **only** EC reports pertaining to Serbia's EU integration path. 

ALIGNED version 2 will cover Serbia's and Montenegro's EC reports.

ALIGNED version 3 will cover all Western Balkan countries that are EU candidates.

ALIGNED version 4 will cover all EU candidates.

ALIGNED version 5 may include more document types.

## Using the dashboard
### What you need

Python 3.9 or later, and four packages: streamlit, pandas, plotly, and kaleido. Install them with pip before running anything.

### Running it locally

Put aligned_app.py and aligned_data.xlsx in the same folder. Then run streamlit run aligned_app.py in your terminal from that folder. The app will open in your browser automatically.

The app expects the dataset to be named exactly aligned_data.xlsx with a sheet called data. If either ever changes, there are two constants at the top of aligned_app.py — DATA_FILE and DATA_SHEET — where you update that.

### Sidebar controls

There are three control families and they are mutually exclusive — activating one clears the others.

Presentation presets are the quickest way in. Full Picture shows the overall average across all topics. Pol. vs Econ. splits by political versus economic criteria. Dom. vs Intl. splits by domestic reform versus international cooperation efforts. World-Systems applies the WSA lens (see below).

Customise lets you filter by dimension (Political / Economic), effort type (Domestic / International), or pick individual topics from the full list. These can be combined.

World-Systems Analysis is a separate theoretical lens. Primary interests of the EU core are Migration, Normalisation of Relations with Kosovo, External Relations, and Regional Cooperation. Secondary interests are Civil Society, Public Administration Reform, Freedom of Expression, and Fundamental Rights. This classification is part of ongoing doctoral research and should be read as interpretative, not definitive.

View at the bottom of the sidebar toggles between a line chart (yearly averages over time) and a bar chart (period averages ranked).

### How scores work

Each sentence is coded on a five-point scale: −1 (strongly negative), −0.5, 0 (neutral — excluded from this dataset), +0.5, and +1 (strongly positive). What you are looking at is how the European Commission frames reform progress in its reports, not an independent assessment of whether reforms actually happened.

### Exporting

Below the chart there are two download buttons — one for the chart as a PNG, one for the data behind the current view as a CSV. The PNG export requires kaleido to be installed.

### Citing this dataset
Karadžić, O. (2026). Assessing Legal and Institutional Governance Norms in European Democracies (ALIGNED) (Version 1.0.2) [Data set]. Reform Track. https://reformtrack.org

### Licences

I am publishing the code under MIT licence. Dataset, graphs produced by dashboard are licenced under CC BY 4.0 data license.
Please check LICENCE for details.

## Thank you for reading


© 2026 Reform Track – All rights reserved.
