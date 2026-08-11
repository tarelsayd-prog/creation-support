import streamlit as st
import google.generativeai as genai
import pandas as pd
import io

# --- Configure the Page ---
st.set_page_config(page_title="SKU Categorizer & Describer", layout="centered")
st.title("📦 AI Inventory Categorizer (Multilingual)")

# --- API Key Setup ---
api_key = st.secrets.get("GEMINI_API_KEY", "")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.warning("Please add your GEMINI_API_KEY to the Streamlit secrets.")

# --- The Master Prompt ---
MASTER_PROMPT = """
Please act as an expert inventory categorizer, e-commerce copywriter, and professional English-to-Arabic translator. I will provide you with a list of SKUs. 
You must organize them into a CSV format with EXACTLY the following 11 columns: 
Title, Type, Subtype, Description_EN, Description_AR, Feature_Bullet_1_EN, Feature_Bullet_1_AR, Feature_Bullet_2_EN, Feature_Bullet_2_AR, Feature_Bullet_3_EN, Feature_Bullet_3_AR

Rules:
1. Strictly use only the Types and Subtypes listed below.
2. If an item is not a toy (e.g., adult apparel, baby feeding bottles), leave the Type and Subtype columns with the keyword (Not Toy).
3. Description_EN: Write a powerful and catchy one-paragraph product description suitable for an e-commerce platform based on the Title.
4. Description_AR: Write a natural, highly engaging Arabic translation of that e-commerce product description.
5. Feature_Bullet_1_EN, Feature_Bullet_2_EN, Feature_Bullet_3_EN: Write three distinct, compelling key features/benefits for the product in English.
6. Feature_Bullet_1_AR, Feature_Bullet_2_AR, Feature_Bullet_3_AR: Provide accurate and professional Arabic translations for the three feature bullets.
7. CRITICAL: Return ONLY valid CSV data. Do not include markdown formatting, explanations, or any other text. You MUST enclose any text containing commas, newlines, or special characters in double quotes ("") so that it does not break the CSV layout.

Types and Subtypes:
- Pretend Play: Beauty Playsets, Tools, Magnet & Felt Playboards, Shops & Accessories, Money & Banking, Doctor Playsets, Household Toys, Kitchen & Food
- Sports & Outdoor Play: Inflatable Pool Ride On, Pool Toys and Games, Trampolines, Playhouses, Baby Floats & Float Suits, Sand & Water Tables, Sports, Balls, Pools, Gym Sets & Swings, Blasters & Foam Play, Beanbags & Foot Bags, Play Tents & Tunnels, Boats, Kites & Wind Spinners, Beach Toys, Bubbles, Pool Covers & Accessories, Kickball & Playground Balls, Swim Ring, Rafts, Yo-yos, Lawn Games, Fitness Equipment, Water Slides, Ball Pits and Accessories, Play Sets & Playground Equipment, Inflatable Bouncers, Water Blasters & Soakers
- Hobbies: Models & Model Kits, RC Helicopters, RC Motorcycles, RC Cars & Trucks, RC Ships & Submarines, Slot Cars Race Tracks & Accessories, Hobby RC Vehicles & Parts, Stamp Collecting, RC Trains, RC Quadcopters, Scaled Model Vehicles, RC Vehicles & Parts, Trains & Accessories, Radio Control, RC Animals & Robots, Model Building Kits & Tools, Hobby Building Tools & Hardware, Coin Collecting, RC Airplanes
- Figures & Statues: Accessories, Statues & Bobbleheads, Action Figures, Playsets, Animal Figures
- Toy Play Vehicles: Vehicle Playsets, Trains & Railway Sets, RC Vehicles & Batteries, Play Vehicles, Die-cast Vehicles, Race Tracks
- Puzzles: Brain Teasers, Jigsaw Puzzles, Floor Puzzles, Pegged Puzzles, 3D Puzzles
- Arts & Crafts: Printing & Stamping, Craft Kits, Easels, Drawing & Painting Supplies, Beads, Stickers, Blackboards & Whiteboards, Clay & Dough
- Learning & Education: Early Development Toys, Mathematics & Counting, Solar, Flash Cards, Reading & Writing, Geography, Basic & Life Skills Toys, Musical Instruments, Science, Electronics
- Tricycles, Scooters & Wagons: Skates, Skateboards, Kids Bikes, Kids Helmets, Ride-on Toys, Kids Kick Scooter, Kids Scooter Parts & Accessories, Kids Protective Gear, Electric Ride ons, Tricycles, Kids Hoverboard, Kids Drift Scooter, Bike Accessories
- Baby & Toddler Toys: Activity Centers, Music & Sound, Stacking & Nesting Toys, Shape Sorters, Hammering & Pounding Toys, Baby Gyms & Playmats, Push & Pull Toys, Bath Toys, Indoor Climbers & Play Structures, Blocks, Crib Toys & Attachments, Rocking & Spring Ride-ons, Car Seat & Stroller Toys, Rattles, Stuffed Animals & Toys
- Party Supplies: Party Packs, Candles, Party Tableware, Cake Supplies, Party Games & Crafts, Balloons, Pinatas, Tablecovers & Centerpieces, Holi Colour, Party Hats, Banners Streamers & Confetti, Noisemakers, Invitations & Cards, Party Favors
- Stuffed Animals & Plush: Plush Backpacks & Purses, Teddy Bears, Plush Pillows, Plush Puppets, Puppets, Animals & Figures
- Dressing Up & Costumes: Costumes, Costume Accessories
- Dolls & Accessories: Playsets & Figures, Dollhouses, Soft Dolls, Doll Accessories, Baby Dolls, Dollhouse Accessories, Fashion Dolls
- Building Toys: Building Sets, Stacking Blocks
- Novelty Toys: Squishy toys, Slime & Putty Toys, Nesting Dolls, Miniatures, Finger Boards & Finger Bikes, Viewfinders, Prisms & Kaleidoscopes, Wind-Up Toys, Gag Toys & Practical Jokes, Fidget Spinners, Pop Bubble Fidget, Magic Kits & Accessories, Money Banks, Light-Up Toys, Magnets & Magnetic Toys, Temporary Tattoos, Shaped Rubber Wristbands, Toy Balls
- Games: Handheld Games, Standard Playing Card Decks, Dice & Gaming Dice, Board Games, Game Accessories, Card Games, Trading Cards, Battling Tops
- Electronics For Kids: Plug & Play Video Games, Music Players & Karaoke, Electronic Pets, Rc Figures & Robots, Electronic Toys, Cameras & Camcorders

Here is the list of SKUs to process:
"""

# --- App UI ---
st.write("Paste your list of SKUs below. The AI will categorize them and generate English/Arabic descriptions and feature bullets.")

sku_input = st.text_area("Enter SKUs (one per line):", height=200)

if st.button("Categorize & Describe SKUs"):
    if not sku_input.strip():
        st.warning("Please enter some SKUs first.")
    else:
        with st.spinner("Processing... generating categories, descriptions, and Arabic translations!"):
            try:
                # Using the latest model you successfully set up
                model = genai.GenerativeModel('gemini-3.5-flash-lite')
                response = model.generate_content(MASTER_PROMPT + "\n" + sku_input)
                
                # Parse the CSV response into a Pandas DataFrame
                csv_data = io.StringIO(response.text.strip())
                df = pd.read_csv(csv_data)
                
                # Display the table
                st.success("Processing Complete!")
                st.dataframe(df, use_container_width=True)
                
                # Allow user to download the table
                csv_export = df.to_csv(index=False).encode('utf-8-sig') # Added utf-8-sig so Excel reads Arabic correctly
                st.download_button(
                    label="Download Data as CSV",
                    data=csv_export,
                    file_name='multilingual_skus.csv',
                    mime='text/csv',
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")
