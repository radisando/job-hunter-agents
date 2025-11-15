import os
import streamlit as st

from google import genai
from google.genai.agents import Agent, ParallelAgent, SequentialAgent
from google.genai.runners import InMemoryRunner
from google.genai.tools import google_search


# ==========================
# 1. SETUP API KEY
# ==========================
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")


# ==========================
# 2. DEFINE AGENTS
# ==========================

# 1️⃣ Company Finder Agent
company_finder = Agent(
    name="CompanyFinder",
    model="gemini-2.5-flash-lite",
    instruction="""List around 10 companies located in or near Cologne (Germany)
that have **more than 200 employees** and are **not consulting firms**.
Focus on product-based companies, retailers, manufacturers, or service providers
with in-house data teams.
Provide: Company name, industry, estimated employee count, and headquarters location.""",
    tools=[google_search],
    output_key="company_list",
)

# 2️⃣ Job Openings Agent
job_openings = Agent(
    name="JobOpeningsChecker",
    model="gemini-2.5-flash-lite",
    instruction="""From the following list of companies:
{company_list}

Find which companies currently have open roles related to:
- Data Analyst
- Business Intelligence Analyst
- Data Scientist

Mention the job title, location, and (if available) where the opening was found.
Keep the results factual and concise.""",
    tools=[google_search],
    output_key="openings_report",
)

# 3️⃣ Company Insights Agent
company_insights = Agent(
    name="CompanyInsights",
    model="gemini-2.5-flash-lite",
    instruction="""For the companies mentioned in:
{company_list}

Gather short insights for each one:
- What industry they operate in
- Whether they have a data-driven culture or use analytics tools (BI, AI, ML, etc.)
- Recent data-related projects or initiatives if available
Summarize in ~2 sentences per company.""",
    tools=[google_search],
    output_key="insights_summary",
)

# 4️⃣ Aggregator Agent
aggregator = Agent(
    name="AggregatorAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Combine and analyze the results:

**Companies Identified:**
{company_list}

**Open Positions:**
{openings_report}

**Company Insights:**
{insights_summary}

Generate a final **"Data Jobs Target Report"** (approx. 250 words) including:
- The 5 most promising companies to apply to.
- Why they are interesting for a Job Position {position}.
- Possible next actions (e.g., explore their career page, connect with data employees, follow LinkedIn).""",
    output_key="final_report",
)


# ==========================
# 3. BUILD AGENT PIPELINE
# ==========================

parallel_phase = ParallelAgent(    name="ParallelResearchPhase",
                                   sub_agents=[company_finder, job_openings, company_insights])

root_agent = SequentialAgent( name="CologneDataJobsSystem",
                              sub_agents=[parallel_phase, aggregator])

runner = InMemoryRunner(agent=root_agent)


# ==========================
# 4. STREAMLIT UI
# ==========================

st.set_page_config(page_title="Job Hunter — Agents", page_icon="🔎")

st.title("🔎 Job Hunter — Multi-Agent Job Search")
st.markdown("Type the job title and city (e.g., 'Data Analyst', 'Cologne') and click GO.")

st.markdown(
    "This app identifies non-consulting companies in the desired city "
    "with more than 200 employees that hire for the chosen position."
)

with st.form("search_form"):
    position = st.text_input("Job title / keywords", value="Data Analyst")
    city = st.text_input("City / Region", value="Cologne")
    min_employees = st.number_input("Minimum employees", value=200, step=50)
    include_consulting = st.checkbox("Include consulting companies?", value=False)
    submitted = st.form_submit_button("🚀 GO!")

if submitted:
    query = f"Find companies in {city} with more than {min_employees} employees (exclude consulting={not include_consulting}) that hire for {position} / Data Analyst / BI Analyst / Data Scientist"
    with st.spinner("Running agents — this may take a few seconds..."):
        try:
            # pass the user query into the pipeline; agents can reference it or use placeholders
            response = runner.run(query)
            st.subheader("Result")
            st.write(response)
        except Exception as e:
            st.error(f"Agent error: {e}")


st.caption("Built with Google Gemini ADK + Streamlit | Created by Rafael")
