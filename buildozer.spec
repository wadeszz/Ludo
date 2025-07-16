name: Build LudoUltimate APK

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          sudo apt update
          sudo apt install -y \
            build-essential git zip unzip openjdk-17-jdk python3-pip \
            libffi-dev libssl-dev libsdl2-dev libgles2-mesa-dev \
            libgstreamer1.0-dev libmtdev-dev xclip xsel libjpeg-dev

          pip install --upgrade pip
          pip install cython virtualenv buildozer

      - name: Initialize Buildozer spec
        run: buildozer init || true

      - name: Build APK
        run: buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: LudoUltimate-APK
          path: bin/*.apk
