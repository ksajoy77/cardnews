import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 화면 기본 설정 및 타이틀
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 생성 버튼 연한 인디핑크 스타일 적용
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
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 색상 매핑 표
COLOR_PALETTE = {
    "검정": "#000000",
    "흰색": "#FFFFFF",
    "노랑": "#FFE812",
    "빨강": "#FF3B30",
    "파랑": "#007AFF",
    "차콜": "#333333",
    "아이보리": "#FDFBF7"
}

# 기본 배경색 목록
BG_PALETTE = {
    "크림베이지": "#F6F4EE",
    "앤디핑크": "#F8EDE9",
    "민트": "#E9F3ED",
    "다크그레이": "#2A2A2A",
    "순백색": "#FFFFFF"
}

# 2. 헤드라인 입력
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
headline_text = st.text_input("", value="50대에 시작하는 월 300 파이프라인", label_visibility="collapsed")

# 3. 폰트 및 세부 설정
st.markdown("---")
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치 (상/하)", min_value=50, max_value=500, value=150)

col1, col2 = st.columns(2)
with col1:
    text_color_name = st.selectbox("글자 색상", list(COLOR_PALETTE.keys()), index=0)
    text_color = COLOR_PALETTE[text_color_name]
with col2:
    outline_color_name = st.selectbox("외곽선 색상", list(COLOR_PALETTE.keys()), index=1)
    outline_color = COLOR_PALETTE[outline_color_name]

col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 4. 캡션유도문장
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="상세한 내용은 본문 내용 확인", label_visibility="collapsed")

# 5. 디자인 선택
st.markdown("---")
st.subheader("🎨 디자인 선택")
design_type = st.radio("", ["기본형", "사진형"], horizontal=True, label_visibility="collapsed")

uploaded_file = None
if design_type == "기본형":
    bg_name = st.selectbox("배경색상 선택", list(BG_PALETTE.keys()), index=0)
    bg_color = BG_PALETTE[bg_name]
else:
    bg_color = "#FFFFFF"
    st.markdown("**📁 파일불러오기**")
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# 6. 카드 이미지 생성 함수
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
    
    if use_shadow:
        draw.text((hx + 3, text_y_pos + 3), headline_text, font=font, fill="#888888")
        
    if use_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((hx + dx, text_y_pos + dy), headline_text, font=font, fill=outline_color)

    draw.text((hx, text_y_pos), headline_text, font=font, fill=text_color)

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
