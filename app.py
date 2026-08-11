import streamlit as st
import pandas as pd
import io

# --- Configure the Page ---
st.set_page_config(page_title="SKU Categorizer", layout="centered")
st.title("📦 Keyword Inventory Categorizer")
st.write("This app categorizes SKUs using keyword matching (No API required).")

# --- The Keyword Rules Dictionary ---
# You can easily add more words to this list!
CATEGORY_RULES = {
    'Pretend Play': {
        'Kitchen & Food': ['kitchen', 'food', 'cooking', 'chef', 'microwave'],
        'Doctor Playsets': ['doctor', 'nurse', 'medical', 'stethoscope'],
        'Tools': ['tool', 'drill', 'hammer', 'workbench']
    },
    'Sports & Outdoor Play': {
        'Pool Toys and Games': ['pool', 'inflatable', 'swim', 'water slide'],
        'Trampolines': ['trampoline', 'bounce'],
        'Play Tents & Tunnels': ['tent', 'tunnel']
    },
    'Puzzles': {
        'Jigsaw Puzzles': ['jigsaw', '1000 piece', '500 piece'],
        'Brain Teasers': ['rubik', 'brain teaser', 'logic']
    },
    'Baby & Toddler Toys': {
        'Bath Toys': ['bath', 'rubber duck', 'water toy'],
        'Blocks': ['lego', 'mega bloks', 'building block']
    }
}

def categorize_sku(title):
    """Checks the SKU title against our keyword rules."""
    title_lower = str(title).lower()
    
    # First, check for obvious non-toys
    if any(word in title_lower for word in ['adult', 'shirt', 'bottle', 'diaper']):
        return pd.Series(['(Not Toy)', '(Not Toy)'])

    # Search through our dictionary for a match
    for main_type, subtypes in CATEGORY_RULES.items():
        for subtype, keywords in subtypes.items():
            if any(keyword in title_lower for keyword in keywords):
                return pd.Series([main_type, subtype])
                
    # If no keywords match at all
    return pd.Series(['Uncategorized', 'Uncategorized'])

# --- App UI ---
sku_input = st.text_area("Enter SKUs (one per line):", height=200)

if st.button("Categorize SKUs"):
    if not sku_input.strip():
        st.warning("Please enter some SKUs first.")
    else:
        # Convert the pasted text into a list
        sku_list = [sku.strip() for sku in sku_input.split('\n') if sku.strip()]
        df = pd.DataFrame(sku_list, columns=['Title'])
        
        # Apply our keyword logic
        df[['Type', 'Subtype']] = df['Title'].apply(categorize_sku)
        
        # Display the result
        st.success("Categorization Complete!")
        st.dataframe(df, use_container_width=True)
        
        # Download Button
        csv_export = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv_export,
            file_name='categorized_skus.csv',
            mime='text/csv',
        )
