# 🕵️ AI-Based Deepfake Face Detector

![Image Description](UI%20Images/Project_Banner.png)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![NumPy](https://img.shields.io/badge/NumPy-Scientific%20Computing-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Data%20Visualization-11557C)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Deepfake%20Detection-red)
![Deep Learning](https://img.shields.io/badge/Deep%20Learning-Neural%20Networks-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-success)

A deep learning-powered system that detects whether a facial image is **Real** or **Deepfake**. The application leverages deep learning techniques to identify and classify authentic images from StyleGAN-generated fake images while providing reliable predictions with confidence scores.

---

## 📌 Overview

With the rapid advancement of Generative AI, deepfakes have become increasingly realistic and difficult to identify manually. This project aims to combat misinformation and digital manipulation by providing an automated deepfake face detection solution.

The system processes facial images, extracts meaningful features using deep learning techniques, and classifies them as either **Authentic** or **AI-Generated**.

---

## ✨ Features

- AI-powered deepfake face detection
- Detects synthetic facial images
- Real-time prediction with confidence scores
- Automatic image preprocessing and normalization
- Deep learning-based classification model
- User-friendly web interface
- High accuracy and efficient inference
- Supports image upload for detection
- Visual prediction results for better interpretation

---

## 🖼️ Interface 

![Image Description](UI%20Images/Home_img.png)

*Figure 1: Home page of the Deepfake Face Detector application.*

![Image Description](UI%20Images/About_img.png)

*Figure 2: About page of the Deepfake Face Detector application.*

![Image Description](UI%20Images/How_it_works_img.png)

*Figure 3: How it works page of the Deepfake Face Detector application.*

---

## 📂 Dataset

This model is trained using the publicly available Kaggle dataset **140k Real and Fake Faces**.

### Dataset Details

- **Dataset Name:** 140k Real and Fake Faces
- **Dataset Link:** https://www.kaggle.com/datasets/xhlulu/140k-real-and-fake-faces
- **Total Images:** 140,000
- **Training Images:** 100,000
- **Validation Images:** 20,000
- **Testing Images:** 20,000

### Dataset Structure

```text
dataset/
├── train/
│   ├── real/
│   └── fake/
├── validation/
│   ├── real/
│   └── fake/
└── test/
    ├── real/
    └── fake/
```

---

## 🧠 Model Architecture & Workflow

**Model Used:** Vision Transformer (ViT)

![Image Description](UI%20Images/Project_Workflow.png)

*Figure 4: Project Workflow for the Deepfake Face Detector Application.*

---

## 📁 Project Structure

```text
AI-Based-Deepfake-Face-Detection/
│
├── app.py
├── model_utils.py
├── pages_content.py
├── style.py
│
├── deepfake-face-detector-model-training-notebook.ipynb
│
├── model/
│   └── deepfake_model.pth
│
├── UI Images/
│   ├── About_img.png
│   ├── How_it_works_img.png
│   └── Home_img.png
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

### Artificial Intelligence & Deep Learning
- Python
- PyTorch
- TorchVision
- TIMM (Vision Transformer Models)
- Scikit-learn

### Image Processing
- Pillow (PIL)

### Data Visualization
- Matplotlib
- Plotly

### Web App Development & Deployment
- Streamlit
- Streamlit Community Cloud

### Development & Research Tools
- Jupyter Notebook

### Machine Learning & Computer Vision Concepts
- Deepfake Detection
- Image Classification
- Vision Transformers (ViT)
- Transfer Learning

---

## 📊 Evaluation Metrics

- Accuracy
- Precision
- Recall
- F1-Score
- Confusion Matrix

---

## ⚡ Performance

- Model Type: Deep Learning Classifier
- Binary Classification: Real vs Fake
- Optimized for image-based face detection
- Fast inference and prediction

---

## 🚀 Future Enhancements

- Real-time webcam deepfake detection
- Video deepfake analysis
- Mobile application development
- Explainable AI (XAI) integration
- Cloud deployment using AWS, Azure, or GCP
- Multi-face detection support
- REST API integration
- Continuous learning from new datasets

---

## 🙏 Acknowledgements

Special thanks to:

- Kaggle dataset provider
- Open-source community
- Researchers working on AI-generated content detection
- TensorFlow and OpenCV contributors

---

## 📧 Contact

**Author:** Bhuvnesh

**GitHub:** https://github.com/Bhuvnesh-007

---

### ⭐ If you found this project useful, please consider giving it a star on GitHub!
