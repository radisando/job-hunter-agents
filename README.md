## Job Hunter Agents – Experimental Multi-Agent Job Search System

This project is an experimental attempt to build a multi-agent job-search assistant using Google’s Agent Development Kit (ADK).
The idea explored in this prototype:

- Use Parallel Agents to collect different types of job-related information

- Use Sequential Agents to orchestrate a pipeline

- Deploy the entire system as a Streamlit app

- Make it publicly accessible via Hugging Face Spaces

The intended multi-agent workflow included steps like:

- Agent 1 → Identify companies in a region (e.g., Cologne) with +200 employees

- Agent 2 → Check which of those companies hire Data Analysts, BI Analysts, or Data Scientists

- Agent 3 → Search for open job listings

- Agent 4 → Aggregate all findings into a final report for the user


### 💡Why the deployment failed on Hugging Face

Hugging Face does not currently support the Google ADK Agents module (google.genai.agents), because:

- The Agents SDK is not available on PyPI

- HF Spaces install dependencies only from pip

- The missing package causes import errors such as: No module named 'google.genai.agents'

Even installing google-genai alone is not enough — the ADK agent classes are only included inside Google Cloud / Vertex AI environments, not HF containers.


### 🚀 Recommended Deployment: Google Cloud Platform

Since Hugging Face cannot run ADK Agents, the best deployment option is:

✔️ Google Cloud Run, or

✔️ Vertex AI Workbench + Cloud Run frontend

Advantages:

- Native support for the Google GenAI ADK

- Works with both Sequential and Parallel Agents

- Easy secret management (API keys)

- No dependency issues



### Next step: 

- Deploy to Google Cloud Run for full functionality
