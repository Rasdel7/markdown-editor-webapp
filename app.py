import streamlit as st
import json
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Markdown Editor",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ Live Markdown Editor")
st.markdown("Write markdown and see it rendered "
            "live — with templates and export.")
st.markdown("---")

# Templates
TEMPLATES = {
    "Blank": "",

    "GitHub README": """# Project Name 🚀

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)

## About
Brief description of your project.

## Features
- Feature 1
- Feature 2
- Feature 3

## Installation
```bash
pip install -r requirements.txt
python app.py
```

## Usage
Describe how to use the project.

## Technologies Used
- Python
- Streamlit
- Pandas

## Author
**Your Name** — [GitHub](https://github.com/username)

## License
MIT License
""",

    "Blog Post": """# Your Blog Post Title

*Published on {date} by Jyotiraditya*

---

## Introduction
Start with a hook that grabs the reader's attention.

## Main Content

### Section 1
Your first main point goes here.

### Section 2
Your second main point goes here.

### Section 3
Your third main point goes here.

## Code Example
```python
# Your code here
print("Hello World")
```

## Conclusion
Summarize your key points and call to action.

---
*Thanks for reading! Follow me on
[GitHub](https://github.com/Rasdel7)*
""".replace("{date}",
            datetime.now().strftime('%B %d, %Y')),

    "Project Documentation": """# Project Documentation

## Overview
Brief description of what this project does.

## Table of Contents
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [API Reference](#api-reference)
4. [Examples](#examples)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Steps
```bash
git clone https://github.com/username/project
cd project
pip install -r requirements.txt
```

## Configuration
Describe configuration options here.

## API Reference

### Function Name
```python
def function_name(param1, param2):
    \"\"\"
    Description of function.
    
    Args:
        param1: Description
        param2: Description
    
    Returns:
        Description of return value
    \"\"\"
```

## Examples
```python
# Example usage
result = function_name("value1", "value2")
print(result)
```

## Contributing
Pull requests are welcome!

## License
MIT
""",

    "Meeting Notes": f"""# Meeting Notes

**Date:** {datetime.now().strftime('%B %d, %Y')}
**Attendees:** 

---

## Agenda
1. Item 1
2. Item 2
3. Item 3

## Discussion

### Topic 1
Notes here...

### Topic 2
Notes here...

## Action Items
- [ ] Task 1 — assigned to: @person
- [ ] Task 2 — assigned to: @person
- [ ] Task 3 — assigned to: @person

## Next Meeting
**Date:** TBD
**Topics:** TBD
""",

    "Data Science Report": f"""# Data Science Project Report

**Author:** Jyotiraditya
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Dataset:** Dataset Name

---

## Executive Summary
Brief summary of findings.

## Problem Statement
What problem are we solving?

## Data Description
| Feature | Type | Description |
|---------|------|-------------|
| col1 | numeric | Description |
| col2 | categorical | Description |

## Methodology
1. Data cleaning
2. Exploratory analysis
3. Feature engineering
4. Model training
5. Evaluation

## Key Findings
- Finding 1
- Finding 2
- Finding 3

## Model Performance
| Model | Accuracy | F1 Score |
|-------|----------|----------|
| Random Forest | 95% | 0.94 |
| Logistic Regression | 91% | 0.90 |

## Conclusion
Summary of results and next steps.

## References
- Reference 1
- Reference 2
"""
}

# Session state
if 'markdown_content' not in st.session_state:
    st.session_state.markdown_content = \
        TEMPLATES["GitHub README"]
if 'template_selected' not in st.session_state:
    st.session_state.template_selected = \
        "GitHub README"
if 'saved_docs' not in st.session_state:
    st.session_state.saved_docs = {}
if 'word_count' not in st.session_state:
    st.session_state.word_count = 0

# Sidebar
st.sidebar.header("⚙️ Options")

# Template selector
template = st.sidebar.selectbox(
    "Load template:",
    list(TEMPLATES.keys())
)

if st.sidebar.button("📄 Load Template",
                     type="primary"):
    st.session_state.markdown_content = \
        TEMPLATES[template]
    st.rerun()

st.sidebar.markdown("---")

# Save document
st.sidebar.markdown("### 💾 Save Document")
doc_name = st.sidebar.text_input(
    "Document name:",
    placeholder="e.g. my-readme"
)

if st.sidebar.button("💾 Save"):
    if doc_name.strip():
        st.session_state.saved_docs[doc_name] = {
            'content': st.session_state
                       .markdown_content,
            'saved':   datetime.now().strftime(
                '%d %b %H:%M')
        }
        st.sidebar.success(f"Saved '{doc_name}'!")
    else:
        st.sidebar.warning("Enter a document name.")

# Load saved
if st.session_state.saved_docs:
    st.sidebar.markdown("### 📂 Saved Documents")
    for name, doc in st.session_state\
            .saved_docs.items():
        col1, col2 = st.sidebar.columns([2, 1])
        with col1:
            st.sidebar.caption(
                f"📄 {name} — {doc['saved']}")
        if st.sidebar.button(
            f"Load {name}",
            key=f"load_{name}"
        ):
            st.session_state.markdown_content = \
                doc['content']
            st.rerun()

# Markdown cheatsheet
st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Quick Reference")
st.sidebar.markdown("""
`# H1` `## H2` `### H3`
`**bold**` `*italic*`
`[link](url)`
`![image](url)`
`` `code` ``
`- item` for lists
`1.` for numbered
`> blockquote`
`---` for divider
`| col |` for tables
`- [ ]` for checkboxes
""")

# Main area — Editor and Preview
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✏️ Editor")

    # Toolbar
    t1, t2, t3, t4, t5, t6 = st.columns(6)
    toolbar_actions = {
        "**B**":  "**bold text**",
        "*I*":    "*italic text*",
        "H1":     "# Heading",
        "H2":     "## Heading",
        "`C`":    "`code`",
        "🔗":     "[link text](url)"
    }
    for (label, insert), col in zip(
        toolbar_actions.items(),
        [t1, t2, t3, t4, t5, t6]
    ):
        with col:
            if st.button(label,
                         key=f"tb_{label}",
                         use_container_width=True):
                st.session_state\
                    .markdown_content += \
                    f"\n{insert}"
                st.rerun()

    # Editor
    content = st.text_area(
        "Write markdown:",
        value=st.session_state.markdown_content,
        height=500,
        label_visibility="collapsed"
    )
    st.session_state.markdown_content = content

    # Stats
    words   = len(content.split())
    chars   = len(content)
    lines   = len(content.split('\n'))
    headers = content.count('\n#')

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Words",    words)
    s2.metric("Chars",    chars)
    s3.metric("Lines",    lines)
    s4.metric("Headers",  headers)

with col2:
    st.markdown("### 👁️ Preview")
    st.markdown(
        "<div style='"
        "border: 0.5px solid #333; "
        "border-radius: 8px; "
        "padding: 20px; "
        "min-height: 500px'>"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(content)

# Export section
st.markdown("---")
st.markdown("### 📤 Export")

ex1, ex2, ex3 = st.columns(3)

with ex1:
    st.download_button(
        "⬇️ Download .md file",
        content,
        "document.md",
        "text/markdown",
        use_container_width=True
    )

with ex2:
    st.download_button(
        "⬇️ Download .txt file",
        content,
        "document.txt",
        "text/plain",
        use_container_width=True
    )

with ex3:
    # Convert to HTML
    try:
        import markdown as md_lib
        html_content = md_lib.markdown(content)
    except:
        html_content = f"<pre>{content}</pre>"

    st.download_button(
        "⬇️ Download .html file",
        html_content,
        "document.html",
        "text/html",
        use_container_width=True
    )

st.markdown("---")
st.markdown(
    "Built by **Jyotiraditya** | "
    "Live Markdown Editor | "
    "Write · Preview · Export ✍️"
)