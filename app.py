import streamlit as st
import datetime
import random
import pandas as pd

# 页面配置
st.set_page_config(page_title="颐年乐生活·智慧助老", layout="wide")

# ============ 状态初始化 ============
if "font_size" not in st.session_state:
    st.session_state.font_size = "标准"
if "dinner_mode" not in st.session_state:
    st.session_state.dinner_mode = "堂食"
if "delivery_addr" not in st.session_state:
    st.session_state.delivery_addr = ""
if "location" not in st.session_state:
    st.session_state.location = "北京市·朝阳区"
# 新增：健康数据状态（用于提醒功能）
if "health_vals" not in st.session_state:
    st.session_state.health_vals = {
        "心率": 72,
        "收缩压": 135,
        "舒张压": 88,
        "血糖": 5.6,
        "血氧": 97,
        "睡眠": "7小时20分"
    }

# ============ 字体配置 ============
font_dict = {
    "标准": "18px",
    "大号": "22px",
    "超大号": "26px"
}
current_font = font_dict[st.session_state.font_size]

# ============ 全局样式 ============
st.markdown(f"""
<style>
.big-font {{font-size: {current_font} !important;}}
.card {{background: #fff; border-radius: 20px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);}}
.emergency {{background: #e63946; color: #fff; font-size: {current_font}; font-weight: bold; padding: 15px; border-radius: 10px; text-align: center;}}
.tip-box {{background: #fef9e3; padding: 15px; border-radius: 15px; border-left: 5px solid #f4a261; font-size: {current_font};}}
.guide-box {{background: #eef5ff; padding: 15px; border-radius: 15px; margin: 10px 0; border: 1px solid #4080ff;}}
.loc-box {{background:#e8f4f8; padding:15px; border-radius:15px; margin:10px 0;}}
/* 新增：健康卡片样式，模仿你给的APP界面 */
.health-card {{
    background: #fff;
    border-radius: 15px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}
.health-icon {{
    width:40px; height:40px;
    border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    color:white; font-weight:bold;
}}
/* 异常提醒样式 */
.warning {{color: #ff4d4f; font-weight: bold;}}
.normal {{color: #52c41a;}}
</style>
""", unsafe_allow_html=True)

# ============ 问候语 ============
def get_greet():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "早上好 🌞"
    elif hour < 18:
        return "下午好 ☀️"
    else:
        return "晚上好 🌙"

# ========== 核心：Streamlit 内嵌 JS 真实定位 ==========
st.subheader("📍 真实位置获取")
loc_html = """
<div class="loc-box">
<button onclick="getRealLocation()" style="font-size:18px;padding:8px 20px;">🔍 获取当前真实位置</button>
<p id="loc_text">点击按钮，允许位置权限</p>
</div>

<script>
function getRealLocation(){
    const textDom = document.getElementById("loc_text");
    if(!navigator.geolocation){
        textDom.innerText = "❌ 浏览器不支持定位";
        return;
    }
    textDom.innerText = "正在定位...请允许权限";
    navigator.geolocation.getCurrentPosition(
        function(pos){
            let lat = pos.coords.latitude.toFixed(4);
            let lon = pos.coords.longitude.toFixed(4);
            textDom.innerHTML = `✅ 定位成功<br>纬度：${lat} &nbsp; 经度：${lon}<br>已自动更新页面地址`;
            window.parent.document.querySelector("input[data-testid='stTextInput']").value = lat+","+lon;
            window.parent.document.querySelector("input[data-testid='stTextInput']").dispatchEvent(new Event('input'));
        },
        function(err){
            textDom.innerText = "❌ 定位失败，请检查权限";
        }
    );
}
</script>
"""
st.components.v1.html(loc_html, height=150)

# 接收JS传来的定位经纬度（隐藏输入框）
loc_result = st.text_input("", key="real_loc", label_visibility="hidden")
if loc_result:
    try:
        lat, lon = map(float, loc_result.split(","))
        if 32.10 <= lat <= 32.30 and 119.40 <= lon <= 119.60:
            st.session_state.location = "江苏省镇江市京口区"
        else:
            st.session_state.location = "已获取真实GPS位置"
    except:
        st.session_state.location = "已获取真实GPS位置"

# ========== 侧边栏：字体 + 备用模拟定位 ==========
st.sidebar.title("⚙️ 功能设置")
st.sidebar.radio("字体大小", ["标准", "大号", "超大号"], key="font_size")

st.sidebar.markdown("---")
st.sidebar.subheader("📍 备用模拟定位")
area_list = ["北京市·朝阳区", "北京市·海淀区", "上海市·浦东新区", "广州市·天河区", "深圳市·南山区", "江苏省镇江市京口区"]
selected_area = st.sidebar.selectbox("选择地区", area_list, index=area_list.index(st.session_state.location) if st.session_state.location in area_list else 0)
if st.sidebar.button("一键模拟定位", use_container_width=True):
    st.session_state.location = selected_area
    st.sidebar.success(f"模拟定位：{st.session_state.location}")

# 头部信息
st.markdown(f"""
<div class="card big-font">
👴 王爷爷，{get_greet()}<br>
📍 {st.session_state.location} &nbsp; 🌡️ 24°C 晴
</div>
""", unsafe_allow_html=True)

# ========== 常用服务 ==========
st.subheader("常用服务")
col1, col2, col3 = st.columns(3)

with col1:
    # 👉 这里是你可以替换的预约挂号链接
    TARGET_URL = "https://xxx.com"
    st.markdown(f'<a href="{TARGET_URL}" target="_blank" class="link-btn">🏥 预约挂号</a>', unsafe_allow_html=True)

    if st.button("🍚 老年食堂", use_container_width=True):
        st.session_state.dinner_mode = st.radio("选择用餐方式", ["堂食", "外卖"],
                                               index=["堂食","外卖"].index(st.session_state.dinner_mode))
        if st.session_state.dinner_mode == "堂食":
            st.success("🥢 明日菜单：西红柿炒蛋、清蒸鲈鱼、杂粮饭，可直接到店用餐。")
        else:
            st.session_state.delivery_addr = st.text_input("请输入送餐地址：", value=st.session_state.delivery_addr)
            st.success(f"🚚 外卖已登记，明日菜单将送至：{st.session_state.delivery_addr}")

with col2:
    if st.button("💊 用药提醒", use_container_width=True):
        st.info("用药提醒：每日早7:30、晚19:00，药师专线：400-882-1234。")
    if st.button("👨‍⚕️ 上门护理", use_container_width=True):
        st.info("已预约下周一体温测量/康复按摩，工作人员将提前联系。")

with col3:
    if st.button("🎭 社区活动", use_container_width=True):
        st.info("下周活动：书法班、八段锦、手机课堂，报名：010-87654321。")
    if st.button("💳 生活缴费", use_container_width=True):
        st.info("水电燃气线上缴费即将开放，可前往社区服务点代办。")

# 健康小贴士
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

# ========== 重点：按你给的APP界面，改造健康监测模块 ==========
st.subheader("❤️ 健康监测（手环同步）")

# 模拟手环数据输入框（可后续对接真实设备）
st.write("当前手环数据：")
hr = st.number_input("心率（次/分）", min_value=40, max_value=200, value=st.session_state.health_vals["心率"])
sbp = st.number_input("收缩压（mmHg）", min_value=70, max_value=220, value=st.session_state.health_vals["收缩压"])
dbp = st.number_input("舒张压（mmHg）", min_value=40, max_value=120, value=st.session_state.health_vals["舒张压"])
bg = st.number_input("血糖（mmol/L）", min_value=2.0, max_value=20.0, value=st.session_state.health_vals["血糖"], step=0.1)
spo2 = st.number_input("血氧饱和度（%）", min_value=70, max_value=100, value=st.session_state.health_vals["血氧"])

# 更新状态
st.session_state.health_vals["心率"] = hr
st.session_state.health_vals["收缩压"] = sbp
st.session_state.health_vals["舒张压"] = dbp
st.session_state.health_vals["血糖"] = bg
st.session_state.health_vals["血氧"] = spo2

# 异常判断 + 提醒逻辑
warnings = []
call_120 = False

# 心率异常
if hr < 50 or hr > 100:
    warnings.append("⚠️ 心率异常（正常范围：60-100次/分）")
    if hr < 40 or hr > 150:
        call_120 = True

# 血压异常
if sbp < 90 or sbp > 140 or dbp < 60 or dbp > 90:
    warnings.append("⚠️ 血压异常（正常范围：收缩压90-140/舒张压60-90mmHg）")
    if sbp > 180 or dbp > 120 or sbp < 70:
        call_120 = True

# 血糖异常
if bg < 3.9 or bg > 6.1:
    warnings.append("⚠️ 血糖异常（正常范围：3.9-6.1mmol/L）")
    if bg > 13.9 or bg < 2.8:
        call_120 = True

# 血氧异常
if spo2 < 95:
    warnings.append("⚠️ 血氧偏低（正常应≥95%）")
    if spo2 < 90:
        call_120 = True

# 显示卡片布局（模仿你给的APP界面）
hc1, hc2 = st.columns(2)

with hc1:
    # 睡眠卡片
    st.markdown("""
    <div class="health-card">
        <div style="display:flex; align-items:center;">
            <div class="health-icon" style="background:#722ed1;">🛏️</div>
            <div style="margin-left:15px;">
                <div style="font-weight:bold; font-size:20px;">睡眠</div>
                <div style="color:#666;">探索您的睡眠动物</div>
            </div>
        </div>
        <div style="margin-top:15px; display:flex; justify-content:space-between; color:#999;">
            <span>有待提高</span>
            <span>优</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 血压卡片
    st.markdown(f"""
    <div class="health-card">
        <div style="display:flex; align-items:center;">
            <div class="health-icon" style="background:#ff4d4f;">💧</div>
            <div style="margin-left:15px;">
                <div style="font-weight:bold; font-size:20px;">血压</div>
                <div style="color:#666;">佩戴设备后测量</div>
            </div>
        </div>
        <div style="margin-top:15px; display:flex; justify-content:space-between; color:#999;">
            <span>偏低</span>
            <span>偏高</span>
        </div>
        <div style="margin-top:10px; font-size:18px;">
            <span class="{'warning' if sbp>140 or sbp<90 or dbp>90 or dbp<60 else 'normal'}">{sbp}/{dbp} mmHg</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 血氧卡片
    st.markdown(f"""
    <div class="health-card">
        <div style="display:flex; align-items:center;">
            <div class="health-icon" style="background:#ff4d4f;">O₂</div>
            <div style="margin-left:15px;">
                <div style="font-weight:bold; font-size:20px;">血氧饱和度</div>
                <div style="color:#666;">佩戴设备后测量</div>
            </div>
        </div>
        <div style="margin-top:10px; font-size:18px;">
            <span class="{'warning' if spo2<95 else 'normal'}">{spo2}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with hc2:
    # 心率卡片
    st.markdown(f"""
    <div class="health-card">
        <div style="display:flex; align-items:center;">
            <div class="health-icon" style="background:#ff4d4f;">❤️</div>
            <div style="margin-left:15px;">
                <div style="font-weight:bold; font-size:20px;">心率</div>
                <div style="color:#666;">佩戴设备后测量</div>
            </div>
        </div>
        <div style="margin-top:15px; display:flex; justify-content:space-between; color:#999;">
            <span>00:00</span>
            <span>24:00</span>
        </div>
        <div style="margin-top:10px; font-size:18px;">
            <span class="{'warning' if hr>100 or hr<60 else 'normal'}">{hr} 次/分</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 血糖卡片
    st.markdown(f"""
    <div class="health-card">
        <div style="display:flex; align-items:center;">
            <div class="health-icon" style="background:#ff4d4f;">🩸</div>
            <div style="margin-left:15px;">
                <div style="font-weight:bold; font-size:20px;">血糖</div>
                <div style="color:#666;">记录您的血糖数据</div>
            </div>
        </div>
        <div style="margin-top:15px; display:flex; justify-content:space-between; color:#999;">
            <span>00:00</span>
            <span>24:00</span>
        </div>
        <div style="margin-top:10px; font-size:18px;">
            <span class="{'warning' if bg>6.1 or bg<3.9 else 'normal'}">{bg} mmol/L</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 显示所有异常提醒
if warnings:
    st.error("⚠️ 健康数据异常提醒：")
    for msg in warnings:
        st.warning(msg)

# 严重异常时自动拨打120（课堂演示版，显示弹窗提示）
if call_120:
    st.markdown("""
    <div style="background:#ff4d4f; color:white; padding:20px; border-radius:10px; text-align:center; font-size:22px; font-weight:bold;">
        🚨 严重异常！已自动拨打 120 急救电话，请保持电话畅通！
    </div>
    """, unsafe_allow_html=True)

# ========== 个人病史档案 ==========
st.subheader("📋 个人病史档案")
medical_history = [
    {"疾病名称": "高血压", "确诊年份": "2020", "现状": "规律服药，控制良好"},
    {"疾病名称": "轻度关节炎", "确诊年份": "2021", "现状": "注意保暖，偶尔不适"}
]
df_medical = pd.DataFrame(medical_history)
st.dataframe(df_medical, use_container_width=True)

# 紧急求助
st.markdown('<div class="emergency">🚨 一键紧急求助 🚨</div>', unsafe_allow_html=True)
if st.button("立即求助", type="primary", use_container_width=True):
    st.error("【紧急求助】正在联系紧急联系人 & 120急救中心，请保持电话畅通！")

# 快速联系
st.subheader("📞 快速联系家人/社区")
c1, c2, c3 = st.columns(3)
with c1:
    st.button("👨 儿子 张三", use_container_width=True)
with c2:
    st.button("👩 女儿 李芳", use_container_width=True)
with c3:
    st.button("🏘️ 社区小王", use_container_width=True)

# 底部
st.markdown(f"""
<div style="text-align:center; background:#f0f4f9; padding:12px; border-radius:40px; font-size: {current_font};">
📞 社区热线：010-12345678 &nbsp; | &nbsp; 急救：120
</div>
""", unsafe_allow_html=True)
st.markdown("<hr><p style='text-align:center; color:#888;'>🏡 颐年乐生活 · 用心陪伴</p>", unsafe_allow_html=True)
