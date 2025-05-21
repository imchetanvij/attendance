import streamlit as st
import requests
import pandas as pd


# 🔧 Replace this with your actual Web App URL
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzgx96l-aK3d55jnVLxaFTwp8wTObnwQxg27M9cg_jVTbT0CSaeeq65NBN_0rB50dsD/exec"  # replace with your deployed URL

# Load picture descriptions (can come from a Google Sheet or local dict)
picture_options = {
    "A1P1":"A1P1: Lines, Shapes & Forms Drawing",
"A1P2":"A1P2: Objects & Animals Drawing",
"A1P3":"A1P3: Still Life Composition & Drawing",
"A1P4":"A1P4: Landscape Composition & Drawing",
"A1P5":"A1P5: Observation Drawing",
"A1P6":"A1P6: Perspectrive Drawing (Intro)",
"A1P7":"A1P7: Shading Technique 1",
"A1P8":"A1P8: Shading Technique 2",
"A1P9":"A1P9: Shading Technique 3",
"A1P10":"A1P10: Still Life Illustraion",
"A1P11":"A1P11: Landscape Illustration",
"A1P12":"A1P12: Townscape Illustration",
"A1P13":"A1P13: Sketch, Draw & Shade (Human 1)",
"A1P14":"A1P14: Sketch, Draw & Shade (Human 2)",
"A1P15":"A1P15: Shading Illustration 1(Animal)",
"A1P16":"A1P16: Shading Illustration 1(Human)",
"A1Assessment":"A1Assessment: Advance Level 1 Assessment",
"A1AssessmentCOMPLETED":"A1Assessment: Advance Level 1 Assessment COMPLETED",
"A1QuarterlyCraft":"A1Assessment: Advance Level 1 Quarterly Craft",
"A2P1":"A2P1: Material Handling & Intro on PCT1(Poster Color Technique)",
"A2P2":"A2P2: Color Wheel/Schemes & Application of PCT1",
"A2P3":"A2P3: Intro to Coloring Techniques2, Application of PCT 1 and PCT2",
"A2P4":"A2P4: Illustration Painting 1 PCT2",
"A2P5":"A2P5: Illustration Painting 2 PCT2",
"A2P6":"A2P6: Illustration Painting 3 PCT2",
"A2P7":"A2P7: Illustration Painting 4 PCT2",
"A2P8":"A2P8: Material Handling & Intro on WCT1",
"A2P9":"A2P9: Illustration Painting 1 WCT1",
"A2P10":"A2P10: Illustration Painting 2 WCT1",
"A2P11":"A2P11: Illustration Painting 3 WCT1",
"A2P12":"A2P12: Illustration Painting 4 WCT1",
"A2Assessment":"A2Assessment: Advance Level 2 Assessment",
"A2AssessmentCOMPLETED":"A2Assessment: Advance Level 2 Assessment COMPLETED",
"A3P1":"A3P1: Still Life Illustraion",
"A2QuarterlyCraft":"A2Assessment: Advance Level 2  Quarterly Craft",
"A3P2":"A3P2: Life Illustration",
"A3P3":"A3P3: Creative Text Development",
"A3P4":"A3P4: Metaphorical Illustration",
"A3P5":"A3P5: Advertisement Illustration",
"A3P6":"A3P6: Poster Illustration 1 ( Wildlife Conservation)",
"A3P7":"A3P7: Poster Illustration 2 ( Social & Environment )",
"A3P8":"A3P8: Poster Illustration 3 ( Sports )",
"A3P9":"A3P9: Poster Illustration 4 ( Festivity )",
"A3P10":"A3P10: Poster Illustration 5 ( Wonders Of The World )",
"A3P11":"A3P11: Poster Illustration 6 ( Sci-Fi Movie Modern",
"A3P12":"A3P12: Poster Illustration 7 ( Fantasy/Folklore )",
"A3Assessment":"A3Assessment: Advance Level 3 Assessment",
"A3AssessmentCOMPLETED":"A3Assessment: Advance Level 3 Assessment COMPLETED",
"A3QuarterlyCraft":"A3Assessment: Advance Level 3  Quarterly Craft",
"B1P1":"B1P1: Apple",
"B1P2":"B1P2: Mangosteen",
"B1P3":"B1P3: Watermelon",
"B1P4":"B1P4: Duck",
"B1P5":"B1P5: Orange",
"B1P6":"B1P6: Hornbill",
"B1P7":"B1P7: Dolphin",
"B1P8":"B1P8: Cow",
"B1Assessment":"B1Assessment: Basic Level 1 Assessment",
"B1AssessmentCOMPLETED":"B1Assessment: Basic Level 1 Assessment COMPLETED",
"B1Techniques":"B1Techniques: ",
"B1QuarterlyCraft":"B1QuarterlyCraft : Basic Level 1 Quarterly Craft",
"B2P1":"B2P1: Hen",
"B2P2":"B2P2: Turtle",
"B2P3":"B2P3: Elephant",
"B2P4":"B2P4: Lion",
"B2P5":"B2P5: Shark",
"B2P6":"B2P6: Orangutan",
"B2P7":"B2P7: Panda",
"B2P8":"B2P8: Giraffe",
"B2Assessment":"B2Assessment: Basic Level 2 Assessment",
"B2AssessmentCOMPLETED":"B2Assessment: Basic Level 2 Assessment COMPLETED",
"B2Techniques":"B2Techniques: ",
"B2QuarterlyCraft":"B2QuarterlyCraft : Basic Level 2 Quarterly Craft",
"B3P1":"B3P1: Head, Hair & Face (front)",
"B3P2":"B3P2: Illustration (Head, Hair & Face (front))",
"B3P3":"B3P3: Head, Hair & Face (side & back)",
"B3P4":"B3P4: llustration Head, Hair & Face (side & back)",
"B3P5":"B3P5: Hands (Gestures, Angles & Illustration)",
"B3P6":"B3P6: Feet (Gestures, Angles & Illustration)",
"B3P7":"B3P7: Sports ( Illustration)",
"B3P8":"B3P8: Mixed Activities (Illustration)",
"B3Assessment":"B3Assessment: Basic Level 3 Assessment",
"B3AssessmentCOMPLETED":"B3Assessment: Basic Level 3 Assessment COMPLETED",
"B3Techniques":"B3Techniques: ",
"B3QuarterlyCraft":"B3QuarterlyCraft : Basic Level 3 Quarterly Craft",
"F1P1":"F1P1: The Moon & the Stars",
"F1P2":"F1P2: My Lovely House",
"F1P3":"F1P3: Walrus in the Arctic",
"F1P4":"F1P4: The Big Fish",
"F1P5":"F1P5: (HW) The Mother Duck",
"F1P6":"F1P6: Natural Landscape",
"F1P7":"F1P7: The Garden Bird",
"F1P8":"F1P8: The Funny Sun",
"F1P9":"F1P9: I Am A Pilot",
"F1P10":"F1P10: (HW) Lets Surf",
"F1Assessment":"F1Assessment: Foundation Level 1 Assessment",
"F1AssessmentCOMPLETED":"F1Assessment: Foundation Level 1 Assessment COMPLETED",
"F1Techniques":"F1Techniques: Distinguish Dark and Light Colors, Outline, Shading, One direction Coloring, Adding Objects",
"F1QuarterlyCraft":"F1QuarterlyCraft : Foundation Level 1 Quarterly Craft",
"F2P1":"F2P1: Jump Rabbit Jump",
"F2P2":"F2P2: The Clipping Crab",
"F2P3":"F2P3: The Juggling Sea Lion",
"F2P4":"F2P4: Fun Chicky Chick",
"F2P5":"F2P5: The Mother Hen",
"F2P6":"F2P6: Mangosteen or Water Apple",
"F2P7":"F2P7: Badminton or Tennis",
"F2P8":"F2P8: The Playful Fish",
"F2P9":"F2P9: Let's feed the Sheep",
"F2P10":"F2P10: Riding in My Car",
"F2Assessment":"F2Assessment: Foundation Level 2 Assessment",
"F2AssessmentCOMPLETED":"F2Assessment: Foundation Level 2 Assessment COMPLETED",
"F2Techniques":"F2Techniques: Distinguish Dark and Light Colors, Outline, Shading, One direction Coloring, Adding Objects, Two Color Shading",
"F2QuarterlyCraft":"F2QuarterlyCraft : Foundation Level 2 Quarterly Craft",
"F3P1":"F3P1: My Favourite Vegetables",
"F3P2":"F3P2: The Hungry Lion",
"F3P3":"F3P3: Happy Easter Day",
"F3P4":"F3P4: The Amazing Octopus",
"F3P5":"F3P5: The Little Ladybird",
"F3P6":"F3P6: The Mother Eagle",
"F3P7":"F3P7: The Magical Clown",
"F3P8":"F3P8: Let's Build a Sandcastle",
"F3P9":"F3P9: My Favourite Fruits",
"F3P10":"F3P10: The Strong Elephant",
"F3Assessment":"F3Assessment: Foundation Level 3 Assessment",
"F3AssessmentCOMPLETED":"F3Assessment: Foundation Level 3 Assessment COMPLETED",
"F3Techniques":"F3Techniques: Distinguish Dark and Light Colors, Outline, Shading, One direction Coloring, Adding Objects, Three Color Shading",
"F3QuarterlyCraft":"F3QuarterlyCraft : Foundation Level 3 Quarterly Craft",
"I4P1":"I4P1: School,Classroom, construction",
"I4P2":"I4P2: Cooking, Restaurant, Kitchen",
"I4P3":"I4P3: Sports (TT, Bowling, Badminton, Discuss throw)",
"I4P4":"I4P4: Scuba diving, Fishing",
"I4P5":"I4P5: Kite flying",
"I4P6":"I4P6: Farming",
"I4P7":"I4P7: Rainiy Season",
"I4P8":"I4P8: Exercise, Walking, Boxing",
"I4Assessment":"I4Assessment: Intermediate Level 4 Assessment",
"I4AssessmentCOMPLETED":"I4Assessment: Intermediate Level 4 Assessment COMPLETED",
"I4Techniques":"I4Techniques: ",
"I4QuarterlyCraft":"I4QuarterlyCraft : INTERMEDIATE Level 4 Quarterly Craft",
"I5P1":"I5P1: Fishing",
"I5P2":"I5P2: Sports, Goal Saving, Basket Ball, Hockey and Rugby",
"I5P3":"I5P3: Water Sports",
"I5P4":"I5P4: Picnic",
"I5P5":"I5P5: Cleaning up",
"I5P6":"I5P6: Sports, Athletics",
"I5P7":"I5P7: Boat race",
"I5P8":"I5P8: Zoo with Giraffee, Jeep Seal and a photographer",
"I5Assessment":"I5Assessment: Intermediate Level 5 Assessment",
"I5AssessmentCOMPLETED":"I5Assessment: Intermediate Level 5 Assessment COMPLETED",
"I5Techniques":"I5Techniques: ",
"I5QuarterlyCraft":"I5QuarterlyCraft : INTERMEDIATE Level 5 Quarterly Craft",
"I6P1":"I6P1: Fish and Vegetable market",
"I6P2":"I6P2: Circus, Magic carnival performance",
"I6P3":"I6P3: Fire fighting",
"I6P4":"I6P4: Bus, bike, traffic police lady shopping",
"I6P5":"I6P5: Festivals",
"I6P6":"I6P6: Seasons",
"I6P7":"I6P7: Space",
"I6P8":"I6P8: Twin towers, United we stand(religions)",
"I6Assessment":"I6Assessment: Intermediate Level 6 Assessment",
"I6AssessmentCOMPLETED":"I6Assessment: Intermediate Level 6 Assessment COMPLETED",
"I6Techniques":"I6Techniques: ",
"I6QuarterlyCraft":"I6QuarterlyCraft : INTERMEDIATE Level 6 Quarterly Craft",
"JP1":"JP1: ",
"JP2":"JP2: ",
"JP3":"JP3: ",
"JP4":"JP4: ",
"JP5":"JP5: ",
"JP6":"JP6: ",
"JP7":"JP7: ",
"JP8":"JP8: ",
"JP9":"JP9: ",
"JP10":"JP10: ",
"PBTechniques":"PBTechniques: Introduction to Color Families, Teeth To Teeth, Outlining",
"JuniorQuarterlyCraft":"JuniorQuarterlyCraft : JUNIOR Level  Quarterly Craft",
"PBAssessment":"PBAssessment: Pre Basic Assessment",
"PBAssessmentCOMPLETED":"PBAssessment: Pre Basic Assessment COMPLETED",
"PB1":"PB1: GRID DRAWING SQUIRREL",
"PB2":"PB2: GRID DRAWING PENGUIN",
"PB3":"PB3: LINES, SHAPES & FORMS : CAT AND OBJECTS",
"PB4":"PB4: LINES, SHAPES AND FORMS : MARINE ANIMALS",
"PB5":"PB5: DIRECTION LEFT AND RIGHT CHAMELEON",
"PB6":"PB6: DIRECTION LEFT RIGHT AND FRONT PEOPLE",
"PB7":"PB7: OVERLAP FRONT MIDDLE AND BACK STILL LIFE TOYS",
"PB8":"PB8: OVERLAP FRONT MIDDLE AND BACK CLOWN FISH",
"PB9":"PB9: CROPPING LEFT RIGHT TOP AND BOTTOM MARINE LIFE",
"PB10":"PB10: CROPPING LEFT RIGHT TOP AND BOTTOM FARM LIFE",
"PBQuarterlyCraft":"PBQuarterlyCraft : PRE BASIC Level  Quarterly Craft",
"PREINTERMEDIATEP1":"PREINTERMEDIATE Pict 1",
"PREINTERMEDIATEP2":"PREINTERMEDIATE Pict 2",
"PREINTERMEDIATEP3":"PREINTERMEDIATE Pict 3",
"PREINTERMEDIATEP4":"PREINTERMEDIATE Pict 4",
"PREINTERMEDIATEP5":"PREINTERMEDIATE Pict 5",
"PREINTERMEDIATEP6":"PREINTERMEDIATE Pict 6",
"PREINTERMEDIATEP7":"PREINTERMEDIATE Pict 7",
"PREINTERMEDIATEP8":"PREINTERMEDIATE Pict 8",
"PREINTERMEDIATEAssessment":"PREINTERMEDIATE Assessment",
"PREINTERMEDIATEAssessmentCOMPLETED":"PREINTERMEDIATE Assessment COMPLETED",
"PREINTERMEDIATETechniques":"PREINTERMEDIATE Techniques",
"PREINTERMEDIATEQuarterlyCraft":"PREINTERMEDIATE Quarterly Craft"
}




def fetch_data():
    response = requests.get(WEB_APP_URL)
    response.raise_for_status()
    data = response.json()
    #print(response.json())
    st.subheader("Raw JSON from Web App:")
st.json(response.json())

    return pd.DataFrame(data)

#def expand_data_column(df):
    # Expand the 'data' dict column into separate columns
#    data_expanded = pd.json_normalize(df['data'])
#    df_expanded = pd.concat([df.drop(columns=['data']), data_expanded], axis=1)
#    return df_expanded

#def expand_data_column(df):
#    if 'data' in df.columns:
#        data_expanded = df['data'].apply(lambda x: pd.Series(x) if isinstance(x, dict) else {})
#        df = pd.concat([df.drop(columns=['data']), data_expanded], axis=1)
#    return df


def post_updates(updated_rows):
    # Send updated rows back to the App Script POST endpoint
    # Payload format may vary depending on your app script
    payload = {"updates": updated_rows}
    response = requests.post(WEB_APP_URL, json=payload)
    response.raise_for_status()
    return response.json()

def main():
    st.title("Teacher Attendance Interface")

    # Replace this with actual logged-in teacher CI
    logged_in_ci = st.text_input("Enter your CI (teacher ID) for testing:")

    if not logged_in_ci:
        st.info("Please enter your CI to see your data.")
        return

    # Fetch data
    df_raw = fetch_data()
    st.write("Raw fetched data:", df_raw)


    # Expand nested data
    #df = expand_data_column(df_raw)
    df = df_raw
    st.write("Raw fetched data Expanded:", df)

    # Filter rows by logged-in teacher CI
    df = df[df['CI'] == logged_in_ci]

    if df.empty:
        st.warning("No data found for your CI.")
        return

    # Prepare a list to collect updates
    updated_rows = []

    # Show data and editable fields
    st.write(f"Showing {len(df)} records for CI = {logged_in_ci}")

    for idx, row in df.iterrows():
        st.markdown("---")
        st.write(f"**RowKey:** {row['RowKey']} | **Date:** {row.get('DATE', 'N/A')} | **Slot:** {row.get('SLOT', 'N/A')}")

        # Show all fields in read-only except WORK DONE IN THE CLASS and REMARKS
        for col in df.columns:
            if col in ['RowKey', 'CI', 'WORK DONE IN THE CLASS', 'REMARKS', 'data']:
                continue
            st.write(f"{col}: {row.get(col, '')}")

        # Editable fields
        work_done = st.selectbox(
            "WORK DONE IN THE CLASS",
            options=picture_options,
            #index=picture_options.index(row.get('WORK DONE IN THE CLASS')) if row.get('WORK DONE IN THE CLASS') in picture_options else 0,
            index = list(picture_options.keys()).index(row.get('WORK DONE IN THE CLASS')) if row.get('WORK DONE IN THE CLASS') in picture_options else 0,

            key=f"workdone_{idx}"
        )
        remarks = st.text_area(
            "REMARKS",
            value=row.get('REMARKS', ''),
            key=f"remarks_{idx}",
            height=80
        )

        # Store updated row data
        updated_row = {
            "RowKey": row['RowKey'],
            "WORK DONE IN THE CLASS": work_done,
            "REMARKS": remarks,
        }
        updated_rows.append(updated_row)

    # Submit button
    if st.button("Submit Updates"):
        # Prepare payload for only updated rows with full original row keys
        response = post_updates(updated_rows)
        st.success("Updates sent successfully!")
        st.json(response)

if __name__ == "__main__":
    main()
