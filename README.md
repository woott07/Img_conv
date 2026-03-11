# 🖼️ Image Converter & Compressor (img-convo)

A lightweight **Python CLI utility** that converts images to **JPG** and compresses them to a **target file size (KB)** while preserving the best possible quality.

This tool is designed to be simple, fast, and reliable for everyday image processing tasks such as reducing image size for uploads, sharing, or storage.

---

# ✨ Features

### 🔄 Universal Image → JPG Conversion
Convert almost any image format into **standard JPG**.

Supported formats include:
- PNG
- WebP
- HEIC / HEIF (iPhone images)
- BMP
- TIFF
- JPEG
- and most formats supported by **Pillow**

Transparency in formats like PNG or WebP is automatically handled by converting:
```
RGBA / P → RGB
```
before saving as JPG.

---

### 🎯 Target Size Compression

Compress an image so that the final file size stays **under a specified KB limit**.

Example:

```
Input: 4.3 MB image
Target: 500 KB
Output: ≤ 500 KB JPG
```

The script uses an **intelligent binary search algorithm** to find the **highest possible JPEG quality** that still meets the target size.

Quality search range:

```
JPEG Quality: 5 → 95
```

---

### 🧠 Smart Fallback Resizing

If the image is **still too large even at the lowest quality**, the script will automatically:

1. Reduce the image resolution
2. Retry compression
3. Repeat until the target size is reached

Resizing uses the **Lanczos filter**, which provides high-quality downsampling.

---

### 💻 Flexible CLI Usage

The tool supports **two usage modes**.

#### Interactive Mode

Run without arguments:

```
python img.py
```

You will be prompted for:
```
image path
target size (KB)
```

You can also **drag and drop an image into the terminal**.

---

#### Headless / Script Mode

Provide arguments directly:

```
python img.py input_image.png 500
```

Example:

```
python img.py photo.heic 300
```

This makes the tool suitable for:
- automation
- scripts
- batch workflows

---

# 🧰 Tech Stack

- **Python**
- **Pillow** – image processing
- **pillow-heif** – HEIC / HEIF image support

---

# 📦 Installation

### 1. Clone the repository
https://github.com/woott07/Img_conv
```
git clone https://github.com/woott07/Img_conv
cd img-convo
```

### 2. Install dependencies

```
pip install pillow pillow-heif
```

---

# 🚀 Usage

### Convert and compress an image

```
python img.py image.png 500
```

Output:

```
image.jpg
```

Compressed to **≤ 500 KB**.

---

### Interactive mode

```
python img.py
```

Follow the prompts.

---

# ⚙️ How It Works

The compression system works in **three stages**.

### 1. Convert to JPG

If the input image is not JPG, it is converted while handling transparency.

---

### 2. Binary Search Compression

The script searches for the optimal JPEG quality using **binary search**.

Example search flow:

```
Quality 50 → too large
Quality 30 → small enough
Quality 40 → slightly large
Quality 35 → perfect
```

This ensures the **best quality under the target size**.

---

### 3. Resolution Fallback

If compression alone cannot reach the target size:

```
Image resolution is reduced
↓
Compression runs again
```

This loop continues until the target size is achieved.

---

# 📂 Project Structure

```
img-convo/
│
├── img.py
└── README.md
```

---

# 🛠 Example

Input image:

```
IMG_2314.HEIC
Size: 4.2 MB
```

Command:

```
python img.py IMG_2314.HEIC 500
```

Output:

```
IMG_2314.jpg
Size: 492 KB
```

---

# 📄 License

Feel Free to modify on your need :)

---

# 👨‍💻 Author

**Md Sowel Rana**
