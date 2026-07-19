name: Build Jarvis APK
on:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Flutter SDK
        uses: subosito/flutter-action@v2
        with:
          channel: 'stable'

      - name: Install Dependencies
        run: |
          pip install flet
          pip install -r requirements.txt

      - name: Build APK
        run: |
          flet build apk

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v3
        with:
          name: jarvis-app-apk
          path: build/apk/*.apk
