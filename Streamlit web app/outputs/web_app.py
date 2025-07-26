import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image, ImageDraw

# Add viewport meta tag and CSS for mobile responsiveness
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
    .main {
        padding: 0 !important;
    }
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 300px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 2rem;
        margin-left: -2rem;
    }
    .stCanvas {
        width: 100% !important;
        height: 100% !important;
        max-width: none !important;
        aspect-ratio: 1300/900;
    }
    canvas {
        width: 100% !important;
        height: 100% !important;
        aspect-ratio: 1300/900;
    }
    .canvas-container {
        width: 100% !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    @media (max-width: 768px) {
        .main > div {
            padding: 0 !important;
            margin: 0 !important;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        div[data-testid="stToolbar"] {
            display: none;
        }
        div[data-testid="stDecoration"] {
            display: none;
        }
        button[kind="header"] {
            display: none;
        }
        .stSelectbox > div > div {
            max-width: 100%;
        }
        .stCanvas {
            width: 100vw !important;
            height: auto !important;
            max-width: none !important;
            aspect-ratio: 1300/900;
            transform: scale(1);
            transform-origin: top left;
        }
        canvas {
            width: 100vw !important;
            height: auto !important;
            aspect-ratio: 1300/900;
        }
        .canvas-container {
            width: 100vw !important;
            height: auto !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: visible !important;
        }
        .element-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        [data-testid="column"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        .stButton {
            padding: 1rem !important;
        }
        .row-widget {
            padding: 0.5rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Constants
DEFAULT_WIDTH = 1300
DEFAULT_HEIGHT = 900
MOBILE_BREAKPOINT = 768

# Formation coordinates (left side by default)
formations = {
    '4-3-3 (Attacking)': [(225, 150), (225, 350), (225, 550), (225, 750),
                          (350, 200), (350, 450), (350, 700),
                          (480, 200), (480, 450), (480, 700)],
    '4-3-3 (Defensive)': [(225, 150), (225, 350), (225, 550), (225, 750),
                          (300, 250), (300, 450), (300, 650),
                          (400, 200), (400, 450), (400, 700)],
    '4-4-2 (Diamond)': [(225, 150), (225, 350), (225, 550), (225, 750),
                        (300, 450),
                        (350, 250), (350, 650),
                        (400, 450),
                        (480, 300), (480, 600)],
    '4-4-2 (Flat)': [(225, 150), (225, 350), (225, 550), (225, 750),
                      (350, 150), (350, 350), (350, 550), (350, 750),
                      (480, 300), (480, 600)],
    '3-5-2': [(225, 250), (225, 450), (225, 650),
              (300, 150), (300, 450), (300, 750),
              (350, 300), (350, 600),
              (450, 300), (450, 600)],
    '3-4-3': [(225, 250), (225, 450), (225, 650),
              (350, 150), (350, 350), (350, 550), (350, 750),
              (480, 200), (480, 450), (480, 700)],
    '5-3-2': [(225, 150), (225, 350), (225, 550), (225, 750),
              (200, 450),
              (350, 250), (350, 450), (350, 650),
              (450, 300), (450, 600)],
    '4-2-3-1': [(225, 150), (225, 350), (225, 550), (225, 750),
                (300, 300), (300, 600),
                (400, 200), (400, 450), (400, 700),
                (480, 450)]
}

# Player roles and positions with descriptions
formation_positions = {
    '4-3-3 (Attacking)': [
        ('LB', 'Attacking Full-back'), ('CB', 'Ball-playing Defender'), 
        ('CB', 'Stopper'), ('RB', 'Attacking Full-back'),
        ('CDM', 'Deep-lying Playmaker'), ('CM', 'Box-to-box Midfielder'), 
        ('CAM', 'Advanced Playmaker'),
        ('LW', 'Inside Forward'), ('ST', 'Complete Forward'), ('RW', 'Inside Forward')
    ],
    '4-3-3 (Defensive)': [
        ('LB', 'Defensive Full-back'), ('CB', 'Ball-playing Defender'), 
        ('CB', 'Stopper'), ('RB', 'Defensive Full-back'),
        ('CDM', 'Defensive Midfielder'), ('CM', 'Box-to-box Midfielder'), 
        ('CM', 'Ball-winning Midfielder'),
        ('LW', 'Winger'), ('ST', 'Target Man'), ('RW', 'Winger')
    ],
    '4-4-2 (Diamond)': [
        ('LB', 'Full-back'), ('CB', 'Centre-back'), ('CB', 'Centre-back'), ('RB', 'Full-back'),
        ('CDM', 'Defensive Midfielder'), ('LM', 'Wide Midfielder'), ('RM', 'Wide Midfielder'),
        ('CAM', 'Attacking Midfielder'), ('ST', 'Target Man'), ('ST', 'Deep-lying Forward')
    ],
    '4-4-2 (Flat)': [
        ('LB', 'Full-back'), ('CB', 'Centre-back'), ('CB', 'Centre-back'), ('RB', 'Full-back'),
        ('LM', 'Wide Midfielder'), ('CM', 'Central Midfielder'), ('CM', 'Central Midfielder'),
        ('RM', 'Wide Midfielder'), ('ST', 'Target Man'), ('ST', 'Poacher')
    ],
    '3-5-2': [
        ('CB', 'Sweeper'), ('CB', 'Stopper'), ('CB', 'Cover'),
        ('LWB', 'Wing-back'), ('CDM', 'Defensive Midfielder'), ('CM', 'Box-to-box'),
        ('CM', 'Playmaker'), ('RWB', 'Wing-back'),
        ('ST', 'Target Man'), ('ST', 'Shadow Striker')
    ],
    '3-4-3': [
        ('CB', 'Sweeper'), ('CB', 'Stopper'), ('CB', 'Cover'),
        ('LM', 'Wing-back'), ('CM', 'Deep-lying Playmaker'), ('CM', 'Box-to-box'),
        ('RM', 'Wing-back'), ('LW', 'Inside Forward'), ('ST', 'Complete Forward'),
        ('RW', 'Inside Forward')
    ],
    '5-3-2': [
        ('LWB', 'Wing-back'), ('CB', 'Centre-back'), ('CB', 'Sweeper'),
        ('CB', 'Centre-back'), ('RWB', 'Wing-back'),
        ('CM', 'Defensive Midfielder'), ('CM', 'Box-to-box'), ('CM', 'Advanced Playmaker'),
        ('ST', 'Target Man'), ('ST', 'Shadow Striker')
    ],
    '4-2-3-1': [
        ('LB', 'Full-back'), ('CB', 'Ball-playing Defender'), ('CB', 'Stopper'),
        ('RB', 'Full-back'), ('CDM', 'Defensive Midfielder'), ('CDM', 'Deep-lying Playmaker'),
        ('CAM', 'Attacking Midfielder'), ('LW', 'Inside Forward'), ('ST', 'Complete Forward'),
        ('RW', 'Inside Forward')
    ]
}

# Tactical styles with descriptions
tactical_styles = {
    'Tiki-taka': 'Short passing, high possession, high press',
    'Counter-attack': 'Deep defense, fast transitions, direct passing',
    'Gegenpressing': 'Intense pressing after losing possession',
    'Direct Play': 'Long balls, physical presence, set pieces',
    'Wing Play': 'Width, crosses, overlapping runs',
    'Catenaccio': 'Defensive organization, counter-attacks'
}

# Function to calculate responsive dimensions
def get_responsive_dimensions():
    # Get the current viewport width from session state or use default
    viewport_width = st.session_state.get('viewport_width', DEFAULT_WIDTH)
    
    # Calculate the scale factor while maintaining aspect ratio
    scale_factor = min(1.0, viewport_width / DEFAULT_WIDTH)
    
    # Calculate new dimensions
    pitch_width = int(DEFAULT_WIDTH * scale_factor)
    pitch_height = int(DEFAULT_HEIGHT * scale_factor)
    
    return pitch_width, pitch_height

# Draw the football pitch
def draw_pitch_background():
    # Create pitch with original dimensions
    pitch = Image.new('RGB', (DEFAULT_WIDTH, DEFAULT_HEIGHT), (34, 139, 34))  # Green
    draw = ImageDraw.Draw(pitch)
    
    # Draw pitch elements with proper scaling
    line_width = max(2, int(5 * min(1, DEFAULT_WIDTH/1300)))  # Scale line width but keep minimum visibility
    
    # Main outline
    draw.rectangle([0, 0, DEFAULT_WIDTH-1, DEFAULT_HEIGHT-1], outline="white", width=line_width)
    
    # Center line
    draw.line([(DEFAULT_WIDTH//2, 0), (DEFAULT_WIDTH//2, DEFAULT_HEIGHT)], fill="white", width=line_width)
    
    # Center circle
    center = (DEFAULT_WIDTH//2, DEFAULT_HEIGHT//2)
    r = int(90 * min(1, DEFAULT_WIDTH/1300))  # Scale radius
    draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], outline="white", width=line_width)
    
    # Penalty areas
    box_width = int(165 * min(1, DEFAULT_WIDTH/1300))
    small_box_width = int(55 * min(1, DEFAULT_WIDTH/1300))
    box_height = int(450 * min(1, DEFAULT_HEIGHT/900))
    small_box_height = int(180 * min(1, DEFAULT_HEIGHT/900))
    
    # Left boxes
    draw.rectangle([0, (DEFAULT_HEIGHT-box_height)//2, box_width, (DEFAULT_HEIGHT+box_height)//2], outline="white", width=line_width)
    draw.rectangle([0, (DEFAULT_HEIGHT-small_box_height)//2, small_box_width, (DEFAULT_HEIGHT+small_box_height)//2], outline="white", width=line_width)
    
    # Right boxes
    draw.rectangle([DEFAULT_WIDTH-box_width, (DEFAULT_HEIGHT-box_height)//2, DEFAULT_WIDTH, (DEFAULT_HEIGHT+box_height)//2], outline="white", width=line_width)
    draw.rectangle([DEFAULT_WIDTH-small_box_width, (DEFAULT_HEIGHT-small_box_height)//2, DEFAULT_WIDTH, (DEFAULT_HEIGHT+small_box_height)//2], outline="white", width=line_width)
    
    # Penalty spots
    spot_size = max(2, int(5 * min(1, DEFAULT_WIDTH/1300)))
    draw.ellipse([100-spot_size, DEFAULT_HEIGHT//2-spot_size, 100+spot_size, DEFAULT_HEIGHT//2+spot_size], fill="white")
    draw.ellipse([DEFAULT_WIDTH-100-spot_size, DEFAULT_HEIGHT//2-spot_size, DEFAULT_WIDTH-100+spot_size, DEFAULT_HEIGHT//2+spot_size], fill="white")
    draw.ellipse([DEFAULT_WIDTH//2-spot_size, DEFAULT_HEIGHT//2-spot_size, DEFAULT_WIDTH//2+spot_size, DEFAULT_HEIGHT//2+spot_size], fill="white")
    
    return pitch

# Function to get viewport dimensions
def get_viewport_size():
    # Inject JavaScript to get viewport dimensions
    js_code = """
        <script>
        const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        const vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
        
        if (window.rendered_viewer) {
            window.rendered_viewer.postMessage({
                type: 'viewport_data',
                width: vw,
                height: vh
            }, '*');
        }
        </script>
    """
    st.components.v1.html(js_code, height=0)

# Main App
def app():
    st.title("⚽ Football Tactics Board")
    
    # Create a container for better mobile layout
    with st.container():
        # Create columns with responsive widths for mobile
        col1, col2 = st.columns([1, 1])
        
        with col1:
            team1_form = st.selectbox(
                "Team 1 Formation",
                list(formations.keys()),
                key="team1",
                help="Select formation for team 1"
            )
            
            # Add tactical style selector
            team1_style = st.selectbox(
                "Team 1 Tactical Style",
                list(tactical_styles.keys()),
                key="team1_style"
            )
            if team1_style:
                st.info(f"Style: {tactical_styles[team1_style]}")
            
            # Show player roles
            if team1_form:
                st.subheader("Team 1 Player Roles")
                for pos, role in formation_positions[team1_form]:
                    st.write(f"**{pos}**: {role}")
        
        with col2:
            team2_form = st.selectbox(
                "Team 2 Formation",
                list(formations.keys()),
                key="team2",
                help="Select formation for team 2"
            )
            
            # Add tactical style selector
            team2_style = st.selectbox(
                "Team 2 Tactical Style",
                list(tactical_styles.keys()),
                key="team2_style"
            )
            if team2_style:
                st.info(f"Style: {tactical_styles[team2_style]}")
            
            # Show player roles
            if team2_form:
                st.subheader("Team 2 Player Roles")
                for pos, role in formation_positions[team2_form]:
                    st.write(f"**{pos}**: {role}")

    # Get responsive dimensions
    pitch_width, pitch_height = get_responsive_dimensions()

    # Background image with responsive dimensions
    bg_image = draw_pitch_background()
    bg_image = bg_image.resize((pitch_width, pitch_height), Image.Resampling.LANCZOS)

    # Session state for persistence
    if "formation_key" not in st.session_state:
        st.session_state.formation_key = 0
    if "objects" not in st.session_state:
        st.session_state.objects = []

    # Generate formation button - full width and mobile-friendly
    if st.button("Generate Formation", use_container_width=True, key="generate_btn"):
        st.session_state.formation_key += 1
        objects = []

        # Scale factor for object positions
        scale_x = pitch_width / DEFAULT_WIDTH
        scale_y = pitch_height / DEFAULT_HEIGHT

        # Goalkeepers with scaled positions
        gk_radius = int(25 * min(scale_x, scale_y))
        objects.extend([
            {
                "type": "group",
                "left": int(80 * scale_x),
                "top": int((pitch_height//2 - 25) * scale_y),
                "width": gk_radius * 2,
                "height": gk_radius * 2,
                "objects": [
                    {"type": "circle", "left": 0, "top": 0, "radius": gk_radius, "fill": "yellow", "originX": "center", "originY": "center"},
                    {"type": "text", "left": 0, "top": -8, "text": "1", "fill": "black", "fontSize": int(16 * min(scale_x, scale_y)), "originX": "center", "originY": "center"},
                    {"type": "text", "left": 0, "top": 8, "text": "GK", "fill": "black", "fontSize": int(14 * min(scale_x, scale_y)), "originX": "center", "originY": "center"}
                ]
            },
            {
                "type": "group",
                "left": int((pitch_width - 130) * scale_x),
                "top": int((pitch_height//2 - 25) * scale_y),
                "width": gk_radius * 2,
                "height": gk_radius * 2,
                "objects": [
                    {"type": "circle", "left": 0, "top": 0, "radius": gk_radius, "fill": "yellow", "originX": "center", "originY": "center"},
                    {"type": "text", "left": 0, "top": -8, "text": "1", "fill": "black", "fontSize": int(16 * min(scale_x, scale_y)), "originX": "center", "originY": "center"},
                    {"type": "text", "left": 0, "top": 8, "text": "GK", "fill": "black", "fontSize": int(14 * min(scale_x, scale_y)), "originX": "center", "originY": "center"}
                ]
            }
        ])

        # Team 1 players with scaled positions
        player_radius = int(20 * min(scale_x, scale_y))
        for idx, ((x, y), (pos, role)) in enumerate(zip(formations[team1_form], formation_positions[team1_form])):
            scaled_x = int(x * scale_x)
            scaled_y = int(y * scale_y)
            if 0 <= scaled_x <= pitch_width and 0 <= scaled_y <= pitch_height:
                objects.append({
                    "type": "group",
                    "left": scaled_x,
                    "top": scaled_y,
                    "width": player_radius * 2,
                    "height": player_radius * 2,
                    "objects": [
                        {"type": "circle", "left": 0, "top": 0, "radius": player_radius, "fill": "blue", "originX": "center", "originY": "center"},
                        {"type": "text", "left": 0, "top": -8, "text": str(idx + 2), "fill": "white", "fontSize": int(16 * min(scale_x, scale_y)), "originX": "center", "originY": "center"},
                        {"type": "text", "left": 0, "top": 8, "text": pos, "fill": "white", "fontSize": int(14 * min(scale_x, scale_y)), "originX": "center", "originY": "center"}
                    ]
                })

        # Team 2 players with scaled positions
        for idx, ((x, y), (pos, role)) in enumerate(zip(formations[team2_form], formation_positions[team2_form])):
            mirrored_x = pitch_width - int(x * scale_x)
            scaled_y = int(y * scale_y)
            if 0 <= mirrored_x <= pitch_width and 0 <= scaled_y <= pitch_height:
                objects.append({
                    "type": "group",
                    "left": mirrored_x,
                    "top": scaled_y,
                    "width": player_radius * 2,
                    "height": player_radius * 2,
                    "objects": [
                        {"type": "circle", "left": 0, "top": 0, "radius": player_radius, "fill": "red", "originX": "center", "originY": "center"},
                        {"type": "text", "left": 0, "top": -8, "text": str(idx + 2), "fill": "white", "fontSize": int(16 * min(scale_x, scale_y)), "originX": "center", "originY": "center"},
                        {"type": "text", "left": 0, "top": 8, "text": pos, "fill": "white", "fontSize": int(14 * min(scale_x, scale_y)), "originX": "center", "originY": "center"}
                    ]
                })

        # Ball with scaled position
        ball_radius = int(15 * min(scale_x, scale_y))
        objects.append({
            "type": "circle",
            "left": pitch_width//2,
            "top": pitch_height//2,
            "radius": ball_radius,
            "fill": "white"
        })

        st.session_state.objects = objects

    # Render canvas with mobile-friendly container
    with st.container():
        canvas_key = f"canvas_{st.session_state.formation_key}"
        st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=int(5 * min(pitch_width/DEFAULT_WIDTH, pitch_height/DEFAULT_HEIGHT)),
            background_image=bg_image,
            height=pitch_height,
            width=pitch_width,
            drawing_mode="transform",
            initial_drawing={"version": "4.4.0", "objects": st.session_state.objects},
            key=canvas_key
        )

        # Add tactical instructions
        st.subheader("Tactical Instructions")
        st.write("""
        ### Pressing Zones
        - High Press: Press opponent in their defensive third
        - Mid Press: Engage in midfield
        - Low Block: Defend deep in own half
        
        ### Build-up Play
        - Short passing from the back
        - Direct long balls
        - Wing play with overlapping fullbacks
        
        ### Transitions
        - Quick counter-attacks
        - Possession retention
        - Immediate press after losing ball
        """)

# Main entry
if __name__ == "__main__":
    app()
