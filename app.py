from flask import Flask, render_template_string, request, jsonify, send_file
import requests
import base64
import io

app = Flask(__name__)

# DeepSwapper API configuration
DEEPSWAP_API = "https://api.deepswapper.com/swap"
SECURITY_PAYLOAD = {
    "token": "0.ufDEMbVMT7mc9_XLsFDSK5CQqdj9Cx_Zjww0DevIvXN5M4fXQr3B9YtPdGkKAHjXBK6UC9rFcEbZbzCfkxxgmdTYV8iPzTby0C03dTKv5V9uXFYfwIVlqwNbIsfOK_rLRHIPB31bQ0ijSTEd-lLbllf3MkEcpkEZFFmmq8HMAuRuliCXFEdCwEB1HoYSJtvJEmDIVsooU3gYdrCm5yOJ8_lZ4DiHCSvy7P8-YxwJKkapJNCMUCFIfJbWDkDzvh8DGPyTRoHbURX8kClfImmPrGcqlfd7kkoNRcudS25IbNf1CGBsh8V96MtEhnTZvOpZfnp5dpV7MfgwOgvx7hUazUaC_wxQE63Aa0uOPuGvJ70BNrmeZIIrY9roD1Koj316L4g2BZ_LLZZF11wcrNNon8UXB0iVudiNCJyDQCxLUmblXUpt4IUvRoiOqXBNtWtLqY0su0ieVB0jjyDf_-zs7wc8WQ_jqp-NsTxgKOgvZYWV6Elz_lf4cNxGHZJ5BdcyLEoRBH3cksvwoncmYOy5Ulco22QT-x2z06xVFBZYZMVulxAcmvQemKfSFKsNaDxwor35p-amn9Vevhyb-GzA_oIoaTmc0fVXSshax2rdFQHQms86fZ_jkTieRpyIuX0mI3C5jLGIiOXzWxNgax9eZeQstYjIh8BIdMiTIUHfyKVTgtoLbK0hjTUTP0xDlCLnOt5qHdwe_iTWedBsswAJWYdtIxw0YUfIU22GMYrJoekOrQErawNlU5yT-LhXquBQY3EBtEup4JMWLendSh68d6HqjN2T3sAfVw0nY5jg7_5LJwj5gqEk57devNN8GGhogJpfdGzYoNGja22IZIuDnPPmWTpGx4VcLOLknSHrzio.tXUN6eooS69z3QtBp-DY1g.d882822dfe05be2b36ed1950554e1bac753abfe304a289adc4289b3f0d517356",
    "type": "invisible",
    "id": "deepswapper"
}

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <link rel="icon" href="https://files.catbox.moe/gt0b6x.jpg" />
  <link rel="apple-touch-icon" href="https://files.catbox.moe/gt0b6x.jpg" />
  <title>Face Swap Tool - BY Abbas</title>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6690222744270600" crossorigin="anonymous"></script>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    /* Modern Advanced Theme */
    :root {
      /* Primary Colors */
      --primary-50: #f0f9ff;
      --primary-100: #e0f2fe;
      --primary-200: #bae6fd;
      --primary-300: #7dd3fc;
      --primary-400: #38bdf8;
      --primary-500: #0ea5e9;
      --primary-600: #0284c7;
      --primary-700: #0369a1;
      --primary-800: #075985;
      --primary-900: #0c4a6e;
      
      /* Accent Colors */
      --accent-50: #fdf4ff;
      --accent-100: #fae8ff;
      --accent-200: #f5d0fe;
      --accent-300: #f0abfc;
      --accent-400: #e879f9;
      --accent-500: #d946ef;
      --accent-600: #c026d3;
      --accent-700: #a21caf;
      --accent-800: #86198f;
      --accent-900: #701a75;
      
      /* Dark Theme */
      --dark-50: #f8fafc;
      --dark-100: #f1f5f9;
      --dark-200: #e2e8f0;
      --dark-300: #cbd5e1;
      --dark-400: #94a3b8;
      --dark-500: #64748b;
      --dark-600: #475569;
      --dark-700: #334155;
      --dark-800: #1e293b;
      --dark-900: #0f172a;
      --dark-950: #020617;
      
      /* Gradients */
      --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --gradient-accent: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
      --gradient-dark: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
      --gradient-button: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      --gradient-button-hover: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
      --gradient-card: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
      
      /* Shadows */
      --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
      --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
      --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
      --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      --shadow-glow: 0 0 20px rgba(102, 126, 234, 0.5);
      --shadow-glow-accent: 0 0 30px rgba(240, 147, 251, 0.4);
      
      /* Spacing */
      --space-1: 0.25rem;
      --space-2: 0.5rem;
      --space-3: 0.75rem;
      --space-4: 1rem;
      --space-5: 1.25rem;
      --space-6: 1.5rem;
      --space-8: 2rem;
      --space-10: 2.5rem;
      --space-12: 3rem;
      --space-16: 4rem;
      --space-20: 5rem;
      
      /* Border Radius */
      --radius-sm: 0.375rem;
      --radius-md: 0.5rem;
      --radius-lg: 0.75rem;
      --radius-xl: 1rem;
      --radius-2xl: 1.5rem;
      --radius-3xl: 2rem;
      --radius-full: 9999px;
      
      /* Typography */
      --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
      --font-display: 'Space Grotesk', system-ui, sans-serif;
    }

    /* Global Styles */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: var(--font-sans);
      background: var(--dark-950);
      color: var(--dark-100);
      min-height: 100vh;
      position: relative;
      overflow-x: hidden;
      line-height: 1.6;
    }

    /* Animated Background */
    .animated-bg {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      z-index: -1;
      background: linear-gradient(45deg, #0f172a, #1e293b, #0f172a);
      background-size: 400% 400%;
      animation: gradientShift 15s ease infinite;
    }

    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .floating-orbs {
      position: fixed;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index: -1;
    }

    .orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      opacity: 0.3;
      animation: float 20s infinite ease-in-out;
    }

    .orb-1 {
      width: 400px;
      height: 400px;
      background: var(--gradient-primary);
      top: -200px;
      left: -200px;
      animation-delay: 0s;
    }

    .orb-2 {
      width: 500px;
      height: 500px;
      background: var(--gradient-accent);
      bottom: -250px;
      right: -250px;
      animation-delay: 5s;
    }

    .orb-3 {
      width: 300px;
      height: 300px;
      background: linear-gradient(135deg, #667eea 0%, #f093fb 100%);
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      animation-delay: 10s;
    }

    @keyframes float {
      0%, 100% { transform: translate(0, 0) scale(1); }
      25% { transform: translate(100px, -100px) scale(1.1); }
      50% { transform: translate(-100px, 100px) scale(0.9); }
      75% { transform: translate(50px, 50px) scale(1.05); }
    }

    /* Header */
    header {
      padding: var(--space-6) 0;
      position: relative;
      z-index: 10;
    }

    .header-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 var(--space-6);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo {
      display: flex;
      align-items: center;
      gap: var(--space-3);
      font-size: 1.5rem;
      font-weight: 700;
      font-family: var(--font-display);
      color: var(--dark-100);
      text-decoration: none;
      transition: all 0.3s ease;
    }

    .logo:hover {
      transform: translateY(-2px);
      color: var(--primary-400);
    }

    .logo-icon {
      width: 48px;
      height: 48px;
      background: var(--gradient-primary);
      border-radius: var(--radius-xl);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 1.5rem;
      box-shadow: var(--shadow-lg);
    }

    /* Main Container */
    .main-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: var(--space-8) var(--space-6);
      position: relative;
      z-index: 10;
    }

    .hero-section {
      text-align: center;
      margin-bottom: var(--space-16);
    }

    .hero-title {
      font-family: var(--font-display);
      font-size: clamp(2.5rem, 5vw, 4rem);
      font-weight: 900;
      line-height: 1.1;
      margin-bottom: var(--space-6);
      background: linear-gradient(135deg, #667eea 0%, #f093fb 50%, #667eea 100%);
      background-size: 200% auto;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      animation: gradientText 3s ease infinite;
      text-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
    }

    @keyframes gradientText {
      0% { background-position: 0% center; }
      50% { background-position: 100% center; }
      100% { background-position: 0% center; }
    }

    .hero-subtitle {
      font-size: 1.25rem;
      color: var(--dark-400);
      max-width: 600px;
      margin: 0 auto;
      line-height: 1.7;
    }

    /* Glass Card */
    .glass-card {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-3xl);
      padding: var(--space-10);
      box-shadow: var(--shadow-2xl);
      position: relative;
      overflow: hidden;
      transition: all 0.3s ease;
    }

    .glass-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      animation: shimmer 3s infinite;
    }

    @keyframes shimmer {
      0% { transform: translateX(-100%); }
      100% { transform: translateX(100%); }
    }

    .glass-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
    }

    /* Form Styles */
    .upload-form {
      display: flex;
      flex-direction: column;
      gap: var(--space-8);
    }

    .form-group {
      position: relative;
    }

    .form-label {
      display: block;
      font-size: 0.875rem;
      font-weight: 600;
      color: var(--dark-300);
      margin-bottom: var(--space-3);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .file-upload {
      position: relative;
      overflow: hidden;
      border-radius: var(--radius-xl);
      background: rgba(255, 255, 255, 0.03);
      border: 2px dashed rgba(255, 255, 255, 0.1);
      transition: all 0.3s ease;
    }

    .file-upload:hover {
      border-color: var(--primary-500);
      background: rgba(102, 126, 234, 0.05);
    }

    .file-upload input[type="file"] {
      position: absolute;
      opacity: 0;
      width: 100%;
      height: 100%;
      cursor: pointer;
    }

    .file-upload-label {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: var(--space-8);
      cursor: pointer;
      transition: all 0.3s ease;
    }

    .file-upload-icon {
      width: 64px;
      height: 64px;
      background: var(--gradient-primary);
      border-radius: var(--radius-full);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 1.5rem;
      margin-bottom: var(--space-4);
      transition: all 0.3s ease;
    }

    .file-upload:hover .file-upload-icon {
      transform: scale(1.1);
      box-shadow: var(--shadow-glow);
    }

    .file-upload-text {
      font-size: 1rem;
      color: var(--dark-200);
      margin-bottom: var(--space-2);
    }

    .file-upload-hint {
      font-size: 0.875rem;
      color: var(--dark-500);
    }

    .file-preview {
      margin-top: var(--space-4);
      border-radius: var(--radius-xl);
      overflow: hidden;
      display: none;
      box-shadow: var(--shadow-lg);
      position: relative;
    }

    .file-preview img {
      width: 100%;
      height: 200px;
      object-fit: cover;
      display: block;
    }

    .file-preview-overlay {
      position: absolute;
      top: var(--space-2);
      right: var(--space-2);
      background: rgba(0, 0, 0, 0.7);
      color: white;
      padding: var(--space-1) var(--space-3);
      border-radius: var(--radius-full);
      font-size: 0.75rem;
      backdrop-filter: blur(10px);
    }

    /* Button Styles */
    .btn-primary {
      background: var(--gradient-button);
      color: white;
      border: none;
      padding: var(--space-4) var(--space-8);
      border-radius: var(--radius-full);
      font-size: 1.125rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: var(--space-3);
      position: relative;
      overflow: hidden;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      box-shadow: var(--shadow-lg);
    }

    .btn-primary::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
      transition: left 0.5s ease;
    }

    .btn-primary:hover::before {
      left: 100%;
    }

    .btn-primary:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-glow);
      background: var(--gradient-button-hover);
    }

    .btn-primary:active {
      transform: translateY(-1px);
    }

    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.1);
      color: white;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: var(--space-3) var(--space-6);
      border-radius: var(--radius-full);
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      display: inline-flex;
      align-items: center;
      gap: var(--space-2);
      text-decoration: none;
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
      color: white;
    }

    /* Results Section */
    .results-section {
      margin-top: var(--space-12);
      display: none;
    }

    .results-section.active {
      display: block;
      animation: fadeInUp 0.6s ease;
    }

    @keyframes fadeInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .result-card {
      background: rgba(255, 255, 255, 0.05);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-3xl);
      overflow: hidden;
      box-shadow: var(--shadow-xl);
    }

    .result-image {
      width: 100%;
      max-height: 500px;
      object-fit: contain;
      display: block;
    }

    .result-actions {
      padding: var(--space-6);
      display: flex;
      gap: var(--space-4);
      justify-content: center;
      background: rgba(0, 0, 0, 0.2);
    }

    /* Loading State */
    .loading-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: var(--space-12);
      gap: var(--space-4);
    }

    .loading-spinner {
      width: 64px;
      height: 64px;
      border: 4px solid rgba(255, 255, 255, 0.1);
      border-top: 4px solid var(--primary-500);
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .loading-text {
      font-size: 1.125rem;
      color: var(--dark-300);
    }

    /* Error State */
    .error-state {
      background: rgba(239, 68, 68, 0.1);
      border: 1px solid rgba(239, 68, 68, 0.3);
      border-radius: var(--radius-xl);
      padding: var(--space-6);
      text-align: center;
      color: #fca5a5;
    }

    /* Features Grid */
    .features-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: var(--space-8);
      margin-top: var(--space-20);
    }

    .feature-card {
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: var(--radius-2xl);
      padding: var(--space-8);
      text-align: center;
      transition: all 0.3s ease;
      position: relative;
      overflow: hidden;
    }

    .feature-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: var(--gradient-card);
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .feature-card:hover::before {
      opacity: 1;
    }

    .feature-card:hover {
      transform: translateY(-5px);
      border-color: var(--primary-500);
    }

    .feature-content {
      position: relative;
      z-index: 1;
    }

    .feature-icon {
      width: 80px;
      height: 80px;
      background: var(--gradient-primary);
      border-radius: var(--radius-2xl);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 2rem;
      margin: 0 auto var(--space-6);
      box-shadow: var(--shadow-lg);
      transition: all 0.3s ease;
    }

    .feature-card:hover .feature-icon {
      transform: scale(1.1) rotate(5deg);
      box-shadow: var(--shadow-glow);
    }

    .feature-title {
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--dark-100);
      margin-bottom: var(--space-3);
      font-family: var(--font-display);
    }

    .feature-description {
      color: var(--dark-400);
      line-height: 1.7;
    }

    /* Footer */
    footer {
      margin-top: var(--space-20);
      padding: var(--space-8) 0;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      text-align: center;
      color: var(--dark-500);
    }

    .footer a {
      color: var(--primary-400);
      text-decoration: none;
      font-weight: 600;
      transition: color 0.3s ease;
    }

    .footer a:hover {
      color: var(--primary-300);
    }

    /* Responsive Design */
    @media (max-width: 768px) {
      .hero-title {
        font-size: 2.5rem;
      }

      .glass-card {
        padding: var(--space-6);
      }

      .features-grid {
        grid-template-columns: 1fr;
        gap: var(--space-6);
      }

      .result-actions {
        flex-direction: column;
      }

      .btn-secondary {
        width: 100%;
        justify-content: center;
      }
    }

    @media (max-width: 480px) {
      .header-content {
        flex-direction: column;
        gap: var(--space-4);
      }

      .hero-title {
        font-size: 2rem;
      }

      .glass-card {
        padding: var(--space-4);
      }

      .file-upload-label {
        padding: var(--space-6);
      }

      .file-upload-icon {
        width: 48px;
        height: 48px;
        font-size: 1.25rem;
      }
    }
  </style>
</head>
<body>
  <div class="animated-bg"></div>
  <div class="floating-orbs">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
  </div>

  <header>
    <div class="header-content">
      <a href="#" class="logo">
        <div class="logo-icon">
          <i class="fas fa-camera-retro"></i>
        </div>
        <span>AB Face Swap</span>
      </a>
    </div>
  </header>

  <main class="main-container">
    <section class="hero-section">
      <h1 class="hero-title">AI Face Swap Magic</h1>
      <p class="hero-subtitle">Transform your photos with cutting-edge AI technology. Upload two images and watch the magic happen instantly.</p>
    </section>

    <div class="glass-card">
      <form id="faceSwapForm" class="upload-form">
        <div class="form-group">
          <label class="form-label">Source Image</label>
          <div class="file-upload">
            <input type="file" id="source" name="source" accept="image/*" required />
            <label for="source" class="file-upload-label">
              <div class="file-upload-icon">
                <i class="fas fa-user"></i>
              </div>
              <div class="file-upload-text">Choose Source Image</div>
              <div class="file-upload-hint">Click to browse or drag and drop</div>
            </label>
          </div>
          <div class="file-preview" id="sourcePreview">
            <img src="" alt="Source preview" />
            <div class="file-preview-overlay">Source Image</div>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Target Image</label>
          <div class="file-upload">
            <input type="file" id="target" name="target" accept="image/*" required />
            <label for="target" class="file-upload-label">
              <div class="file-upload-icon">
                <i class="fas fa-image"></i>
              </div>
              <div class="file-upload-text">Choose Target Image</div>
              <div class="file-upload-hint">Click to browse or drag and drop</div>
            </label>
          </div>
          <div class="file-preview" id="targetPreview">
            <img src="" alt="Target preview" />
            <div class="file-preview-overlay">Target Image</div>
          </div>
        </div>

        <button type="submit" class="btn-primary" id="swapButton">
          <i class="fas fa-magic"></i>
          <span>Swap Faces</span>
        </button>
      </form>
    </div>

    <div class="results-section" id="resultsSection"></div>

    <section class="features-grid">
      <div class="feature-card">
        <div class="feature-content">
          <div class="feature-icon">
            <i class="fas fa-bolt"></i>
          </div>
          <h3 class="feature-title">Lightning Fast</h3>
          <p class="feature-description">Get your face-swapped images in seconds with our optimized AI processing pipeline.</p>
        </div>
      </div>

      <div class="feature-card">
        <div class="feature-content">
          <div class="feature-icon">
            <i class="fas fa-shield-alt"></i>
          </div>
          <h3 class="feature-title">Privacy First</h3>
          <p class="feature-description">Your images are processed securely and never stored on our servers. Complete privacy guaranteed.</p>
        </div>
      </div>

      <div class="feature-card">
        <div class="feature-content">
          <div class="feature-icon">
            <i class="fas fa-palette"></i>
          </div>
          <h3 class="feature-title">High Quality</h3>
          <p class="feature-description">Advanced AI ensures realistic, high-quality face swaps with natural-looking results.</p>
        </div>
      </div>

      <div class="feature-card">
        <div class="feature-content">
          <div class="feature-icon">
            <i class="fas fa-mobile-alt"></i>
          </div>
          <h3 class="feature-title">Mobile Friendly</h3>
          <p class="feature-description">Perfect experience on any device. Works seamlessly on desktop, tablet, and mobile.</p>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <p>&copy; 2023 - 2025 <a href="https://t.me/abbas_tech_india">Abbas</a>. All rights reserved.</p>
  </footer>

  <script>
    // File preview functionality
    function setupFilePreview(inputId, previewId) {
      const input = document.getElementById(inputId);
      const preview = document.getElementById(previewId);
      const img = preview.querySelector('img');

      input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = function(e) {
            img.src = e.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(file);
        } else {
          preview.style.display = 'none';
        }
      });
    }

    setupFilePreview('source', 'sourcePreview');
    setupFilePreview('target', 'targetPreview');

    // Form submission
    document.getElementById('faceSwapForm').addEventListener('submit', function(e) {
      e.preventDefault();
      
      const resultsSection = document.getElementById('resultsSection');
      const swapButton = document.getElementById('swapButton');
      const formData = new FormData(this);
      
      // Disable button and show loading
      swapButton.disabled = true;
      swapButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Processing...</span>';
      
      // Show loading state
      resultsSection.innerHTML = `
        <div class="glass-card">
          <div class="loading-state">
            <div class="loading-spinner"></div>
            <div class="loading-text">Swapping faces... This may take a moment.</div>
          </div>
        </div>
      `;
      resultsSection.classList.add('active');
      
      // Send request
      fetch('/swap', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          return response.blob();
        } else {
          return response.json().then(data => {
            throw new Error(data.message || 'Face swap failed');
          });
        }
      })
      .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        
        resultsSection.innerHTML = `
          <div class="result-card">
            <img src="${imageUrl}" alt="Face swap result" class="result-image" />
            <div class="result-actions">
              <a href="${imageUrl}" download="faceswap_result.jpg" class="btn-secondary">
                <i class="fas fa-download"></i>
                Download
              </a>
              <button type="button" class="btn-secondary" id="newSwapBtn">
                <i class="fas fa-redo"></i>
                New Swap
              </button>
            </div>
          </div>
        `;
        
        // Add event listener to new swap button
        document.getElementById('newSwapBtn').addEventListener('click', function() {
          document.getElementById('faceSwapForm').reset();
          document.getElementById('sourcePreview').style.display = 'none';
          document.getElementById('targetPreview').style.display = 'none';
          resultsSection.classList.remove('active');
          swapButton.disabled = false;
          swapButton.innerHTML = '<i class="fas fa-magic"></i><span>Swap Faces</span>';
          URL.revokeObjectURL(imageUrl);
        });
      })
      .catch(error => {
        resultsSection.innerHTML = `
          <div class="glass-card">
            <div class="error-state">
              <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
              <div>${error.message}</div>
            </div>
          </div>
        `;
        
        swapButton.disabled = false;
        swapButton.innerHTML = '<i class="fas fa-magic"></i><span>Swap Faces</span>';
      });
    });

    // Add drag and drop functionality
    function setupDragAndDrop(uploadElement) {
      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadElement.addEventListener(eventName, preventDefaults, false);
      });

      function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
      }

      ['dragenter', 'dragover'].forEach(eventName => {
        uploadElement.addEventListener(eventName, highlight, false);
      });

      ['dragleave', 'drop'].forEach(eventName => {
        uploadElement.addEventListener(eventName, unhighlight, false);
      });

      function highlight(e) {
        uploadElement.classList.add('drag-over');
      }

      function unhighlight(e) {
        uploadElement.classList.remove('drag-over');
      }

      uploadElement.addEventListener('drop', handleDrop, false);

      function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        const input = uploadElement.querySelector('input[type="file"]');
        input.files = files;
        
        // Trigger change event
        const event = new Event('change', { bubbles: true });
        input.dispatchEvent(event);
      }
    }

    document.querySelectorAll('.file-upload').forEach(setupDragAndDrop);
  </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    """Serve the web interface"""
    return render_template_string(html_template)

@app.route("/swap", methods=["POST"])
def face_swap():
    """API endpoint for face swapping"""
    try:
        if "source" not in request.files or "target" not in request.files:
            return jsonify({
                "success": False,
                "message": "source and target images are required"
            }), 400

        source_img = request.files["source"].read()
        target_img = request.files["target"].read()

        source_b64 = base64.b64encode(source_img).decode()
        target_b64 = base64.b64encode(target_img).decode()

        payload = {
            "source": source_b64,
            "target": target_b64,
            "security": SECURITY_PAYLOAD
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.post(DEEPSWAP_API, json=payload, headers=headers, timeout=120)

        if response.status_code != 200:
            return jsonify({
                "success": False,
                "message": "DeepSwap API failed",
                "status": response.status_code
            }), 500

        data = response.json()

        if "result" not in data:
            return jsonify({
                "success": False,
                "message": "No result received from API"
            }), 500

        image_bytes = base64.b64decode(data["result"])

        return send_file(
            io.BytesIO(image_bytes),
            mimetype="image/png",
            as_attachment=False
        )

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api", methods=["GET"])
def api_info():
    """API information endpoint"""
    return jsonify({
        "status": "running",
        "usage": "POST /swap with source & target images",
        "endpoints": {
            "web_interface": "GET /",
            "swap_api": "POST /swap",
            "api_info": "GET /api"
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
