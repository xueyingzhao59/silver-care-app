import streamlit as st
import datetime
import random

st.set_page_config(page_title="银龄生活·智慧助老", layout="wide")

st.markdown("""
<style>
.big-font {font-size: 22px !important;}
.card {background: #fff; border-radius: 20px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);}
.emergency {background: #e63946; color: #fff; font-size: 22px; font-weight: bold; padding: 15px; border-radius: 10px; text-align: center;}
.tip-box {background: #fef9e3; padding: 15px; border-radius: 15px; border-left: 5px solid #f4a261; font-size: 18px;}
</style>
""", unsafe_allow_html=True)

def get_greet():
    h = datetime.datetime.now().hour
    if h < 12:
        return "早上好 🌞"
    elif h < 18:
        return "下午好 ☀️"
    else:
        return "晚上好 🌙"

st.markdown(f"""
<div class="card big-font">
👴 王爷爷，{get_greet()}<br>
📍 北京市·朝阳区 &nbsp; 🌡️ 24°C 晴
</div>
""", unsafe_allow_html=True)

st.subheader("常用服务")
c1,c2,c3 = st.columns(3)
with c1:
    if st.button("🏥 预约挂号", use_container_width=True):
        st.info("即将为您跳转附近医院挂号平台，或拨打114协助挂号。")
    if st.button("🍚 老年食堂", use_container_width=True):
        st.info("老年食堂：明日菜单：西红柿炒蛋、清蒸鲈鱼、杂粮饭，可联系网格员预订。")
with c2:
    if st.button("💊 用药提醒", use_container_width=True):
        st.info("用药提醒：每日早7:30、晚19:00，药师专线：400-882-1234。")
    if st.button("👨‍⚕️ 上门护理", use_container_width=True):
        st.info("已预约下周一体温测量/康复按摩，工作人员将提前联系。")
with c3:
    if st.button("🎭 社区活动", use_container_width=True):
        st.info("下周活动：书法班、八段锦、手机课堂，报名：010-87654321。")
    if st.button("💳 生活缴费", use_container_width=True):
        st.info("水电燃气线上缴费即将开放，可前往社区服务点代办。")

st.subheader("健康小贴士")
tips = [
    "🌿 夏季宜午休30分钟，多喝水，高血压长辈按时服药。",
    "🍎 每日吃苹果补充维生素，少吃高盐腌制品。",
    "🚶 饭后散步15分钟，帮助消化、稳定血糖。",
    "😴 23点前入睡，保证7小时睡眠，呵护心脑血管。",
    "👂 定期检查视听能力，雨天出行注意防滑。"
]
if "cur_tip" not in st.session_state:
    st.session_state.cur_tip = random.choice(tips)
if st.button("🔄 换一条提醒"):
    st.session_state.cur_tip = random.choice(tips)
st.markdown(f'<div class="tip-box">{st.session_state.cur_tip}</div>', unsafe_allow_html=True)

st.markdown('<div class="emergency">🚨 一键紧急求助 🚨</div>', unsafe_allow_html=True)
if st.button("立即求助", type="primary", use_container_width=True):
    st.error("【紧急求助】正在联系紧急联系人 & 120急救中心，请保持电话畅通！")

st.subheader("📞 快速联系家人/社区")
cc1,cc2,cc3 = st.columns(3)
with cc1:
    st.button("👨 儿子 张三", use_container_width=True)
with cc2:
    st.button("👩 女儿 李芳", use_container_width=True)
with cc3:
    st.button("🏘️ 社区小王", use_container_width=True)

st.markdown("""
<div style="text-align:center; background:#f0f4f9; padding:12px; border-radius:40px; font-size:18px;">
📞 社区热线：010-12345678 &nbsp; | &nbsp; 急救：120
</div>
""", unsafe_allow_html=True)
st.markdown("<hr><p style='text-align:center; color:#888;'>🏡 银龄生活 · 用心陪伴</p>", unsafe_allow_html=True)
