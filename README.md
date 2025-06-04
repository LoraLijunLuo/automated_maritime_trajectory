# 🚢 Cruise Ship Trajectory Analysis with ArcGIS & Python

This project automates the geospatial processing of maritime trajectory data using Python and ArcGIS Pro. It was developed as part of a university course in 2022 and focuses on converting raw GPS logs from cruise ships into spatial trajectory lines enriched with distance, time, and speed attributes.

---

## 📌 Project Overview

- **Goal**: Transform raw timestamped GPS data into polylines representing ship trajectories.
- **Context**: More than 70 cruise ships operating in Northern Europe (North Sea, Baltic Sea, and English Channel).
- **Output**: Attribute-rich polyline layers ready for spatial analysis and visualization in ArcGIS Pro.

---

## 🛠️ Implementation Summary

- **Tools**: Python (`arcpy`), ArcGIS Pro (Custom Script Tool)
- **Input**: `.txt` files with ship ID, timestamp, and coordinates
- **Main Steps**:
  - Parse data and group by ship ID
  - Calculate:
    - Distance (via Haversine formula)
    - Time interval between observations
    - Speed (distance/time)
  - Filter abnormal speeds (> 60 km/h)
  - Generate polylines with segment attributes
  - Export results to a File Geodatabase

---

## 🗺️ Result Highlights

- Successfully processed and visualized ship trajectories with time-distance-speed attributes
- Color-coded route maps created in ArcGIS Pro for spatial interpretation
- Invalid trajectories (e.g. land-crossing, irregular speeds) excluded from results

![Project Workflow](documentation/fig1_workflow.png)
![Screenshot of Output Map](documentation/output_map_example.jpg)

---

## 📚 What I Learned

- Built a full geospatial data pipeline from raw data to final map layers
- Gained hands-on experience in:
  - Scripting with `arcpy` for spatial automation
  - Handling noisy, real-world movement data
  - Designing user-friendly tools in ArcGIS Pro
- Understood challenges in trajectory analysis:
  - Data inconsistencies
  - Performance optimization for batch processing
  - Integration between code and GIS platform

---

## 🔍 Future Improvements

- Add coastline validation to prevent land-crossing routes
- Enhance map layout and reporting for presentation-ready outputs

---

## 📝 Acknowledgements

This project was completed as part of the course *Programming, Customization and Automation in GIS* at the University of Copenhagen.

Developed by: **Lora Lijun Luo**  
Year: **2022**
