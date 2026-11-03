import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 하단 생성 버튼 인디핑크 스타일 및 4x6 바둑판 전용 여백
st.markdown("""
<style>
/* 카드뉴스 즉시 생성하기 핑크 버튼 */
div[data-testid="stButton"]:last-of-type > button {
    background-color: #F4C2C2 !important;
    color: #333333 !important;
    border: none !important;
    font-weight: bold !important;
    padding: 0.7rem 1rem !important;
    border-radius: 10px !important;
}

/* 4x6 컬러 바둑판 타일 버튼 최적화 (가로 4칸 고정) */
div[data-testid="column"] button {
    height: 34px !important;
    min-height: 34px !important;
    padding: 0px !important;
    margin: 2px 0px !important;
    border-radius: 4px !important;
    font-size: 13px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 가로 4칸 x 세로 6줄 (총 24가지 핵심 컬러)
PALETTE_24 = [
    "#000000", "#555555", "#AAAAAA", "#FFFFFF",
    "#8B0000", "#FF0000", "#FF453A", "#FF8E8E",
    "#FF851B", "#FFA500", "#FFE812", "#FFF9E6",
    "#1E4620", "#30D158", "#20C997", "#E9F3ED",
    "#001F3F", "#007AFF", "#32ADE6", "#E1F5FE",
    "#4B0082", "#AF52DE", "#F4C2C2", "#F8EDE9"
]

# 세션 상태 초기화
if "text_color" not in st.session_state:
    st.session_state.text_color = "#000000"
if "shadow_color" not in st.session_state:
    st.session_state.shadow_color = "#AAAAAA"
if "outline_color" not in st.session_state:
    st.session_state.outline_color = "#FFFFFF"
if "action_text_color" not in st.session_state:
    st.session_state.action_text_color = "#FF0000"
if "action_outline_color" not in st.session_state:
    st.session_state.action_outline_color = "#FFFFFF"

# 2. 헤드라인 입력 (엔터 줄바꿈 지원)
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
default_headline = "50대에 시작하는\n월 300 파이프라인"
headline_text = st.text_area("", value=default_headline, height=100, label_visibility="collapsed")

# 3. 폰트 및 위치 설정
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("헤드라인 글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=600, value=250)

col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 터치/클릭 즉시 선택되는 가로 4칸 x 세로 6줄 네이티브 바둑판
def render_4x6_grid(label, state_key):
    st.write(f"**{label}**")
    cur_color = st.session_state[state_key].upper()
    
    # 6개 행 생성
    for r in range(6):
        cols = st.columns(4)
        for c in range(4):
            idx = r * 4 + c
            color_hex = PALETTE_24[idx]
            is_active = (cur_color == color_hex.upper())
            mark = "✔" if is_active else ""
            txt_color = "#FFFFFF" if color_hex in ["#000000", "#555555", "#8B0000", "#1E4620", "#001F3F", "#4B0082"] else "#000000"
            border_css = "3px solid #FF3B30" if is_active else "1px solid #CCCCCC"
            
            with cols[c]:
                # 각 버튼에 해당 색상과 테두리 직접 주입
                st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] div:nth-child({c+1}) button[key="btn_{state_key}_{idx}"] {{
                    background-color: {color_hex} !important;
                    color: {txt_color} !important;
                    border: {border_css} !important;
                }}
                </style>
                """, unsafe_allow_html=True)
                
                # 터치 시 세션 저장 후 즉시 리런
                if st.button(mark, key=f"btn_{state_key}_{idx}", use_container_width=True):
                    st.session_state[state_key] = color_hex
                    st.rerun()

# 헤드라인 전용 4x6 바둑판
render_4x6_grid("글자색상", "text_color")
if use_shadow:
    render_4x6_grid("그림자색상", "shadow_color")
if use_outline:
    render_4x6_grid("외곽선색상", "outline_color")

# 4. 캡션유도문장
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="▶ 상세한 내용은 본문 내용 확인", label_visibility="collapsed")

use_action_outline = st.checkbox("외곽선", value=False, key="chk_act_out")
render_4x6_grid("글자색상", "action_text_color")
if use_action_outline:
    render_4x6_grid("외곽선색상", "action_outline_color")

# 5. 디자인 선택
st.markdown("---")
st.subheader("🎨 디자인 선택")
design_type = st.radio("", ["기본형", "사진형"], horizontal=True, label_visibility="collapsed")

BG_PALETTE = {
    "크림베이지": "#F6F4EE",
    "앤디핑크": "#F8EDE9",
    "민트": "#E9F3ED",
    "다크그레이": "#2A2A2A",
    "순백색": "#FFFFFF"
}

uploaded_file = None
if design_type == "기본형":
    bg_name = st.selectbox("배경색상 선택", list(BG_PALETTE.keys()), index=0)
    bg_color = BG_PALETTE[bg_name]
else:
    bg_color = "#FFFFFF"
    st.markdown("**📁 파일불러오기**")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# 6. 이미지 생성 로직 (좌우 여백 80px 보장 & 첫 글자 줄맞춤)
def create_card():
    width, height = 1080, 1350
    margin_x = 80  # 좌우 여백 확보
    
    if design_type == "사진형" and uploaded_file is not None:
        raw_image = Image.open(uploaded_file)
        raw_image = ImageOps.exif_transpose(raw_image).convert("RGB")
        image = ImageOps.fit(raw_image, (width, height), Image.Resampling.LANCZOS)
    else:
        image = Image.new("RGB", (width, height), color=bg_color)
        
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
        sub_font = ImageFont.truetype(font_path, int(font_size * 0.52))
        brand_font = ImageFont.truetype(font_path, 32)
    except:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()

    lines = [line.strip() for line in headline_text.split("\n") if line.strip()]
    if not lines:
        lines = ["문구를 입력하세요"]

    curr_y = text_y_pos
    line_spacing = int(font_size * 1.35)
    
    # 1) 헤드라인 출력 (대표님이 엔터 친 라인 그대로 좌측 margin_x에 정렬)
    for line in lines:
        if use_shadow:
            draw.text((margin_x + 4, curr_y + 4), line, font=font, fill=st.session_state.shadow_color)
        if use_outline:
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                draw.text((margin_x + dx, curr_y + dy), line, font=font, fill=st.session_state.outline_color)
        draw.text((margin_x, curr_y), line, font=font, fill=st.session_state.text_color)
        curr_y += line_spacing

    # 2) 캡션유도문장 출력 (헤드라인 첫 글자 기준 margin_x에 정확히 수직 줄맞춤)
    curr_y += 15
    safe_action_text = action_text.replace("👉", "▶").replace("☞", "▶")
    
    if use_action_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((margin_x + dx, curr_y + dy), safe_action_text, font=sub_font, fill=st.session_state.action_outline_color)
    draw.text((margin_x, curr_y), safe_action_text, font=sub_font, fill=st.session_state.action_text_color)

    # 3) 왼쪽 하단 브랜딩 (margin_x 정렬)
    draw.text((margin_x, 1260), "@duruduru.page", font=brand_font, fill="#888888")

    return image

# 7. 버튼 및 다운로드
st.markdown("---")
if st.button("🚀 카드뉴스 이미지 즉시 생성하기", use_container_width=True):
    result_img = create_card()
    st.image(result_img, caption="완성된 카드뉴스 미리보기", use_container_width=True)
    
    buf = io.BytesIO()
    result_img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="💾 스마트폰 갤러리에 저장하기",
        data=byte_im,
        file_name="cardnews_output.png",
        mime="image/png",
        use_container_width=True
    )
