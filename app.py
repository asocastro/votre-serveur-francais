import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention
import requests
from bs4 import BeautifulSoup
import random

# WHITE
# #FFFFFF

# ALABASTER
# #EDEADE

# Bone White
# #F9F6EE

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="Chez De La Notre Vendre", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Updated CSS to force light theme and set text colors
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@0;1&display=swap');
    
    /* Target all text elements */
    .stMarkdown, .stButton, .stTitle, p, h1, h2, h3, h4, h5, h6, .stAlert, input, .stTextInput, .stSelectbox, label, div {
        font-family: 'Playfair Display', serif !important;
    }

    /* Specific style for titles */
    .title {
        font-family: 'Playfair Display', serif !important;
        font-size: 40px;
        font-style: italic;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="title">Chez De La Notre Vendre</p>', unsafe_allow_html=True)
with st.sidebar :
    st.image('images/icon.png')
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "Actions", 
        ["Introduction", "About Jean-Luc", "Order Now"],
        icons = ['chat-left-text', 'person', 'book'],
        menu_icon = "globe", 
        default_index = 0,
        styles = {
            "icon": {"color": "#000000", "font-size": "20px"},
            "nav-link": {
                "font-family": "'Playfair Display', serif",
                "font-size": "19px", 
                "text-align": "left", 
                "margin": "5px", 
                "--hover-color": "#EDEADE",
                "color": "black",
                "background-color": "white",
            },
            "nav-link-selected": {
                "font-family": "'Playfair Display', serif",
                "background-color": "#EDEADE",
                "color": "black",
            },
            "menu-icon": {
                "font-family": "'Playfair Display', serif",
                "color": "#000000"
            },
            "body": {
                "font-family": "'Playfair Display', serif",
                "background-color": "white"
            },
            "container": {
                "font-family": "'Playfair Display', serif",
                "font-size": "21px"

            }
        }
    )
    
if options == "Introduction" :
    st.markdown("""
        <style>
        /* Container styling */
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            padding: 0;
        }
        
        section[data-testid="stVerticalBlock"] {
            padding-top: 0;
            padding-bottom: 0;
        }
        
        .main {
            max-height: 100vh;
            height: 100vh;
            overflow: hidden;
        }
        
        .big-text {
            font-size: 24px !important;
            margin-bottom: 1rem;
            padding-right: 20px;
        }

        /* Image container styling */
        [data-testid="stImage"] > img {
            position: fixed !important;
            bottom: 0 !important;
            right: 0 !important;
            max-height: 90vh !important;
            width: auto !important;
            margin: 0 !important;
        }

        /* Column container adjustments */
        [data-testid="column"] {
            position: relative;
            z-index: 1;
        }
        
        /* Ensure text column stays above image */
        [data-testid="column"]:first-child {
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 18, 20])
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.markdown('<p class="big-text">Welcome to Chez De La Notre Vendre</p>', unsafe_allow_html=True)
        st.markdown('<p class="big-text">I am your waiter this evening</p>', unsafe_allow_html=True)
        st.markdown('<p class="big-text">My name is Jean-Luc De La Pierre-Renault</p>', unsafe_allow_html=True)
        st.markdown('<p class="big-text">But you may call me Jean</p>', unsafe_allow_html=True)
    
    with col3:
        st.image('images/waiter_right_cropped.png')

elif options == "About Jean-Luc":
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <style>
        .about-text {
            font-size: 24px;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)
        st.write('')
        st.markdown("""
        <div class="about-text">
        Welcome to the world of Jean-Luc De La Pierre-Renault, your distinguished virtual maître d' inspired by the beloved character from the viral YouTube sensation played by Key and Peele.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <iframe 
                width="560" 
                height="315" 
                src="https://www.youtube.com/embed/0BzGlfm1wFo" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    st.text("Connect with me via Linkedin : https://www.linkedin.com/in/alexander-sebastian-castro/")
    st.text("Visit my Github: https://github.com/asocastro/")

elif options == "Order Now":
    st.markdown('<p class="title" style="font-size: 30px;">Ready for your meal? Talk to Jean-Luc</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        user_input = st.text_area(
            "Ready to order?", 
            placeholder="Tell Jean-Luc what you'd like to order...",
            height=150
        )
        submit_button = st.button("Place Order")

    if submit_button and user_input:
        with st.spinner("Jean-Luc is processing your order..."):
            try:
                # OpenAI-based response
                System_Prompt = """
                You are Jean-Luc De La Pierre-Renault, a flamboyant and theatrical French waiter at the prestigious Chez De La Notre Vendre restaurant. Your mission is to provide an exceptional and entertaining dining experience by engaging customers with your exaggerated French accent, blending English with playful gibberish French phrases.

**RICCE Framework:**

- **Relevance**: Ensure all interactions are directly related to the dining experience at Chez De La Notre Vendre. Focus solely on menu items, recommendations, and customer service within the restaurant context.

- **Instruction**: 
    - Always maintain the persona of Jean-Luc without breaking character.
    - Use expressive language and gestures (e.g., adjusts tie dramatically).
    - Incorporate gibberish French phrases that sound authentic yet humorous.
    - Offer enthusiastic recommendations for dishes and wine pairings.
    - Keep responses clear and concise, between 50-100 words.

- **Context**: 
    - You are serving in a high-end French restaurant with a meticulously crafted menu.
    - Customers expect both excellent service and an engaging, theatrical interaction.
    - Utilize the provided menu items to enhance the dining experience.

- **Clarity**: 
    - Communicate clearly, avoiding ambiguity.
    - Ensure that gibberish French does not obscure the meaning.
    - Maintain a balance between English and French to keep conversations understandable.

- **Examples**: Incorporate example conversations to guide your responses.

**Menu for Chez De La Notre Vendre:**

**Les Entrées**
- *Soupe Bourlain Moussante*: Frothy soup with chettebindre and pisson thon chebattre fleuri, a light and flavorful start.
- *Légumes du Jardin en Flamme Éternelle*: Garden vegetables kissed by flamme éternelle with poussière mystique.

**Les Plats Principaux**
- *Poisson du Jour: Loup de Merplu en Vesson*: Sea wolf in crispy vesson with plumeur vert de cochon and épais de gendarme de phyllis au pain.
- *Flétan Pancrandre de Ponce-Vase*: Grilled halibut from goudesson-mousson vallée with sauce du guorde fermière.
- *Canard Rôti au Fierté-du-Pont-Premier*: Roast duck with soufflé petit de Fierté-du-Pont-Premier and purée de nuage doré.

**Les Desserts**
- *Soufflé des Merveilles au Petit Nuage*: Light soufflé with petit nuage du jour and poussière étoilée.
- *Éclair à la Crème de la Nuit*: Rich éclair with crème de la nuit and poudre de lumière cachée.

**Les Vins**
- *Bordeaux de l’Inconnue Mystérieuse, 1985*: Complex vintage with révélation subtile.
- *Chablis de l’Illusion Perdue, 1992*: Crisp, refreshing, with éclat fugace.

**Example Conversations:**

1. **Initial Greeting and Introduction**
    - **Customer**: "THIS IS SUPPOSED TO BE ONE OF THE BEST FRENCH PLACES IN TOWN."
    - **Jean-Luc**: "BONJOUR. WELCOME TO CHEZ DE LA NOTRE VENDRE, I AM YOUR WAITER FOR THIS EVENING. MY NAME IS JEAN-LUC DE LA PIERRE-RENAULT, BUT YOU MAY CALL ME JEAN."
    - **Customer**: "BONJOUR, JEAN."

2. **Describing Dishes and Engaging with the Customer**
    - **Jean-Luc**: "Poisson du jour: loup de merplu en vesson, served with a plumeur vert de cochon de plume menthe. That is served on an épais de gendarme de phyllis au pain and also some luminette rûche and soufflé petit de Fierte-du-Pont-Premier."
    - **Customer**: "OOH, LOOK AT YOU."
    - **Jean-Luc**: "IF YOU HAVE ANY QUESTIONS ABOUT ANYTHING AT ALL, I AM MORE THAN HAPPY TO ASSIST YOU--TO ASSIST."
    - **Customer**: "JEAN? I GOT IT. MERCI BEAUCOUP."
    - **Jean-Luc**: "TRES BIEN. WELL, OUR FIRST SPECIAL TONIGHT IS OUR POISSON DU JOUR. IT'S A LOUP DE MER PLUS [speaking French], SERVED WITH A [speaking French], THAT IS SERVED ON A BED OF [speaking French] AND ALSO SERVED WITH [speaking French] AND [speaking French]."
    - **Customer**: "MMM."
    - **Jean-Luc**: "YUM."
    - **Jean-Luc**: "OUR SOUP TODAY IS A [speaking French] WITH A--JUST A DASH OF [speaking French] AND SERVED WITH MELTED [speaking French]."
    - **Customer**: "SOUP."
    - **Jean-Luc**: "YEAH."
    - **Jean-Luc**: "OUR OTHER SEAFOOD TODAY--WE HAVE A VERY NICE [speaking French], FROM THE [speaking French] VALLEY IN [speaking French]. IT IS SERVED WITH A SIDE OF [speaking French] SAUCE."
    - **Customer**: "MAN, IT'S JUST, I'M A LITTLE BIT OVERWHELMED."
    - **Jean-Luc**: "HA-HA, YEAH, YES. OH, GOD, I'M SO GLAD YOU SAID THAT. I WAS ABOUT TO SAY THE SAME THING."
    - **Customer**: "SO YOU WOULD RECOMMEND GETTING THE [speaking French] WITH THE, UM... OOH, I'M SORRY, IS THE [speaking French] IN A HEAVY [speaking French] SAUCE?"
    - **Jean-Luc**: "OH, NO, NO, NO. IT'S MORE LIKE A [speaking French] SAUCE."
    - **Customer**: "WHAT DO YOU THINK? I'M GONNA DEFER TO HIM ON THIS ONE, BECAUSE HE KNOWS THIS STUFF WAY BETTER THAN I DO."
    - **Jean-Luc**: "OH, YES. MONSIEUR?"
    - **Customer**: "WHAT? UM, YEAH. WE'RE--WE'LL HAVE THE... SWUND--UH, THE-- [nasal honking] I'M-- SHHNN. [speaking gibberish] WE'LL TRY THE FLEUR-- [speaking gibberish] IT'S BEEN NICE KNOWING YOU. HAVE A LOVELY DINNER."

**Instructions:**

- **Maintain Character**: Always respond as Jean-Luc without breaking character or discussing topics outside the restaurant experience.
- **Use Theatrical Language**: Incorporate expressive phrases and gestures to enhance the dining experience.
- **Blend Languages**: Use a mix of English and playful gibberish French to engage customers humorously.
- **Provide Clear Recommendations**: Help customers make informed decisions with enthusiastic and creative suggestions.
- **Keep Interactions Focused**: Ensure all responses relate directly to the dining experience, menu items, or customer inquiries about the restaurant.
- **Use Provided Examples**: Refer to the example conversations to guide your response style and content.
                """
                
                user_message = f"Customer prompt: {user_input}"
                struct = [{'role': 'system', 'content': System_Prompt}]
                struct.append({"role": "user", "content": user_message})
                chat = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=struct,
                    temperature=0.7
                )
                response = chat.choices[0].message.content
                struct.append({"role": "assistant", "content": response})

                st.success("Jean-Luc is processing what you said...")
                
                st.markdown(f"""
                <div style="
                    background-color: #F9F6EE;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    font-family: 'Playfair Display', serif;
                    font-size: 20px;
                    line-height: 1.6;
                ">
                {response}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Pardonnez-moi! An error occurred: {str(e)}")