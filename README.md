# PicCompressor

**PicCompressor** is a Python-based application that provides a graphical user interface to compress grayscale BMP images using block-wise Discrete Cosine Transform (DCT). Users can select an image file, set parameters for block size and frequency threshold, and compress images. After the compression, the software provides a view containing the original photo and the compressed (and decompressed) one. 

---

## Technologies Used

- Python 3  
- NumPy  
- SciPy  
- Pillow  
- Matplotlib  
- Tkinter

---

## Project Structure

<pre>
PicCompressor/
├── compression_results/         # Sample images for testing
├── images/                      # Grayscale images to be used as input
├── plots/                       # Useful plots for the project report
└── src/
    ├── controller/              # controller.py manages calls from the view and calls model functions
    ├── model/                   # Contains DCT1D, DCT2D, utils, and compression logic
    ├── test/                    # Test scripts comparing single process vs multiprocess performance
    ├── view/                    # GUI interface (interface.py)
    └── extracompressor/         # Additional compressors (multiprocess and custom DCT-based), not connected to the GUI
</pre>

---

## Installation 

1. Clone the repository:

```bash
git clone https://github.com/AlessandroIsceri/PicCompressor.git
```

2. Install required packages

```bash
pip install -r requirements.txt
```

## Usage

To run the GUI:

1. Navigate to the `src/view` directory:

```bash
cd src/view
```

2. Run the interface script:

```bash
python interface.py
```

3. Use the GUI to:

* Select a grayscale BMP image from your filesystem
* Set the block size parameter F
* Set the frequency threshold d
* Start the compression

## More Information
For more information on the project and obtained results, please read the report: [`Relazione_Progetto_2_Metodi_Farioli_Isceri.pdf`](https://github.com/AlessandroIsceri/PicCompressor/blob/master/Relazione_Progetto_2_Metodi_Farioli_Isceri.pdf).