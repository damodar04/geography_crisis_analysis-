import streamlit as st
import pandas as pd
from openai import OpenAI, AzureOpenAI
import json
import time
import requests
from PIL import Image 

# --- Page Configuration ---
st.set_page_config(
    page_title="Interactive Maritime Intelligence Center",
    page_icon="📡", 
    layout="wide",
)

# --- API Keys ---
NEWSAPI_KEY = "ed2adf20b47247429" 
DEEPSEEK_API_KEY = "sk-0c7489587"
AZURE_API_KEY = "BVdtDRjC29UejATKda7J4BlJ99AKACYeBjFXJ3w3AAABACOGL10p"
AZURE_ENDPOINT = "https://oai-nasco.openai.azure.com/"
AZURE_DEPLOYMENT_NAME = "gpt-4o"    
# --- Load and Display Logo ---
try:
    logo_path = r"D:\Sea_route_analyzer\images\Auagentphoto.png" 
    logo = Image.open(logo_path)
    st.image(logo, width=200) 
except FileNotFoundError:
    st.error(f"Error: Logo image not found at path: {logo_path}. Please ensure the path is correct or place the logo in the same folder as app.py.")
except Exception as e:
    st.error(f"An error occurred loading the logo: {e}")


# --- Helper Functions ---
@st.cache_data
def fetch_major_news(api_key):
    """Searches NewsAPI.org for the latest major maritime-related crises. This function is cached."""
    query = ('("maritime crisis" OR "shipping disruption" OR "geopolitical trade" OR "suez canal" OR "strait of hormuz" OR "port strike" OR "sanctions") AND (impact OR crisis OR tension)')
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&pageSize=7&sortBy=publishedAt&apiKey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('articles', [])
    except Exception as e:
        st.error(f"Error fetching news from NewsAPI.org: {e}. Check your API Key.")
        return []

def get_deep_dive_analysis(_article_content, provider):
    """Uses AI to perform a comprehensive analysis of a single news article."""
    prompt = f"""
    Act as the Head of Global Supply Chain Intelligence. Analyze the following news article to produce a definitive intelligence report.
    Your entire response must be in English.

    ARTICLE:
    {_article_content}

    Provide your response ONLY in the following valid JSON format:
    {{
      "EventTitle": "A concise title for the event from the article.",
      "EventSummary": "A 2-3 sentence summary of the core event and its significance.",
      "ImpactedCountries": [
        {{
          "Country": "Name of an impacted country.",
          "ImpactDetails": "How this country is specifically affected (e.g., 'Faces major export delays due to port closures', 'Import costs for energy are expected to rise.')."
        }}
      ],
      "ImpactedPorts": [
        {{
          "Port": "Name of the major port mentioned or implicated.",
          "PortNationalImportance_Est_Percent": "<integer, your best estimate of this port's percentage of its country's total maritime trade>",
          "ImpactOnPort": "How port operations are affected (e.g., 'Severe congestion expected', 'Operations halted', 'High-risk area for insurance')."
        }}
      ],
      "CommodityImpact": [
        {{
          "Commodity": "Name of the commodity/product (e.g., Crude Oil, Electronics, Wheat, Automotive Parts).",
          "Effect": "Price Hike | Potential Shortage | Significant Shipping Delay"
        }}
      ],
      "AffectedSeaRoutes": ["List of affected sea routes (e.g., 'Asia-Europe via Suez Canal')."]
    }}
    """
    try:
        if provider == "Azure OpenAI":
            client = AzureOpenAI(api_key=AZURE_API_KEY, api_version="2024-02-15-preview", azure_endpoint=AZURE_ENDPOINT)
            response = client.chat.completions.create(model=AZURE_DEPLOYMENT_NAME, response_format={"type": "json_object"}, messages=[{"role": "system", "content": "You are a Head of Supply Chain Intelligence."}, {"role": "user", "content": prompt}])
            return json.loads(response.choices[0].message.content)
        elif provider == "DeepSeek":
            client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com/v1")
            response = client.chat.completions.create(model="deepseek-chat", response_format={"type": "json_object"}, messages=[{"role": "system", "content": "You are a Head of Supply Chain Intelligence."}, {"role": "user", "content": prompt}])
            return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"Error during AI deep-dive analysis: {e}")
        return None

# --- Streamlit UI ---
st.title("📡 Interactive Maritime Intelligence Center") 
st.markdown("This dynamic tool scans major world news, allows you to select a key event, and provides an instant AI-powered deep-dive analysis of its impact on global trade.")

# Initialize session state
if 'articles' not in st.session_state:
    st.session_state.articles = []
if 'analysis_cache' not in st.session_state:
    st.session_state.analysis_cache = {}

# --- Step 1: Fetch News ---
st.markdown("---")
col1, col2 = st.columns([1, 2])
with col1:
    llm_provider = st.selectbox("Select AI Provider", ["DeepSeek", "Azure OpenAI"])
with col2:
    if st.button("📰 Step 1: Fetch Major Maritime News", use_container_width=True):
        with st.spinner("Scanning for major global maritime news..."):
            st.session_state.articles = fetch_major_news(NEWSAPI_KEY)
            st.session_state.analysis_cache = {} # Clear the cache
            if not st.session_state.articles:
                st.warning("No major crisis news found at this time. The global situation appears stable.")
            st.rerun() # Rerun to update the radio button with new articles

# --- Step 2: Select News and Analyze ---
if st.session_state.articles:
    st.markdown("---")
    st.subheader("📰 Step 2: Select a News Headline for Deep-Dive Analysis")
    
    article_titles = [article['title'] for article in st.session_state.articles]
    selected_title = st.radio("Select an event to analyze:", article_titles, key="article_selector")

    analysis = None
    if selected_title:
        # Check our manual cache first
        if selected_title in st.session_state.analysis_cache:
            analysis = st.session_state.analysis_cache[selected_title]
        else:
            # If not in cache, run the analysis
            with st.spinner(f"Performing AI deep-dive analysis on '{selected_title}'..."):
                selected_article = next((article for article in st.session_state.articles if article['title'] == selected_title), None)
                if selected_article and selected_article.get('content'):
                    analysis = get_deep_dive_analysis(selected_article['content'], llm_provider)
                    # Save the new result to our cache
                    st.session_state.analysis_cache[selected_title] = analysis
                else:
                    st.warning("Could not find content for the selected article to analyze.")
        
        # --- Display the report ---
        if analysis:
            st.markdown("---")
            st.header(f"Deep-Dive Report: {analysis.get('EventTitle', 'N/A')}")
            st.info(f"**Event Summary:** {analysis.get('EventSummary', 'N/A')}")
            
            tab1, tab2, tab3 = st.tabs(["🌍 Country & Port Impact", "📦 Commodity Impact", "🗺️ Route Impact"])

            with tab1:
                st.subheader("Affected Countries")
                country_impacts = analysis.get('ImpactedCountries', [])
                if country_impacts:
                    for country in country_impacts:
                        st.markdown(f"**- {country.get('Country')}:** {country.get('ImpactDetails')}")
                else: st.markdown("No specific countries identified.")
                
                st.subheader("Affected Ports")
                port_impacts = analysis.get('ImpactedPorts', [])
                if port_impacts: st.table(pd.DataFrame(port_impacts))
                else: st.markdown("No specific ports identified.")

            with tab2:
                st.subheader("Impact on Commodities & Goods")
                commodity_impacts = analysis.get('CommodityImpact', [])
                if commodity_impacts: st.table(pd.DataFrame(commodity_impacts))
                else: st.markdown("No specific commodity impacts identified.")

            with tab3:
                st.subheader("Affected Sea Routes")
                routes = analysis.get('AffectedSeaRoutes', [])
                if routes: st.markdown("\n".join([f"- {route}" for route in routes]))
                else: st.markdown("No specific sea routes identified.")
else:
    st.info("Click 'Fetch Major Maritime News' to begin.")