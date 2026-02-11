# Instructions to Fix feature_engineering.ipynb

## Problem
The notebook has a path error when loading the cleaned data file.

## Solution

### Step 1: Update the Data Loading Cell
Find the cell with this code (around line 51):
```python
data=pd.read_csv('RFM analysis/src/data/clean_data.csv',parse_dates=['InvoiceDate'])
```

**Replace it with:**
```python
data=pd.read_csv('src/data/clean_data.csv',parse_dates=['InvoiceDate'])
```

### Step 2: Restart Kernel
After making the change:
1. Restart the Jupyter kernel (Kernel → Restart)
2. Run all cells from the beginning

## What Was Fixed

### In `src/create_RFM.py`:
1. ✅ Fixed typo: `'InvoiceNO'` → `'InvoiceNo'`
2. ✅ Fixed `rfm_pipeline()` to properly capture and return dataframe from each function

### In `src/data_preprocessing.py`:
1. ✅ Fixed file path to use absolute path based on script location
2. ✅ Fixed pipeline function to capture return values

## Alternative: Use Helper Function
You can also add this helper function to automatically find the correct path:

```python
import os

def get_data_path(filename):
    """Get the correct path to data file"""
    # Get the notebook's directory
    notebook_dir = os.getcwd()
    return os.path.join(notebook_dir, 'src', 'data', filename)

# Then use it like this:
data = pd.read_csv(get_data_path('clean_data.csv'), parse_dates=['InvoiceDate'])
```
