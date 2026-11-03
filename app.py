import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# CSS: 인디핑크 생성 버튼 및 모바일 전용 원터치 컬러 타일 스타일
st.markdown("""
<style>
div[data-testid="stButton"] > button {
    background-color: #F4C2C2 !important;
    color: #333333 !important;
    border: none !important;
    font-weight: bold !important;
    padding: 0.7rem 1rem !important;
    border-radius: 10px !important;
}

/* 컬러 타일 버튼 전용 여백 및 크기 세팅 */
div[data-testid="column"] button {
    height: 26px !important;
    min-height: 26px !important;
    padding: 0px !important;
    margin: 1px 0px !important;
    border-radius: 3px !important;
    font-size: 11px !important;
    font-weight: bold !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 36가지 핵심 컬러 팔레트 (가로 6 x 세로 6)
PALETTE_36 = [
    "#000000", "#333333", "#666666", "#999999", "#D9D9D9", "#FFFFFF",
    "#8B0000", "#FF0000", "#FF453A", "#FF6B6B", "#FF8E8E", "#FFC1C1",
    "#D35400", "#FF851B", "#FFA500", "#FFD700", "#FFE812", "#FFF9E6",
    "#1E4620", "#2ECC40", "#30D158", "#20C997", "#A8E6CF", "#E9F3ED",
    "#001F3F", "#0074D9", "#007AFF", "#32ADE6", "#7FDBFF", "#E1F5FE",
    "#4B0082", "#B10DC9", "#AF52DE", "#FF2D55", "#F4C2C2", "#F8EDE9"
]

# 세션 색상 초기값
if "text_color" not in st.session_state:
    st.session_state.text_color = "#000000"
if "shadow_color" not in st.session_state:
    st.session_state.shadow_color = "#999999"
if "outline_color" not in st.session_state:
    st.session_state.outline_color = "#FFFFFF"
if "action_text_color" not in st.session_state:
    st.session_state.action_text_color = "#FF3B30"
if "action_outline_color" not in st.session_state:
    st.session_state.action_outline_color = "#FFFFFF"

# 영문 목록 없이 타일 클릭 즉시 선택되는 6x6 원터치 팔레트 함수
def render_touch_palette(label, state_key):
    st.write(f"**{label}**")
    cur_color = st.session_state[state_key]
    
    # 6개씩 6줄 모눈판
    for r in range(6):
        cols = st.columns(6)
        for c in range(6):
            idx = r * 6 + c
            color_hex = PALETTE_36[idx]
            is_active = (cur_color.upper() == color_hex.upper())
            mark = "●" if is_active else ""
            txt_color = "#FFFFFF" if color_hex in ["#000000", "#333333", "#666666", "#8B0000", "#1E4620", "#001F3F", "#4B0082"] else "#000000"
            border_css = "2px solid #FF3B30" if is_active else "1px solid rgba(0,0,0,0.15)"
            
            with cols[c]:
                # 타일에 실제 색상 입히기
                st.markdown(f"""
                <style>
                div[data-testid="stHorizontalBlock"] div:nth-child({c+1}) button[key="btn_{state_key}_{idx}"] {{
                    background-color: {color_hex} !important;
                    color: {txt_color} !important;
                    border: {border_css} !important;
                }}
                </style>
                """, unsafe_allow_html=True)
                
                if st.button(mark, key=f"btn_{state_key}_{idx}", use_container_width=True):
                    st.session_state[state_key] = color_hex
                    st.rerun()

# 2. 헤드라인 입력 섹션
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
headline_text = st.text_input("", value="50대에 시작하는 월 300 파이프라인", label_visibility="collapsed")

# 3. 폰트 및 스타일 설정
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=600, value=250)

col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 헤드라인 전용 원터치 타일 (라벨 간소화 완료)
render_touch_palette("글자색상", "text_color")
if use_shadow:
    render_touch_palette("그림자색상", "shadow_color")
if use_outline:
    render_touch_palette("외곽선색상", "outline_color")

# 4. 캡션유도문장 섹션 (라벨 간소화 완료)
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="👉 상세한 내용은 본문 내용 확인", label_visibility="collapsed")

use_action_outline = st.checkbox("외곽선", value=False, key="chk_act_out")
render_touch_palette("글자색상", "action_text_color")
if use_action_outline:
    render_touch_palette("외곽선색상", "action_outline_color")

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

# 6. 이미지 생성 함수
def create_card():
    width, height = 1080, 1350
    
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

    def get_text_center_x(text, f):
        bbox = draw.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        return (width - w) // 2

    # 1) 헤드라인 출력
    hx = get_text_center_x(headline_text, font)
    if use_shadow:
        draw.text((hx + 4, text_y_pos + 4), headline_text, font=font, fill=st.session_state.shadow_color)
    if use_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((hx + dx, text_y_pos + dy), headline_text, font=font, fill=st.session_state.outline_color)
    draw.text((hx, text_y_pos), headline_text, font=font, fill=st.session_state.text_color)

    # 2) 캡션유도문장 출력 (헤드라인 다음 줄 배치)
    action_y_pos = text_y_pos + font_size + 35
    ax = get_text_center_x(action_text, sub_font)
    if use_action_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((ax + dx, action_y_pos + dy), action_text, font=sub_font, fill=st.session_state.action_outline_color)
    draw.text((ax, action_y_pos), action_text, font=sub_font, fill=st.session_state.action_text_color)

    # 3) 왼쪽 하단 계정 브랜딩
    draw.text((50, 1270), "@duruduru.page", font=brand_font, fill="#888888")

    return image

# 7. 생성 및 다운로드 버튼
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
