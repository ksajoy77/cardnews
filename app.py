import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# 1. 화면 기본 설정
st.set_page_config(page_title="카드뉴스공장", layout="centered")

# 바둑판 타일 전용 초경량 스타일 (렉 및 멈춤 원천 차단)
st.markdown("""
<style>
/* 카드뉴스 생성 버튼 핑크 */
div[data-testid="stButton"] > button {
    background-color: #F4C2C2 !important;
    color: #333333 !important;
    border: none !important;
    font-weight: bold !important;
    padding: 0.7rem 1rem !important;
    border-radius: 10px !important;
    width: 100% !important;
}

/* 4열 바둑판 타일 정렬 스타일 */
div[role="radiogroup"] {
    display: grid !important;
    grid-template-columns: repeat(4, 1fr) !important;
    gap: 8px !important;
    width: 220px !important;
    margin-bottom: 15px !important;
}
div[role="radiogroup"] label {
    margin: 0 !important;
    padding: 0 !important;
    display: flex !important;
    justify-content: center !important;
    cursor: pointer !important;
}
div[role="radiogroup"] label > div:first-child {
    display: none !important; /* 동그라미 라디오 버튼 숨김 */
}
div[role="radiogroup"] label > div:last-child {
    width: 48px !important;
    height: 32px !important;
    border-radius: 6px !important;
    border: 1px solid rgba(0,0,0,0.15) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 11px !important;
    font-weight: bold !important;
    color: transparent !important;
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

# 2. 헤드라인 입력 (엔터 줄바꿈 지원)
st.markdown("---")
st.subheader("✍️ 헤드라인 입력")
default_headline = "50대에 시작하는\n월 300 파이프라인"
headline_text = st.text_area("", value=default_headline, height=100, label_visibility="collapsed")

# 3. 폰트 및 설정
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

# 24개 색상 바둑판 렌더링 함수
def render_palette_board(label, default_color, key_name):
    st.write(f"**{label}**")
    
    # CSS로 각 타일에 실제 배경색 입히기
    style_tag = "<style>"
    for idx, c in enumerate(PALETTE_24):
        style_tag += f"""
        div[data-testid="stRadio"] div[key="{key_name}"] div[role="radiogroup"] label:nth-child({idx+1}) > div:last-child {{
            background-color: {c} !important;
        }}
        """
    style_tag += f"""
    div[data-testid="stRadio"] div[key="{key_name}"] div[role="radiogroup"] label[data-checked="true"] > div:last-child {{
        border: 3px solid #FF3B30 !important;
        box-shadow: 0 0 5px rgba(255,59,48,0.5) !important;
    }}
    </style>
    """
    st.markdown(style_tag, unsafe_allow_html=True)
    
    # 24개 선택 라디오 (클릭 시 렉 없이 즉시 선택)
    chosen = st.radio(
        label,
        options=PALETTE_24,
        index=PALETTE_24.index(default_color) if default_color in PALETTE_24 else 0,
        key=key_name,
        label_visibility="collapsed"
    )
    return chosen

# 헤드라인 전용 바둑판
text_color = render_palette_board("글자색상", "#000000", "p_text")
shadow_color = render_palette_board("그림자색상", "#AAAAAA", "p_shadow") if use_shadow else "#AAAAAA"
outline_color = render_palette_board("외곽선색상", "#FFFFFF", "p_outline") if use_outline else "#FFFFFF"

# 4. 캡션유도문장
st.markdown("---")
st.subheader("📢 캡션유도문장")
action_text = st.text_input("", value="▶ 상세한 내용은 본문 내용 확인", label_visibility="collapsed")

use_action_outline = st.checkbox("외곽선", value=False, key="chk_act_out")
action_text_color = render_palette_board("글자색상", "#FF0000", "p_act_text")
action_outline_color = render_palette_board("외곽선색상", "#FFFFFF", "p_act_out") if use_action_outline else "#FFFFFF"

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
    margin_x = 80  # 좌우 여백 80px 완벽 보장
    
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
    
    # 1) 헤드라인 출력
    for line in lines:
        if use_shadow:
            draw.text((margin_x + 4, curr_y + 4), line, font=font, fill=shadow_color)
        if use_outline:
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                draw.text((margin_x + dx, curr_y + dy), line, font=font, fill=outline_color)
        draw.text((margin_x, curr_y), line, font=font, fill=text_color)
        curr_y += line_spacing

    # 2) 캡션유도문장 출력 (헤드라인 첫 글자 기준 정렬)
    curr_y += 15
    safe_action_text = action_text.replace("👉", "▶").replace("☞", "▶")
    
    if use_action_outline:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            draw.text((margin_x + dx, curr_y + dy), safe_action_text, font=sub_font, fill=action_outline_color)
    draw.text((margin_x, curr_y), safe_action_text, font=sub_font, fill=action_text_color)

    # 3) 왼쪽 하단 브랜딩 고정
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
