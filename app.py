import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

st.title("📸 카드뉴스공장")

# 36가지 실전 6x6 컬러 팔레트 (가로 6개 x 세로 6개)
PALETTE_36 = [
    "#000000", "#333333", "#666666", "#999999", "#D9D9D9", "#FFFFFF",
    "#8B0000", "#FF0000", "#FF453A", "#FF6B6B", "#FF8E8E", "#FFC1C1",
    "#D35400", "#FF851B", "#FFA500", "#FFD700", "#FFE812", "#FFF9E6",
    "#1E4620", "#2ECC40", "#30D158", "#20C997", "#A8E6CF", "#E9F3ED",
    "#001F3F", "#0074D9", "#007AFF", "#32ADE6", "#7FDBFF", "#E1F5FE",
    "#4B0082", "#B10DC9", "#AF52DE", "#FF2D55", "#F4C2C2", "#F8EDE9"
]

# 세션 상태 초기화
if "text_color" not in st.session_state:
    st.session_state.text_color = "#000000"
if "shadow_color" not in st.session_state:
    st.session_state.shadow_color = "#999999"
if "outline_color" not in st.session_state:
    st.session_state.outline_color = "#FFFFFF"

# 2. 헤드라인 입력
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
headline_text = st.text_input("", value="50대에 시작하는 월 300 파이프라인", label_visibility="collapsed")

# 3. 폰트 및 설정
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=500, value=150)

# 두껍게 / 그림자 / 외곽선 체크박스
col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 모바일 전용 6x6 모눈판 렌더링 함수
def render_mobile_grid(title, state_key):
    st.write(f"**{title}**")
    current_val = st.session_state[state_key]
    
    # 6개씩 묶어서 6줄로 구성
    for row_idx in range(6):
        row_colors = PALETTE_36[row_idx * 6 : (row_idx + 1) * 6]
        choice = st.radio(
            f"{title}_{row_idx}",
            options=row_colors,
            index=row_colors.index(current_val) if current_val in row_colors else None,
            format_func=lambda c: f"■ {c}",
            horizontal=True,
            key=f"grid_{state_key}_{row_idx}",
            label_visibility="collapsed"
        )
        if choice and choice != current_val:
            st.session_state[state_key] = choice
            st.rerun()

# 글자 색상 모눈판
render_mobile_grid("글자 색상", "text_color")

# 그림자 색상 모눈판 (체크 시 노출)
if use_shadow:
    render_mobile_grid("그림자 색상", "shadow_color")

# 외곽선 색상 모눈판 (체크 시 노출)
if use_outline:
    render_mobile_grid("외곽선 색상", "outline_color")

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

# 6. 이미지 생성 함수
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
    
    # 그림자
    if use_shadow:
        draw.text((hx + 4, text_y_pos + 4), headline_text, font=font, fill=shadow_color)
        
    # 외곽선
    if use_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((hx + dx, text_y_pos + dy), headline_text, font=font, fill=outline_color)

    # 헤드라인
    draw.text((hx, text_y_pos), headline_text, font=font, fill=text_color)

    # 캡션유도문장
    ax = get_text_center_x(action_text, sub_font)
    draw.text((ax, 960), action_text, font=sub_font, fill="#666666")

    return image

# 7. 버튼 및 다운로드
st.markdown("---")

# 인디핑크 생성 버튼 전용 CSS
st.markdown("""
<style>
div.stButton > button {
    background-color: #F4C2C2 !important;
    color: #333333 !important;
    border: none !important;
    font-weight: bold !important;
    padding: 0.7rem 1rem !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

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
