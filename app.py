import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 맨 아래 '생성하기' 버튼만 핑크색을 타겟팅하고, 모눈판에는 간섭하지 않도록 CSS 수정
st.markdown("""
<style>
div[data-testid="stButton"]:last-of-type > button {
    background-color: #F4C2C2 !important;
    color: #333333 !important;
    border: none !important;
    font-weight: bold !important;
    padding: 0.7rem 1rem !important;
    border-radius: 10px !important;
}
div[data-testid="stButton"]:last-of-type > button:hover {
    background-color: #EAAFAF !important;
    color: #111111 !important;
}
/* 모눈판 버튼 크기 최적화 */
div[data-testid="column"] button {
    height: 32px !important;
    padding: 0px !important;
    border-radius: 4px !important;
    font-size: 11px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 36가지 실전 비즈니스 & 감성 컬러 팔레트 (이름과 실제 색상 매칭)
PALETTE_36 = {
    "검정": "#000000", "먹색": "#1C1C1E", "다크그레이": "#3A3A3C", "회색": "#8E8E93", "라이트그레이": "#E5E5EA", "순백색": "#FFFFFF",
    "레드": "#FF3B30", "코랄": "#FF6961", "오렌지": "#FF9500", "골드": "#FFB340", "옐로우": "#FFE812", "레몬": "#FFF9E6",
    "네온그린": "#30D158", "포레스트": "#1B5E20", "민트": "#E9F3ED", "스카이블루": "#32ADE6", "블루": "#007AFF", "딥블루": "#0A84FF",
    "인디고": "#5856D6", "퍼플": "#AF52DE", "라벤더": "#F1E4FF", "마젠타": "#FF2D55", "인디핑크": "#F4C2C2", "앤디핑크": "#F8EDE9",
    "브라운": "#795548", "초콜릿": "#4E342E", "카키": "#556B2F", "베이지": "#F6F4EE", "아이보리": "#FDFBF7", "크림": "#FFFDF9",
    "와인": "#880E4F", "네이비": "#0D47A1", "올리브": "#827717", "피치": "#FFDAB9", "살구": "#FFE4E1", "차콜": "#212121"
}

# 2. 헤드라인 입력
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
headline_text = st.text_input("", value="50대에 시작하는 월 300 파이프라인", label_visibility="collapsed")

# 3. 폰트 및 세부 설정
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}
selected_font_label = st.selectbox("폰트 선택", list(font_options.keys()))
font_path = font_options[selected_font_label]

font_size = st.slider("글자 크기", min_value=30, max_value=90, value=55)
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=500, value=150)

# 두껍게 / 그림자 / 외곽선 체크박스 (색상 위 배치)
col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

# 모바일 호환 36색상 선택기 (색상 미리보기 상자 포함)
def color_picker_box(label, default_name):
    st.write(f"**{label}**")
    color_keys = list(PALETTE_36.keys())
    choice = st.selectbox(
        f"{label} 선택",
        options=color_keys,
        index=color_keys.index(default_name),
        label_visibility="collapsed"
    )
    hex_code = PALETTE_36[choice]
    # 선택된 색상을 시각적으로 보여주는 작은 컬러 바
    st.markdown(
        f'<div style="background-color: {hex_code}; height: 16px; width: 100%; border-radius: 4px; border: 1px solid #ccc; margin-bottom: 10px;"></div>',
        unsafe_allow_html=True
    )
    return hex_code

# 글자 색상 선택
text_color = color_picker_box("글자 색상", "검정")

# 그림자 색상 선택 (체크 시 활성화)
shadow_color = "#8E8E93"
if use_shadow:
    shadow_color = color_picker_box("그림자 색상", "회색")

# 외곽선 색상 선택 (체크 시 활성화)
outline_color = "#FFFFFF"
if use_outline:
    outline_color = color_picker_box("외곽선 색상", "순백색")

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
