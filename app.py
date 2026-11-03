import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 생성하기 버튼 인디핑크 전용 스타일
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
</style>
""", unsafe_allow_html=True)

st.title("📸 카드뉴스공장")

# 세션 기본값 설정
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
text_y_pos = st.slider("헤드라인 위치", min_value=50, max_value=600, value=250)

col_chk1, col_chk2, col_chk3 = st.columns(3)
with col_chk1:
    use_bold = st.checkbox("두껍게", value=True)
with col_chk2:
    use_shadow = st.checkbox("그림자", value=False)
with col_chk3:
    use_outline = st.checkbox("외곽선", value=False)

def render_clean_picker(label, state_key):
    st.write(f"**{label}**")
    c1, c2 = st.columns([1, 4])
    with c1:
        picked = st.color_picker("", st.session_state[state_key], key=f"cp_{state_key}", label_visibility="collapsed")
        st.session_state[state_key] = picked
    with c2:
        st.markdown(
            f'<div style="background-color:{picked}; height:35px; border-radius:6px; border:1px solid #ccc; line-height:35px; text-align:center; color:#888; font-size:12px;">선택된 색상</div>',
            unsafe_allow_html=True
        )

# 헤드라인 색상 설정
render_clean_picker("글자색상", "text_color")
if use_shadow:
    render_clean_picker("그림자색상", "shadow_color")
if use_outline:
    render_clean_picker("외곽선색상", "outline_color")

# 4. 캡션유도문장 (절대 깨지지 않는 기호로 기본값 지정)
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="▶ 상세한 내용은 본문 내용 확인", label_visibility="collapsed")

use_action_outline = st.checkbox("외곽선", value=False, key="chk_act_out")
render_clean_picker("글자색상", "action_text_color")
if use_action_outline:
    render_clean_picker("외곽선색상", "action_outline_color")

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

    # 손가락 이모지(👉)가 입력될 경우 네모 엑스 방지를 위해 깔끔한 기호(▶)로 자동 치환
    safe_action_text = action_text.replace("👉", "▶").replace("☞", "▶")

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

    # 2) 캡션유도문장 출력 (헤드라인 바로 다음 줄에 자동 정렬)
    action_y_pos = text_y_pos + font_size + 35
    ax = get_text_center_x(safe_action_text, sub_font)
    if use_action_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((ax + dx, action_y_pos + dy), safe_action_text, font=sub_font, fill=st.session_state.action_outline_color)
    draw.text((ax, action_y_pos), safe_action_text, font=sub_font, fill=st.session_state.action_text_color)

    # 3) 왼쪽 하단 브랜딩 아이디 고정
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
