# EPITECH Web Optimizer

A Flask-based web optimization tool that analyzes, optimizes, and reports on web assets.

## Features

- **Web Analyzer**: Analyzes web pages and assets
- **Optimizer**: Optimizes images, CSS, JavaScript, and HTML
- **Dashboard**: View optimization reports through a web interface

## Local Development

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd EPITECH-main

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
# Run the dashboard
python dashboard/app.py
```

Visit `http://localhost:5000` to view the dashboard.

## Deployment on Render

### Quick Deploy

1. **Push to GitHub**:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Click "Create Web Service"

### Manual Configuration (if not using render.yaml)

If you prefer manual setup:

1. **Create New Web Service** on Render
2. **Configure**:

   - **Name**: epitech-optimizer
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT dashboard.app:app`
   - **Plan**: Free

3. **Environment Variables** (optional):
   - `PYTHON_VERSION`: 3.11.0
   - `FLASK_ENV`: production

### Post-Deployment

Your app will be available at: `https://your-app-name.onrender.com`

## Project Structure

```
EPITECH-main/
├── analyzer/           # Web analysis module
│   └── analyzer.py
├── dashboard/          # Flask web dashboard
│   ├── app.py
│   └── templates/
├── optimizer/          # Optimization modules
│   ├── cleaner.py
│   ├── compressors.py
│   ├── minifier.py
│   └── optimizer.py
├── reports/            # Generated reports
├── requirements.txt    # Python dependencies
└── render.yaml        # Render deployment config
```

## Usage

### Analyzing a Website

```python
from analyzer.analyzer import analyze_website

results = analyze_website('https://example.com')
```

### Optimizing Assets

```python
from optimizer.optimizer import optimize_images

optimize_images('path/to/images')
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
