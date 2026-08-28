# MediaPipe: Comprehensive Guide

## Table of Contents
1. [What is MediaPipe?](#what-is-mediapipe)
2. [Core Architecture & Concepts](#core-architecture--concepts)
3. [MediaPipe Tasks API vs. Legacy Framework](#mediapipe-tasks-api-vs-legacy-framework)
4. [Available Solutions](#available-solutions)
5. [Setup & Installation](#setup--installation)
6. [Basic Implementation Example (Python)](#basic-implementation-example-python)
7. [Constraints & Limitations](#constraints--limitations)
8. [Best Practices](#best-practices)

---

## 1. What is MediaPipe?

**MediaPipe** is an open-source, cross-platform framework developed by Google for building applied machine learning (ML) pipelines. It is specifically designed to handle multimodal data—including video, audio, time-series data, and text. 

MediaPipe allows developers to build complex, real-time perception applications with minimal latency and high efficiency, making it ideal for edge devices, mobile phones, web browsers, and desktop applications.

### Key Features:
- **Cross-Platform:** Runs on Android, iOS, Desktop (C++/Python), and Web (JavaScript/WebAssembly).
- **Real-Time Performance:** Optimized for low latency, often running complex ML models at 30+ FPS on mobile CPUs/GPUs.
- **Pre-trained Models:** Comes with highly optimized, pre-trained models for common tasks (e.g., face detection, hand tracking, pose estimation).
- **Customizability:** Allows fine-tuning of models using MediaPipe Model Maker and integration of custom TensorFlow Lite models.

---

## 2. Core Architecture & Concepts

At its core, MediaPipe operates as a directed acyclic graph (DAG) where nodes represent processing steps and edges represent data flow.

### Terminology:
- **Graph:** The overall pipeline structure. It consists of interconnected nodes.
- **Calculator:** A single node within the graph. It performs a specific operation (e.g., image resizing, running a TFLite model, drawing overlays). Calculators can be written in C++.
- **Packet:** The basic unit of data in MediaPipe. A packet consists of a numeric timestamp and a shared pointer to an immutable payload (e.g., an image frame or an array of landmarks).
- **Stream:** A sequence of Packets whose timestamps are monotonically increasing. Streams connect Calculators.
- **Side Packet:** Similar to a regular packet, but it remains constant throughout the graph execution (e.g., a static configuration flag or file path).

---

## 3. MediaPipe Tasks API vs. Legacy Framework

Google recently introduced the **MediaPipe Tasks API** to simplify development, distinguishing it from the older, more complex graph-based approach.

### Legacy Framework (Calculators & Graphs)
- Required defining protobuf (`.pbtxt`) graph configurations.
- Steep learning curve.
- High customizability—you could inject custom C++ calculators into the pipeline.
- Still necessary for highly custom, non-standard pipelines.

### MediaPipe Tasks API (Modern Approach)
- Object-oriented, easy-to-use API.
- Available for Vision, Audio, and Text.
- Eliminates the need to write complex graph definitions for standard tasks.
- Supports **Model Maker** (for fine-tuning models) and **MediaPipe Studio** (for web-based visual prototyping).
- **Recommendation:** Use the Tasks API for new projects unless you have highly specialized requirements that necessitate the legacy framework.

---

## 4. Available Solutions

MediaPipe provides out-of-the-box solutions organized into three main categories:

### Vision
- **Object Detection:** Detects multiple classes of objects.
- **Image Classification:** Categorizes the dominant object in an image.
- **Image Segmentation:** Separates objects from the background (e.g., background blur).
- **Interactive Image Segmentation:** Segments an object based on user-selected coordinates.
- **Face Detection:** Bounding box detection for faces.
- **Face Landmarker:** Detects 478 3D facial landmarks (useful for AR filters and emotion recognition).
- **Hand Landmarker:** Detects 21 3D landmarks per hand, handles multiple hands, and recognizes basic gestures.
- **Pose Landmarker:** Tracks 33 3D body landmarks (useful for fitness tracking).

### Audio
- **Audio Classification:** Categorizes audio into predefined classes.

### Text
- **Text Classification:** Sentiment analysis and categorization.
- **Language Detector:** Identifies the language of a given text.
- **Text Embedder:** Generates vector representations of text for semantic search.

---

## 5. Setup & Installation

The easiest way to get started is with Python. Below are instructions for various platforms.

### Python (Windows, macOS, Linux)
**Prerequisites:** Python 3.8 to 3.11.

```bash
# Create a virtual environment (recommended)
python -m venv mediapipe-env

# Activate the environment
# Windows:
mediapipe-env\Scripts\activate
# macOS/Linux:
source mediapipe-env/bin/activate

# Install MediaPipe Tasks API and OpenCV
pip install mediapipe opencv-python
```

### Web (JavaScript/TypeScript)
You can include MediaPipe directly in your frontend via CDN or NPM.

```bash
npm install @mediapipe/tasks-vision
```

### Android (Java/Kotlin)
Add the dependency to your `build.gradle`:

```gradle
dependencies {
    implementation 'com.google.mediapipe:tasks-vision:latest.release'
}
```

### C++
Setting up C++ MediaPipe requires Bazel. It is notoriously complex on Windows. It is highly recommended to use Linux or WSL2 for C++ MediaPipe development.

---

## 6. Basic Implementation Example (Python)

Here is a modern example using the **MediaPipe Tasks API** to perform Hand Landmarking on a webcam feed.

> **Note:** You must download the pre-trained model bundle first.
> Download `hand_landmarker.task` from the [MediaPipe Developer site](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#models).

```python
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 1. Configuration
model_path = 'hand_landmarker.task' # Path to your downloaded model
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a hand landmarker instance with the live stream mode:
options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=lambda result, output_image, timestamp_ms: print(f"Detected hands: {len(result.hand_landmarks)}")
)

with HandLandmarker.create_from_options(options) as landmarker:
    # 2. Capture Video
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # 3. Preprocess the image
        # MediaPipe expects RGB format, OpenCV uses BGR
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # 4. Run Inference
        # Get timestamp in milliseconds
        frame_timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        landmarker.detect_async(mp_image, frame_timestamp_ms)
        
        # 5. Display the frame (Output drawing omitted for brevity)
        cv2.imshow('MediaPipe Hand Tracking', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
```

---

## 7. Constraints & Limitations

While powerful, MediaPipe has several constraints you must design around:

### 1. Model Bundle Blackboxes
When using the Tasks API, you interact with `.task` files. These are bundled zip files containing the TFLite model and metadata. Extracting or modifying the internal pipeline of a `.task` file is difficult. You are largely constrained to what the specific Task API exposes.

### 2. Multi-Threading and Async
In `LIVE_STREAM` mode, results are returned asynchronously via a callback. You cannot easily return the result directly in your main loop block. This requires managing state (e.g., storing the latest result from the callback in a global/class variable to draw it in the main thread).

### 3. C++ Windows Build Issues
Building MediaPipe from source using Bazel on native Windows is highly unstable and often unsupported for newer features. If you must use C++, you should target Linux, macOS, or use Windows Subsystem for Linux (WSL2).

### 4. Limited Language Bindings for Advanced Features
The Python API is fantastic for rapid prototyping and using the Tasks API. However, if you need to create custom Calculators (custom graph nodes), you **must** write them in C++. You cannot write a custom MediaPipe Calculator purely in Python.

### 5. Single Target Focus
Many models (like Pose) work best when there is only one dominant subject in the frame. While `num_poses` or `num_hands` can be configured, performance and accuracy degrade significantly in crowded scenes.

### 6. Power Consumption
Running real-time 30FPS inference, even with optimized models, will drain mobile device batteries quickly and generate heat. Always provide users with options to lower the inference frame rate or disable tracking when not in focus.

---

## 8. Best Practices

1. **Use Tasks API First:** Always start with the Tasks API. Only drop down to the legacy Graph/Calculator API if you hit a hard limitation.
2. **Handle Timestamps Carefully:** In `LIVE_STREAM` mode, timestamps must be strictly monotonically increasing. A timestamp equal to or lower than a previous one will crash the pipeline.
3. **Decouple Rendering from Inference:** Do not perform heavy UI rendering inside the async callback function. Have the callback update a shared state, and let your main UI thread handle the drawing.
4. **Use Model Maker for Custom Data:** If you need to detect custom objects, use MediaPipe Model Maker to transfer-learn on top of existing models rather than training a generic TFLite model from scratch.
