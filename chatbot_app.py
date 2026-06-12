import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI

load_dotenv()

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Learning Hub", page_icon="🧠", layout="centered")

MODES = {
    "datascience": {
        "label": "Data Science",
        "icon": "📊",
        "color": "#3b82f6",
        "glow": "59,130,246",
        "particle_color": "0x3b82f6",
        "system": "You are an expert Data Science AI assistant. Teach, explain, and clarify concepts clearly using clean markdown formatting, lists, and code blocks where applicable.",
        "hint": "Ask about ML, stats, pandas, model evaluation…",
        "tag": "ML · Stats · Python",
    },
    "fullstack": {
        "label": "Full Stack Java",
        "icon": "☕",
        "color": "#f97316",
        "glow": "249,115,22",
        "particle_color": "0xf97316",
        "system": "You are an expert Full Stack Java AI assistant. Teach, explain, and clarify concepts clearly using clean markdown formatting, lists, and code blocks where applicable.",
        "hint": "Ask about Spring Boot, React, REST APIs, databases…",
        "tag": "Java · Spring · Web",
    },
    "hacking": {
        "label": "Ethical Hacking",
        "icon": "🛡️",
        "color": "#22c55e",
        "glow": "34,197,94",
        "particle_color": "0x22c55e",
        "system": "You are an expert Ethical Hacking AI assistant. Teach, explain, and clarify concepts clearly using clean markdown formatting, lists, and code blocks where applicable.",
        "hint": "Ask about pen testing, CVEs, network security…",
        "tag": "Security · Networks · CTF",
    },
}

# Initialize session state variables
if "mode" not in st.session_state:
    st.session_state.mode = None
if "history" not in st.session_state:
    st.session_state.history = []
if "model" not in st.session_state:
    st.session_state.model = ChatMistralAI(model="mistral-small-2506", temperature=0.5)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS INJECTION (Fixed URL parsing formatting issue)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background: #080b12 !important;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.2rem 5rem 1.2rem; max-width: 820px; }

#three-canvas-wrap {
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
}

.mode-screen {
    position: relative; z-index: 1;
    min-height: 75vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    padding: 2rem 1rem;
}
.mode-headline {
    font-family: 'JetBrains Mono', monospace;
    font-size: clamp(1.5rem, 4vw, 2.2rem);
    font-weight: 500; color: #f8fafc;
    letter-spacing: -0.03em; margin-bottom: 0.4rem; text-align: center;
}
.mode-sub { font-size: 0.9rem; color: #64748b; text-align: center; margin-bottom: 2.4rem; }

.mode-cards { display: flex; gap: 1.1rem; flex-wrap: wrap; justify-content: center; max-width: 720px; margin-bottom: 2rem;}
.mode-card {
    background: rgba(15,21,35,0.82);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.6rem 1.4rem;
    width: 200px; text-align: center;
    backdrop-filter: blur(14px);
    transition: all 0.3s ease;
}
.mode-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,255,255,0.15);
}
.mode-card .card-icon { font-size: 2.4rem; margin-bottom: 0.7rem; }
.mode-card .card-title { font-weight: 600; font-size: 0.95rem; color: #f1f5f9; margin-bottom: 0.3rem; }
.mode-card .card-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.04em; }

.chat-header {
    display: flex; align-items: center;
    padding: 0.9rem 0;
    background: transparent;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    margin-bottom: 1.4rem;
    gap: 12px;
}
.chat-header-icon { font-size: 1.8rem; }
.chat-header-title { font-weight: 600; font-size: 1.1rem; color: #f1f5f9; }
.chat-header-tag { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; letter-spacing: 0.05em; }

/* Custom Chat Container Overrides to blend with dark mode */
[data-testid="stChatMessage"] {
    background-color: rgba(20, 28, 46, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(8px);
    margin-bottom: 0.8rem !important;
}

.empty-state { text-align: center; padding: 5rem 1rem; }
.empty-state .big { font-size: 3.5rem; margin-bottom: 0.6rem; }
.empty-state p { font-size: 0.9rem; max-width: 320px; margin: 0 auto; line-height: 1.7; color: #475569; }

.stChatInputContainer > div {
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    background: rgba(15,21,35,0.95) !important;
}
.stChatInputContainer textarea { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; }

.stButton > button {
    background: rgba(15,21,35,0.6) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    border-radius: 8px !important;
}
.stButton > button:hover {
    border-color: rgba(255,255,255,0.3) !important;
    color: #f1f5f9 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# THREE.JS AMBIENT BACKGROUND SYSTEM (Stripped of broken markdown links)
# ─────────────────────────────────────────────────────────────────────────────
def three_bg(particle_hex: str = "0x3b82f6"):
    st.markdown(f"""
    <div id="three-canvas-wrap"><canvas id="three-canvas"></canvas></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
    (function() {{
        if (window.__threeInit) return;
        window.__threeInit = true;

        const canvas = document.getElementById('three-canvas');
        const renderer = new THREE.WebGLRenderer({{ canvas, alpha: true, antialias: true }});
        renderer.setPixelRatio(window.devicePixelRatio);

        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, 1, 0.1, 1000);
        camera.position.z = 80;

        const COUNT = 250;
        const geo = new THREE.BufferGeometry();
        const pos = new Float32Array(COUNT * 3);
        const vel = new Float32Array(COUNT * 3);
        for (let i = 0; i < COUNT; i++) {{
            pos[i*3]   = (Math.random() - 0.5) * 200;
            pos[i*3+1] = (Math.random() - 0.5) * 200;
            pos[i*3+2] = (Math.random() - 0.5) * 60;
            vel[i*3]   = (Math.random() - 0.5) * 0.03;
            vel[i*3+1] = (Math.random() - 0.5) * 0.03;
            vel[i*3+2] = 0;
        }}
        geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));

        const mat = new THREE.PointsMaterial({{
            color: {particle_hex}, size: 1.0, transparent: true, opacity: 0.45, sizeAttenuation: true
        }});
        const points = new THREE.Points(geo, mat);
        scene.add(points);

        const lineMat = new THREE.LineBasicMaterial({{ color: {particle_hex}, transparent: true, opacity: 0.05 }});
        let lineObj = null;

        function buildLines() {{
            if (lineObj) scene.remove(lineObj);
            const verts = [];
            const THRESH = 24;
            for (let i = 0; i < COUNT; i++) {{
                for (let j = i+1; j < COUNT; j++) {{
                    const dx = pos[i*3]-pos[j*3], dy = pos[i*3+1]-pos[j*3+1];
                    if (Math.sqrt(dx*dx+dy*dy) < THRESH) {{
                        verts.push(pos[i*3],pos[i*3+1],pos[i*3+2], pos[j*3],pos[j*3+1],pos[j*3+2]);
                    }}
                }}
            }}
            const lg = new THREE.BufferGeometry();
            lg.setAttribute('position', new THREE.BufferAttribute(new Float32Array(verts), 3));
            lineObj = new THREE.LineSegments(lg, lineMat);
            scene.add(lineObj);
        }}

        let frame = 0, mx = 0, my = 0;
        window.addEventListener('mousemove', e => {{
            mx = (e.clientX/window.innerWidth - 0.5)*0.3;
            my = (e.clientY/window.innerHeight - 0.5)*0.3;
        }});

        function resize() {{
            renderer.setSize(window.innerWidth, window.innerHeight);
            camera.aspect = window.innerWidth/window.innerHeight;
            camera.updateProjectionMatrix();
        }}
        resize();
        window.addEventListener('resize', resize);

        function animate() {{
            requestAnimationFrame(animate);
            for (let i = 0; i < COUNT; i++) {{
                pos[i*3] += vel[i*3]; pos[i*3+1] += vel[i*3+1];
                if (Math.abs(pos[i*3])>100) vel[i*3]*=-1;
                if (Math.abs(pos[i*3+1])>100) vel[i*3+1]*=-1;
            }}
            geo.attributes.position.needsUpdate = true;
            if (++frame % 4 === 0) buildLines();
            camera.position.x += (mx*8 - camera.position.x)*0.03;
            camera.position.y += (-my*8 - camera.position.y)*0.03;
            renderer.render(scene, camera);
        }}
        animate();
    }})();
    </script>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# VIEW CONTROLLER
# ─────────────────────────────────────────────────────────────────────────────
if st.session_state.mode is None:
    # SCREEN 1: Welcome Screen
    three_bg("0x3b82f6")
    
    st.markdown('<div class="mode-screen">', unsafe_allow_html=True)
    st.markdown("""
        <div class="mode-headline">What do you want to learn today?</div>
        <div class="mode-sub">Select a workspace to engage with your specialized AI tutor.</div>
    """, unsafe_allow_html=True)

    # Dynamic UI Cards Display
    cards_html = '<div class="mode-cards">'
    for key, m in MODES.items():
        cards_html += f"""
        <div class="mode-card">
            <div class="card-icon">{m['icon']}</div>
            <div class="card-title">{m['label']}</div>
            <div class="card-tag" style="color:{m['color']};">{m['tag']}</div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    # Interactive Workspace Selection Buttons
    col1, col2, col3 = st.columns(3)
    for col, (key, m) in zip([col1, col2, col3], MODES.items()):
        with col:
            if st.button(f"Enter {m['label']}", key=f"btn_{key}", use_container_width=True):
                st.session_state.mode = key
                st.session_state.history = [SystemMessage(content=m["system"])]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # SCREEN 2: Live Conversation Workspace Environment
    current_mode = MODES[st.session_state.mode]
    three_bg(current_mode["particle_color"])

    # Header Panel Layout
    hcol, bcol1, bcol2 = st.columns([4, 1, 1])
    with hcol:
        st.markdown(f"""
        <div class="chat-header">
            <span class="chat-header-icon">{current_mode['icon']}</span>
            <div>
                <div class="chat-header-title">{current_mode['label']} Workspace</div>
                <div class="chat-header-tag" style="color:{current_mode['color']};">{current_mode['tag']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Interactive Utility Buttons
    with bcol1:
        st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("🧹 Clear", use_container_width=True, help="Clear active conversation logs"):
            st.session_state.history = [SystemMessage(content=current_mode["system"])]
            st.rerun()
            
    with bcol2:
        st.markdown("<div style='padding-top: 15px;'></div>", unsafe_allow_html=True)
        if st.button("⟵ Leave", use_container_width=True):
            st.session_state.mode = None
            st.session_state.history = []
            st.rerun()

    # Filter system context message out from user logs
    chat_msgs = [msg for msg in st.session_state.history if not isinstance(msg, SystemMessage)]

    # Handle Empty State Scenario
    if not chat_msgs:
        st.markdown(f"""
        <div class="empty-state">
            <div class="big">{current_mode['icon']}</div>
            <p>{current_mode['hint']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Loop over conversation array using native containers (Safeguards Markdown layout parsing)
        for msg in chat_msgs:
            if isinstance(msg, HumanMessage):
                with st.chat_message("user", avatar="🧑"):
                    st.markdown(msg.content)
            elif isinstance(msg, AIMessage):
                with st.chat_message("assistant", avatar=current_mode['icon']):
                    st.markdown(msg.content)

    # Chat Input Box
    if prompt := st.chat_input(current_mode["hint"]):
        st.session_state.history.append(HumanMessage(content=prompt))
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)
            
        with st.chat_message("assistant", avatar=current_mode['icon']):
            with st.spinner("Processing concepts..."):
                response = st.session_state.model.invoke(st.session_state.history)
                st.markdown(response.content)
                
        st.session_state.history.append(AIMessage(content=response.content))
        st.rerun()