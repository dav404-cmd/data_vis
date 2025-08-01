# Job Data Visualization

A beginner-friendly project for cleaning and visualizing job data scraped from ZipRecruiter, using **Streamlit**.

---

### Disclaimer
> This is a learning project based on a small dataset.  
> ~53% of salary data was filled using **location-based averages** and global averages as fallback.  
> **Not suitable for real-world decision-making.**

---

### Dataset Features

- **Rows:** 1253
- **Columns:**  
  - `title`  
  - `company`  
  - `location`  
  - `job_type`  
  - `workplace_type`  
  - `days_ago`  *(post date)*
  - `salary_filled` *(USD/year)*

---

### Dashboard Features

- **Streamlit App** that lets users:
  - Select a location
  - View **histogram** and **box plot** of salary distribution
  - See top 10 highest-paying jobs in selected location

---

### 🚀 Try it Out
**Live Site:** [Click Here](https://jobdatavisualization.streamlit.app)  
*(If hosted on Streamlit Cloud)*

---

### Project Structure
```
data_vis/
├── data/
│ └── data_cleaned/
│ └── processed_data.csv
├── ui.py
├── README.md
└── .gitignore
```

**Author:** [dav404-cmd](https://github.com/dav404-cmd)