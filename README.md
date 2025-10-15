# 📱 Human Activity Recognition using Smartphone Accelerometer Data  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-yellow)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

---

## 🧭 Project Overview
This project implements **Human Activity Recognition (HAR)** using **smartphone accelerometer data**.  
The goal is to automatically detect and classify human physical activities such as:
- 🚶 Walking  
- 🧗 Walking Upstairs  
- 🧎 Walking Downstairs  
- 🪑 Sitting  
- 🧍 Standing  
- 🛌 Laying  

Using the **UCI HAR Dataset**, the project demonstrates how **machine learning** can process time-series sensor data for practical applications in healthcare, rehabilitation, and fitness monitoring.

---

## 📊 Dataset Description
**Dataset:** [UCI HAR Dataset](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)  
- **Subjects:** 30 volunteers (aged 19–48)  
- **Device:** Samsung Galaxy S II worn on the waist  
- **Sensors:** 3-axial accelerometer & gyroscope  
- **Sampling rate:** 50 Hz  
- **Total samples:** 10,299  
- **Features:** 561 (time & frequency domain)  
- **Activities:** Walking, Walking Upstairs, Walking Downstairs, Sitting, Standing, Laying  

---

## 🧩 Methodology

### **1. Data Loading**
- The dataset is read from text files (`features.txt`, `X_train.txt`, `y_train.txt`, etc.).
- Merged and labeled into a single DataFrame using Pandas.

### **2. Data Preprocessing**
- Normalized sensor readings.  
- Split into **training (70%)** and **testing (30%)** sets.  
- Ensured reproducibility with fixed random seeds.

### **3. Model Design**
- **Algorithm:** Random Forest Classifier  
- **Training samples:** 7,352 × 561 features  
- **Testing samples:** 2,947 × 561 features  
- **Libraries Used:** `scikit-learn`, `numpy`, `pandas`, `matplotlib`, `seaborn`

### **4. Evaluation Metrics**
- Accuracy  
- Precision, Recall, F1-Score  
- Confusion Matrix for visual evaluation  

---

## 📈 Results

| Metric | Score |
|--------|--------|
| **Accuracy** | 0.9257 (92.57%) |
| **Precision (macro avg)** | 0.93 |
| **Recall (macro avg)** | 0.92 |
| **F1-score (macro avg)** | 0.92 |

✅ The model achieved **excellent classification accuracy**, particularly for “Laying” and “Standing” activities.  

**Confusion Matrix & Graphs** are available in the `results/` directory.

---

## 🧠 Technologies Used
- **Programming Language:** Python  
- **IDE:** Anaconda / Jupyter Notebook  
- **Core Libraries:**  
  - NumPy  
  - Pandas  
  - Matplotlib  
  - Seaborn  
  - Scikit-learn  

---

## 🚀 Future Enhancements
- Integrate **gyroscope** and **magnetometer** data.  
- Develop **real-time mobile classification** for edge devices.  
- Explore **deep learning models** (CNNs, RNNs).  
- Enable **user-specific model personalization**.  
- Implement **on-device privacy-preserving inference**.

---

## 👨‍💻 Author
**Hassan Shahid**  
MS Data Science | NUST MISIS  
📍 Moscow, Russia  
📧 Email: [shahid.nust.misis.ru@gmail.com]  
🔗 GitHub: [https://github.com/Markhor072](https://github.com/Markhor072)

---

## 🪪 License
This project is licensed under the **MIT License** — you are free to use, modify, and distribute it for research and education.

---

### ⭐ If you find this project helpful, please star the repository!
