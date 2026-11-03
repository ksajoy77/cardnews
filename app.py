import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont

# 페이지 기본 설정
st.set_page_config(page_title="인스타 캐러셀 프로그램", layout="centered")

# 36색 미니 모눈판 컬러 팔레트 (6x6 격자)
PALETTE_36 = [
    # 1행: 무채색 (블랙 -> 화이트)
    "#000000", "#262626", "#595959", "#8C8C8C", "#BFBFBF", "#FFFFFF",
    # 2행: 레드 / 오렌지 / 핑크
    "#F5222D", "#FA541C", "#FA8C16", "#FF7A45", "#EB2F96", "#FF85C0",
    # 3행: 옐로우 / 골드 / 브라운
    "#FADB14", "#FFC53D", "#D48806", "#874D00", "#614700", "#873800",
    # 4행: 그린 / 에메랄드
    "#52C41A", "#73D13D", "#A0D911", "#13C2C2", "#36CFC9", "#006D75",
    # 5행: 블루 / 네이비 / 퍼플
    "#1677FF", "#4096FF", "#2F54EB", "#597EF7", "#722ED1", "#9254DE",
    # 6행: 감성 파스텔 & 누드톤
    "#FFF0F6", "#FFF2E8", "#FEFFE6", "#E6FFFB", "#F0F5FF", "#F9F0FF"
]

def hex_to_rgb(hex_str):
    """HEX 색상 코드를 RGB 튜플로 변환"""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def is_light_color(hex_str):
    """밝은 색상인지 판별하여 테두리/체크 표시 최적화"""
    r, g, b = hex_to_rgb(hex_str)
    return (r * 0.299 + g * 0.587 + b * 0.114) > 186

# --- CSS 스타일 ---
css_rules = ["""
<style>
/* 맨 아래 생성 버튼 전용 인디핑크 스타일 */
.st-key-generate_card_btn button {
    background-color: #E0838A !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 14px 24px !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    transition: all 0.2s ease-in-out !important;
    margin-top: 25px !important;
    width: 100% !important;
}
.st-key-generate_card_btn button:hover {
    background-color: #D4727A !important;
    color: white !important;
    transform: scale(1.01) !important;
}

/* 초소형 모눈판 타일 스타일 */
div[class*="st-key-swatch_"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 0 !important;
    margin: 0 !important;
}
div[class*="st-key-swatch_"] button {
    width: 30px !important;
    height: 30px !important;
    min-width: 30px !important;
    min-height: 30px !important;
    max-width: 30px !important;
    max-height: 30px !important;
    padding: 0 !important;
    margin: 2px !important;
    border-radius: 4px !important;
    font-size: 11px !important;
    font-weight: bold !important;
    line-height: 30px !important;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.12) !important;
    transition: transform 0.1s ease !important;
}
"""]

# 모눈판 타일 색상 주입
all_prefixes = ["head_text", "head_shadow", "head_stroke", "sub_text", "sub_stroke"]
for p_key in all_prefixes:
    for idx, h_color in enumerate(PALETTE_36):
        light = is_light_color(h_color)
        border_c = "#D9D9D9" if light else "transparent"
        text_c = "#000000" if light else "#FFFFFF"
        css_rules.append(f"""
        .st-key-swatch_{p_key}_{idx} button {{
            background-color: {h_color} !important;
            color: {text_c} !important;
            border: 1px solid {border_c} !important;
        }}
        .st-key-swatch_{p_key}_{idx} button:hover {{
            transform: scale(1.15) !important;
            border: 2px solid #E0838A !important;
        }}
        """)

css_rules.append("</style>")
st.markdown("".join(css_rules), unsafe_allow_html=True)

# 상단 타이틀
st.title("📸 인스타 캐러셀 프로그램")

# 지정 폰트 3종 매핑
font_options = {
    "혜자로운체 (추천)": "GSHYEJAROUNTTF-Bold.ttf",
    "잘난고딕": "JalnanGothicTTF.ttf",
    "그리운 몽토리": "Griun_Mongtori-Rg.ttf"
}

# 기본형 감성 배경색 4종 매핑
bg_color_options = {
    "크림베이지": (247, 243, 235),
    "인디핑크": (245, 235, 235),
    "민트": (235, 245, 242),
    "네이비": (20, 24, 33)
}

def load_font(filename, size):
    """폰트 불러오기"""
    if os.path.exists(filename):
        try:
            return ImageFont.truetype(filename, size)
        except Exception:
            pass
    default_path = "C:/Windows/Fonts/malgunbd.ttf" if os.name == 'nt' else "/System/Library/Fonts/AppleSDGothicNeo.ttc"
    if os.path.exists(default_path):
        return ImageFont.truetype(default_path, size)
    return ImageFont.load_default()

def render_compact_palette(prefix, default_color, label):
    """36색 미니 모눈판 렌더러"""
    if f"{prefix}_color" not in st.session_state:
        st.session_state[f"{prefix}_color"] = default_color

    with st.expander(f"🎨 {label}", expanded=False):
        for row in range(6):
            cols = st.columns(6)
            for col_idx in range(6):
                idx = row * 6 + col_idx
                color_hex = PALETTE_36[idx]
                is_selected = st.session_state[f"{prefix}_color"].upper() == color_hex.upper()
                btn_symbol = "✓" if is_selected else " "
                with cols[col_idx]:
                    if st.button(btn_symbol, key=f"swatch_{prefix}_{idx}"):
                        st.session_state[f"{prefix}_color"] = color_hex
        
        chosen = st.session_state[f"{prefix}_color"]
        st.markdown(
            f"<div style='margin-top:6px; font-size:13px; color:#555;'>"
            f"선택: <span style='display:inline-block;width:12px;height:12px;background-color:{chosen};border-radius:2px;vertical-align:middle;margin-right:4px;border:1px solid #ccc;'></span>"
            f"<code>{chosen}</code></div>", 
            unsafe_allow_html=True
        )
    return st.session_state[f"{prefix}_color"]

# --- [1구역] 헤드라인 기본 설정 ---
col1, col2, col3 = st.columns([1.5, 1, 1.2])
with col1:
    headline_font_name = st.selectbox("🚀 헤드라인 폰트", list(font_options.keys()), index=0)
    headline_font_file = font_options[headline_font_name]
with col2:
    headline_font_size = st.slider("🚀 글자 크기", min_value=40, max_value=90, value=60, step=2)
with col3:
    headline_y_pos = st.slider("🚀 헤드라인 위치(상/하)", min_value=100, max_value=1000, value=750, step=10)

# --- [2구역] 헤드라인 스타일 & 36색 모눈판 ---
h_opt1, h_opt2, h_opt3 = st.columns(3)
with h_opt1:
    use_bold = st.checkbox("폰트 두껍게", value=True)
with h_opt2:
    use_shadow = st.checkbox("그림자 효과", value=False)
with h_opt3:
    use_stroke = st.checkbox("외곽선", value=False)  # 접이식선 -> 외곽선

hc_col1, hc_col2, hc_col3 = st.columns(3)
with hc_col1:
    head_text_color_hex = render_compact_palette("head_text", "#191E28", "글자 색상")
    head_text_color = hex_to_rgb(head_text_color_hex)
with hc_col2:
    head_shadow_color_hex = render_compact_palette("head_shadow", "#000000", "그림자 색상")
    head_shadow_color = hex_to_rgb(head_shadow_color_hex)
with hc_col3:
    head_stroke_color_hex = render_compact_palette("head_stroke", "#FFFFFF", "외곽선 색상")  # 투명색상 -> 외곽선 색상
    head_stroke_color = hex_to_rgb(head_stroke_color_hex)

# 헤드라인 입력창
headline = st.text_area("🚀 헤드라인", value="", height=90)

# --- [3구역] 캡션유도문장 & 스타일 설정 ---
sub_guide_text = st.text_input("🚀 캡션유도문장", value="상세한 내용은 본문 내용 확인")

sub_col1, sub_col2, sub_col3 = st.columns([1, 1, 1])
with sub_col1:
    sub_use_stroke = st.checkbox("외곽선", value=True)  # 옵션접선 -> 외곽선
with sub_col2:
    sub_text_color_hex = render_compact_palette("sub_text", "#000000", "글자 색상")  # 캡처 텍스트색상 -> 글자 색상
    sub_text_color = hex_to_rgb(sub_text_color_hex)
with sub_col3:
    sub_stroke_color_hex = render_compact_palette("sub_stroke", "#FFFFFF", "외곽선 색상")  # 캡션포르선색상 -> 외곽선 색상
    sub_stroke_color = hex_to_rgb(sub_stroke_color_hex)

# --- [4구역] 2x2 격자 레이아웃 ---
row1_left, row1_right = st.columns([1, 1.3])

with row1_left:
    card_type = st.radio("🚀 카드뉴스 디자인 선택", ("기본", "사진형"), horizontal=True, index=0)

with row1_right:
    selected_bg_name = st.radio("🚀 기본형 배경색 선택", list(bg_color_options.keys()), horizontal=True, index=0)

row2_left, row2_right = st.columns([1, 1.3])

with row2_left:
    uploaded_image = st.file_uploader("🚀 사진불러오기", type=["jpg", "jpeg", "png"])

with row2_right:
    st.write("")
    generate_btn = st.button("🚀 카드뉴스 이미지 생성하기", key="generate_card_btn", use_container_width=True)

def draw_styled_text(draw, x, y, text, font, fill_color, bold=False, shadow=False, shadow_c=(0,0,0), stroke=False, stroke_c=(255,255,255)):
    """두껍게, 그림자, 외곽선 효과 렌더링 함수"""
    if shadow:
        draw.text((x + 4, y + 4), text, font=font, fill=shadow_c)

    if stroke:
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            draw.text((x + dx, y + dy), text, font=font, fill=stroke_c)

    if bold:
        for dx, dy in [(1, 0), (0, 1), (1, 1)]:
            draw.text((x + dx, y + dy), text, font=font, fill=fill_color)

    draw.text((x, y), text, font=font, fill=fill_color)

# --- [5구역] 이미지 렌더링 로직 ---
if generate_btn:
    width, height = 1080, 1350
    head_font = load_font(headline_font_file, headline_font_size)
    sub_font = load_font(headline_font_file, 34)
    footer_font = load_font(headline_font_file, 26)

    footer_color_map = {
        "크림베이지": (148, 163, 184), 
        "인디핑크": (148, 163, 184), 
        "민트": (148, 163, 184), 
        "네이비": (100, 116, 139)
    }

    # ==========================================
    # [1] 기본형 레이아웃
    # ==========================================
    if card_type == "기본":
        card = Image.new("RGB", (width, height), color=bg_color_options[selected_bg_name])
        draw = ImageDraw.Draw(card)

        img_y = 120
        if uploaded_image is not None:
            try:
                user_img = Image.open(uploaded_image).convert("RGBA")
                target_w = 940
                target_h = int(user_img.height * (target_w / user_img.width))
                if target_h > 580:
                    target_h = 580
                    target_w = int(user_img.width * (target_h / user_img.height))
                user_img = user_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                
                img_x = (width - user_img.width) // 2
                card.paste(user_img, (img_x, img_y), mask=user_img)
            except Exception:
                pass

        curr_y = headline_y_pos
        if headline.strip():
            for line in headline.split("\n"):
                if line.strip():
                    draw_styled_text(
                        draw, 70, curr_y, line.strip(), head_font, head_text_color,
                        bold=use_bold, shadow=use_shadow, shadow_c=head_shadow_color,
                        stroke=use_stroke, stroke_c=head_stroke_color
                    )
                    curr_y += headline_font_size + 22

        # 캡션유도문장 (사용자 지정 색상 & 외곽선 적용)
        if sub_guide_text.strip():
            draw_styled_text(
                draw, 70, curr_y + 25, sub_guide_text.strip(), sub_font, sub_text_color,
                bold=False, shadow=False, stroke=sub_use_stroke, stroke_c=sub_stroke_color
            )

        draw.text((70, 1260), "@duruduru.page", font=footer_font, fill=footer_color_map[selected_bg_name])

    # ==========================================
    # [2] 사진형 레이아웃
    # ==========================================
    else:
        if uploaded_image is not None:
            bg_raw = Image.open(uploaded_image).convert("RGB")
            bg_ratio = bg_raw.width / bg_raw.height
            t_ratio = width / height
            if bg_ratio > t_ratio:
                new_w = int(bg_raw.height * t_ratio)
                left = (bg_raw.width - new_w) // 2
                bg_cropped = bg_raw.crop((left, 0, left + new_w, bg_raw.height))
            else:
                new_h = int(bg_raw.width / t_ratio)
                top = (bg_raw.height - new_h) // 2
                bg_cropped = bg_raw.crop((0, top, bg_raw.width, top + new_h))
            card = bg_cropped.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        else:
            card = Image.new("RGBA", (width, height), color=(30, 35, 45, 255))

        grad = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(grad)
        grad_start = max(100, headline_y_pos - 150)
        for y in range(grad_start, height):
            alpha = int(225 * ((y - grad_start) / (height - grad_start)))
            g_draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        card = Image.alpha_composite(card, grad)
        draw = ImageDraw.Draw(card)

        curr_y = headline_y_pos
        if headline.strip():
            for line in headline.split("\n"):
                if line.strip():
                    draw_styled_text(
                        draw, 70, curr_y, line.strip(), head_font, head_text_color,
                        bold=use_bold, shadow=use_shadow, shadow_c=head_shadow_color,
                        stroke=use_stroke, stroke_c=head_stroke_color
                    )
                    curr_y += headline_font_size + 22

        # 캡션유도문장 (사용자 지정 색상 & 외곽선 적용)
        if sub_guide_text.strip():
            draw_styled_text(
                draw, 70, curr_y + 25, sub_guide_text.strip(), sub_font, sub_text_color,
                bold=False, shadow=False, stroke=sub_use_stroke, stroke_c=sub_stroke_color
            )

        draw.text((70, 1260), "@duruduru.page", font=footer_font, fill=footer_color_map[selected_bg_name])

    # 결과 저장 및 브라우저 출력
    os.makedirs("output_cards", exist_ok=True)
    save_path = os.path.join("output_cards", "custom_card.png")
    card.save(save_path)

    st.success("🎉 요청하신 스타일로 카드뉴스가 깔끔하게 완성되었습니다!")
    st.image(save_path, caption="완성된 카드뉴스 미리보기", use_container_width=True)