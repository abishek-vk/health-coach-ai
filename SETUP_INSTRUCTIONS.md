# 🚀 Setup & Installation Guide

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: Minimum 512MB RAM
- **Disk Space**: Minimum 100MB for installation

## Quick Installation (5 minutes)

### Step 1: Open Terminal/Command Prompt

**Windows**: Press `Win + R`, type `cmd`, press Enter
**macOS/Linux**: Open Terminal application

### Step 2: Navigate to Project Directory

```bash
cd path/to/health-coach-ai
```

### Step 3: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

You should see output similar to:
```
Successfully installed streamlit-1.28.1 pandas-2.1.1 numpy-1.24.3 ...
```

## Running the Application

### Option 1: Interactive Web Dashboard (Recommended)

```bash
streamlit run main.py
```

Expected output:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://xxx.xxx.xxx.xxx:8501
```

Then:
1. Open your web browser
2. Go to `http://localhost:8501`
3. Start using the application

### Option 2: Run System Demonstration

```bash
python demo.py
```

This shows how the system works without any web interface.

## First Time Usage

### Using the Dashboard

1. **Home Page**
   - Enter a unique User ID (e.g., "user_001")
   - Click "Start Tracking"

2. **Enter Health Data**
   - Fill in your basic information (age, height, weight, etc.)
   - Enter today's metrics (steps, sleep, water)
   - Click "Save Health Data"

3. **View Summary**
   - See your health profile
   - View calculated metrics (BMI, activity level, etc.)
   - Check trends in graphs

4. **Get Recommendations**
   - Receive personalized exercise suggestions
   - Get diet guidance
   - See sleep improvement tips
   - Get hydration reminders
   - View health alerts

## Troubleshooting Installation Issues

### Python Not Found

```bash
# Verify Python installation
python --version

# If not found, download from python.org and install
# Make sure to check "Add Python to PATH" during installation
```

### Pip Not Found

```bash
# Try python -m pip instead
python -m pip install -r requirements.txt
```

### Permission Denied (macOS/Linux)

```bash
# Use sudo if needed
sudo pip install -r requirements.txt

# Or use user installation
pip install --user -r requirements.txt
```

### Module Not Found Errors

```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Then reinstall requirements
pip install -r requirements.txt
```

## Streamlit Configuration

### Changing Port

If port 8501 is already in use:

```bash
streamlit run main.py --server.port 8502
```

### Disabling Welcome Message

```bash
streamlit run main.py --logger.level=error
```

### Running Remotely

```bash
streamlit run main.py --server.headless true --server.address 0.0.0.0
```

## File Permissions

The system creates two JSON files:
- `data/user_records.json` - Historical health records
- `data/user_profiles.json` - Compressed health profiles

**Ensure the directory has write permissions:**

```bash
# macOS/Linux
chmod 755 data/

# Windows (usually automatic)
```

## Verifying Installation

Run the demo to verify everything is working:

```bash
python demo.py
```

Expected output:
- ✅ Data collection successful
- ✅ Files created in data/ directory
- ✅ 11 health records stored
- ✅ Data compressed successfully
- ✅ Recommendations generated

If you see ✅ marks throughout, your installation is complete!

## Project Structure Verification

Check that all files exist:

```
health-coach-ai/
├── requirements.txt          ✓
├── main.py                   ✓
├── demo.py                   ✓
├── README.md                 ✓
├── SETUP_INSTRUCTIONS.md    ✓ (this file)
├── modules/
│   ├── __init__.py          ✓
│   ├── validators.py        ✓
│   ├── data_input.py        ✓
│   ├── file_storage.py      ✓
│   ├── profile_summarizer.py ✓
│   └── recommendation_engine.py ✓
└── data/
    ├── user_records.json     (created on first run)
    └── user_profiles.json    (created on first run)
```

## Next Steps

1. **Run the Demo**: `python demo.py`
2. **Launch Dashboard**: `streamlit run main.py`
3. **Enter Your Health Data**: Use the web interface
4. **Check Recommendations**: View personalized suggestions
5. **Read Documentation**: See README.md for detailed info

## Common Workflows

### Daily Health Tracking

```bash
# 1. Start the app
streamlit run main.py

# 2. Login with your User ID
# 3. Go to "Input Health Data"
# 4. Enter today's metrics
# 5. Check your summary
# 6. View recommendations
```

### Viewing Historical Data

```bash
# 1. Go to "Data Management" in Streamlit
# 2. Enter your User ID
# 3. Select "View Records"
# 4. See all your historical data
```

### Backing Up Your Data

```bash
# Your data is in the data/ folder
# Copy it to backup it up:

# Windows
copy data\ backup_data\ /Y

# macOS/Linux
cp -r data/ backup_data/
```

### Resetting Your Data

```bash
# Delete JSON files to start fresh
# Windows
del data\user_records.json
del data\user_profiles.json

# macOS/Linux
rm data/user_records.json
rm data/user_profiles.json
```

## Getting Help

### Check Logs

The system logs to console. Look for messages like:
- ✅ Success messages (green text)
- ⚠️ Warnings (yellow text)
- ❌ Errors (red text)

### Debug Mode

View detailed output:

```bash
# In Python code, increase logging:
# Edit modules and add:
# import logging
# logging.basicConfig(level=logging.DEBUG)
```

### Common Errors

**Error: "module not found"**
- Solution: Check virtual environment is activated
- Run: `pip install -r requirements.txt`

**Error: "port already in use"**
- Solution: Use different port
- Run: `streamlit run main.py --server.port 8502`

**Error: "JSON decode error"**
- Solution: Delete corrupted data file and restart
- Run: `del data\user_records.json` (Windows)

## Hardware Recommendations

| Category | Minimum | Recommended |
|----------|---------|------------|
| RAM | 512 MB | 2 GB |
| Storage | 100 MB | 500 MB |
| Processor | Dual-core | Quad-core |
| Python | 3.8 | 3.10+ |

## Network Requirements

- **Internet**: Required only for:
  - Initial pip package download
  - Loading Streamlit framework
- **Local Run**: Once installed, runs completely offline

## Performance Tips

1. **Faster Installation**
   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

2. **Faster Streamlit Startup**
   ```bash
   streamlit run main.py --logger.level=error
   ```

3. **Lightweight Data**
   - System automatically compresses data
   - Typically 11 records → ~500 bytes

## Updating Dependencies

To get the latest versions:

```bash
pip install -r requirements.txt --upgrade
```

Or update specific packages:

```bash
pip install streamlit --upgrade
```

## Uninstalling

To completely remove the application:

```bash
# Deactivate virtual environment
deactivate

# Delete the entire project folder
# Windows: Right-click → Delete
# macOS/Linux: rm -rf /path/to/health-coach-ai
```

## Environment Variables (Advanced)

Create a `.env` file for custom settings (optional):

```
DATA_DIR=data/
LOG_LEVEL=INFO
```

Then use in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
data_dir = os.getenv('DATA_DIR', 'data')
```

## Support Resources

- **Documentation**: See README.md
- **Example Code**: Run demo.py
- **Streamlit Docs**: https://docs.streamlit.io/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Python Docs**: https://docs.python.org/

## License & Support

This is an educational project. Feel free to modify and extend it!

---

**Ready to start?**

```bash
streamlit run main.py
```

Happy health tracking! 🏥💪
