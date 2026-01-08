# PC-VOICE-BOT

**Empower Your Voice. Command Your World Instantly.**

![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11-blue) ![Version](https://img.shields.io/badge/version-0.1-blue)

**Built with the tools and technologies:**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![VS Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

---

## Table of Contents

* [Overview](#overview)
* [Getting Started](#getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Usage](#usage)
* [Testing](#testing)

---

## Overview

pc-voice-bot is an open source voice assistant tailored for Windows PC, enabling users to control their system through natural language commands. It combines speech recognition, text-to-speech, and multimedia controls to facilitate hands-free interaction and automation.

**Why pc-voice-bot?**

The project aims to enhance PC usability by providing a customizable voice-controlled interface. The core features include:

* 🎙️ **Voice Command Recognition:** Understands and executes user commands like searching the web, playing music, opening websites, or shutting down.
* 🗣️ **Text-to-Speech Feedback:** Offers real-time voice responses for a more natural interaction experience.
* 🛠️ **Customizable Settings:** Uses a configurable bot name ("Jarvis") for personalized interactions.
* 🗂️ **Windows Shortcuts Reference:** Integrates quick access to system functions, boosting productivity.
* 🧠 **Natural Language Processing:** Supports commands similar to popular voice assistants, making interaction intuitive.
* ⚙️ **Ongoing Development:** Continually improving features for better stability and functionality.

---

## Getting Started

### Prerequisites

The project requires the following dependencies:

* **Programming Language:** Python
* **Package Manager:** Conda

### Installation

Build pc-voice-bot from the source and install dependencies:

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/nathanlobo/pc-voice-bot](https://github.com/nathanlobo/pc-voice-bot)
    ```

2.  **Navigate to the project directory:**

    ```bash
    cd pc-voice-bot
    ```

3.  **Install the dependencies:**

    Using **conda**:

    ```bash
    conda env create -f conda.yml
    ```

---

## Usage

Run the project with:

Using **conda**:

```bash
conda activate {env}
python {main.py}