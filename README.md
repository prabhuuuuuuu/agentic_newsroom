# BeatNet

### A CNN–BiLSTM Framework for Music Genre Classification

BeatNet is a deep learning pipeline for **automatic music genre classification** using audio feature extraction and hybrid neural architectures. The system combines **Convolutional Neural Networks (CNNs)** for spatial feature learning from spectrograms and **Bidirectional LSTMs (BiLSTM)** for modeling temporal dependencies in music signals.

The goal is to classify audio tracks into musical genres using representations such as **Mel-Spectrograms and MFCCs**, which capture the frequency structure of sound signals in a way that approximates human auditory perception.

---

# Overview

Music genre classification is a common task in **Music Information Retrieval (MIR)**. It enables automated tagging, recommendation systems, music discovery, and audio indexing.

Traditional audio classification approaches rely on handcrafted features, but deep learning models such as CNNs and RNNs can automatically learn hierarchical representations of audio signals. CNNs learn spatial patterns in spectrograms, while LSTM-based models capture temporal patterns across time frames. 

BeatNet combines both approaches to build a hybrid architecture that captures **both spectral and temporal information**.

---

# Model Architecture

BeatNet uses a **dual-branch architecture** for feature learning:

### 1. CNN Branch

Processes **Mel-Spectrogram images** extracted from audio signals.

Responsibilities:

* Capture frequency–time spatial patterns
* Learn local acoustic features
* Extract high-level representations of audio textures

### 2. BiLSTM Branch

Processes **MFCC sequences** extracted from the same audio track.

Responsibilities:

* Capture temporal dependencies
* Model sequential structure of sound
* Learn rhythm and evolving patterns in music

### Fusion Layer

Outputs from both branches are combined and passed through fully connected layers for final classification.

```
Audio File
     │
     ├── Mel Spectrogram → CNN → Feature Vector
     │
     └── MFCC Sequence → BiLSTM → Temporal Features
                    │
                Feature Fusion
                    │
            Fully Connected Layers
                    │
              Genre Prediction
```

---

# Dataset

The model is trained on the **GTZAN dataset**, a widely used benchmark dataset for music genre classification.

Dataset characteristics:

* 1000 audio tracks
* 30 seconds per track
* 10 genres

Genres include:

* Blues
* Classical
* Country
* Disco
* Hip-hop
* Jazz
* Metal
* Pop
* Reggae
* Rock

The GTZAN dataset is commonly used for benchmarking deep learning models for genre classification tasks. 

---

# Feature Extraction

BeatNet extracts two complementary feature representations:

### Mel Spectrogram

* Visual representation of audio
* Frequency scaled using the **mel scale**
* Suitable for CNN-based models

### MFCC (Mel-Frequency Cepstral Coefficients)

MFCCs represent the **short-term power spectrum of sound** and are widely used in speech and audio processing because they approximate human auditory perception.

Libraries used:

* **Librosa** for audio preprocessing
* **NumPy / SciPy** for signal processing

---

# Results

Training results achieved:

| Metric    | Value   |
| --------- | ------- |
| Accuracy  | ~92%    |
| Dataset   | GTZAN   |
| Framework | PyTorch |

The hybrid architecture improves classification accuracy compared to using a single model.

---

# Repository Structure

```
BeatNet
│
├── data/
│   └── dataset preprocessing scripts
│
├── models/
│   ├── cnn_model.py
│   ├── bilstm_model.py
│   └── beatnet_model.py
│
├── notebooks/
│   └── training and experimentation
│
├── utils/
│   └── feature extraction utilities
│
├── train.py
├── evaluate.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/prabhuuuuuuu/BeatNet.git
cd BeatNet
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Training

To train the model:

```bash
python train.py
```

Training pipeline includes:

1. Audio preprocessing
2. Feature extraction
3. Model training
4. Evaluation

---

# Inference

To predict the genre of an audio file:

```bash
python predict.py --audio path/to/audio.wav
```

Example output:

```
Predicted Genre: Rock
Confidence: 0.93
```

---

# Technologies Used

* Python
* PyTorch
* Librosa
* NumPy
* Matplotlib
* Scikit-learn

---

# Applications

BeatNet can be used in:

* Music recommendation systems
* Automatic music tagging
* Audio indexing
* Music streaming platforms
* Music information retrieval systems

---

# Future Improvements

Possible improvements include:

* Transformer-based audio models
* Larger datasets (FMA, Million Song Dataset)
* Self-supervised audio representation learning
* Real-time audio classification

---

# Author

**Pranav Prashant Shewale**
