import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 인디핑크 생성 버튼 및 모눈판 스타일
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #F4C2C2;
    color: #333333;
    border: none;
    font-weight: bold;
    padding: 0.6rem 1rem;
    border-radius: 10px;
}
div.stButton > button:first-child:hover {
    background-color: #EAAFAF;
    color: #111111;
}
.color-box {
    display: inline-block;
    width: 20px;
    height: 20px;
    border-radius: 3px;
    margin-right: 5px;
    vertical-align: middle;
    border: 1px solid #ccc;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 36가지 감성 & 비즈니스 컬러 팔레트 (HEX)
PALETTE_36 = [
    "#000000", "#1C1C1E", "#3A3A3C", "#555555", "#8E8E93", "#C7C7CC", "#E5E5EA", "#FFFFFF",
    "#FF3B30", "#FF453A", "#FF6961", "#FF9500", "#FF9F0A", "#FFB340", "#FFCC00", "#FFD60A",
    "#FFE812", "#34C759", "#30D158", "#32ADE6", "#007AFF", "#0A84FF", "#5856D6", "#5E5CE6",
    "#AF52DE", "#BF5AF2", "#FF2D55", "#FF375F", "#E91E63", "#F8EDE9", "#F4C2C2", "#F6F4EE",
    "#FFF9E6", "#E9F3ED", "#D0E8FF", "#F1E4FF"
]

# 세션 상태 초기화 (색상 저장용)
if "text_color" not in st.session_state:
    st.session_state.text_color = "#000000"
if "shadow_color" not in st.session_state:
    st.session_state.shadow_color = "#8E8E93"
if "outline_color" not in st.session_state:
    st.session_state.outline_color = "#FFFFFF"

# 2. 헤드라인 입력
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
headline_text = st.text_input("", value="50대에 시작하는 월 300 파이프라인", label_visibility="collapsed")

# 3. 폰트 및 세부 설정 (구분선 없이 바로 연결)
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=500, value=150)

# 두껍게, 그림자, 외곽선 (색상 위로 배치)
col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 36컬러 초소형 모눈판 선택 함수
def render_color_grid(label, state_key):
    st.caption(f"**{label}**")
    cols_per_row = 12
    for row in range(3):  # 3줄 x 12칸 = 36칸
        cols = st.columns(cols_per_row)
        for col_idx in range(cols_per_row):
            c_idx = row * cols_per_row + col_idx
            c_code = PALETTE_36[c_idx]
            with cols[col_idx]:
                is_selected = (st.session_state[state_key] == c_code)
                btn_label = "●" if is_selected else " "
                if st.button(btn_label, key=f"{state_key}_{c_idx}", use_container_width=True):
                    st.session_state[state_key] = c_code
                    st.rerun()

# 색상 선택 모눈판 출력
render_color_grid("글자 색상", "text_color")
if use_shadow:
    render_color_grid("그림자 색상", "shadow_color")
if use_outline:
    render_color_grid("외곽선 색상", "outline_color")

text_color = st.session_state.text_color
shadow_color = st.session_state.shadow_color
outline_color = st.session_state.outline_color

# 4. 캡션유도문장
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="상세한 내용은 본문 내용 확인", label_visibility="collapsed")

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

# 6. 이미지 생성 로직
def create_card():
    width, height = 1080, 1080
    
    if design_type == "사진형" and uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        image = image.resize((width, height))
    else:
        image = Image.new("RGB", (width, height), color=bg_color)
        
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype(font_path, font_size)
        sub_font = ImageFont.truetype(font_path, int(font_size * 0.45))
    except:
        font = ImageFont.load_default()
        sub_font = ImageFont.load_default()

    def get_text_center_x(text, f):
        bbox = draw.textbbox((0, 0), text, font=f)
        w = bbox[2] - bbox[0]
        return (width - w) // 2

    hx = get_text_center_x(headline_text, font)
    
    # 그림자 효과
    if use_shadow:
        draw.text((hx + 4, text_y_pos + 4), headline_text, font=font, fill=shadow_color)
        
    # 외곽선 효과
    if use_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((hx + dx, text_y_pos + dy), headline_text, font=font, fill=outline_color)

    # 헤드라인
    draw.text((hx, text_y_pos), headline_text, font=font, fill=text_color)

    # 캡션유도문장 (하단 고정)
    ax = get_text_center_x(action_text, sub_font)
    draw.text((ax, 960), action_text, font=sub_font, fill="#666666")

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
