#!/usr/bin/env python3
import os
import platform
import subprocess
import shutil

def clean_build_dirs():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)

def build_cli():
    """Build CLI version"""
    subprocess.run([
        'pyinstaller',
        '--clean',
        '--onefile',
        '--name', f'phoenix-cli-{platform.system().lower()}',
        'phoenix.py'
    ], check=True)

def build_gui():
    """Build GUI version"""
    subprocess.run([
        'pyinstaller',
        '--clean',
        '--onefile',
        '--windowed',
        '--name', f'phoenix-gui-{platform.system().lower()}',
        'phoenix_gui.py'
    ], check=True)

def main():
    # Clean previous builds
    clean_build_dirs()

    # Build both CLI and GUI versions
    build_cli()
    build_gui()

    print("Build completed! Check the 'dist' directory for the executables.")
    print(f"Built for platform: {platform.system()}")

if __name__ == '__main__':
    main() 