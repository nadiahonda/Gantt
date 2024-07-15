# Gantt
Create a Gantt Chart using data from an Excel file

## Functionality

- Select Excel file with input data.
- Choose colors per batch within a certain color pallete.
- Option to include or hide resource 'F&P' from Gantt chart (if existing in Excel file)
- Time unit definition to appear in labels (e.g. min, h)
- View Gantt chart
- Save Gantt chart as PNG with translucent background (standard white background options is also available within Matplotlib window)

## Requirements

- Python libraries: `matplotlib`, `pandas`, `openpyxl`
- Excel file (.xlsx) containing columns `Start`, `Duration`, `Batch`, `Resource 1`, `Resource 2`, `Resource 3`
