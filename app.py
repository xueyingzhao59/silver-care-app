import streamlit as st
import datetime
import random
import pandas as pd

# 页面配置
st.set_page_config(page_title="颐年乐生活·智慧助老", layout="wide")

# 状态初始化
if "font_size" not in st.session_state:
    st.session_state.font_size = "标准"
if "dinner_mode" not in st.session_state:
    st.session_state.dinner_mode = "堂食"
if "delivery_addr" not in st.session_state:
    st.session_state.delivery_addr = ""
# 定位：优先真实定位，默认模拟地址
if "location" not in st.session_state:
    st.session_state.location = "北京市·朝阳区"

# 字体配置
font_dict = {
    "标准": "18px",
    "大号": "22px",
    "超大号": "26px"
}
current_font = font_dict[st.session_state.font_size]

# 全局样式
st.markdown(f"""
<style>
.big-font {{font-size: {current_font} !important;}}
.card {{background: #fff; border-radius: 20px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);}}
.emergency {{background: #e63946; color: #fff; font-size: {current_font}; font-weight: bold; padding: 15px; border-radius: 10px; text-align: center;}}
.tip-box {{background: #fef9e3; padding: 15px; border-radius: 15px; border-left: 5px solid #f4a261; font-size: {current_font};}}
.guide-box {{background: #eef5ff; padding: 15px; border-radius: 15px; margin: 10px 0; border: 1px solid #4080ff;}}
.loc-box {{background:#e8f4f8; padding:15px; border-radius:15px; margin:10px 0;}}
</style>
""", unsafe_allow_html=True)

# 问候语
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
# 嵌入HTML+JS定位组件，获取经纬度并传回Streamlit
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
            // 把定位结果传给Streamlit
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
    st.session_state.location = "已获取真实GPS位置"

# ========== 侧边栏：字体 + 备用模拟定位 ==========
st.sidebar.title("⚙️ 功能设置")
st.sidebar.radio("字体大小", ["标准", "大号", "超大号"], key="font_size")

st.sidebar.markdown("---")
st.sidebar.subheader("📍 备用模拟定位")
area_list = ["北京市·朝阳区", "北京市·海淀区", "上海市·浦东新区", "广州市·天河区", "深圳市·南山区"]
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

# 常用服务
st.subheader("常用服务")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏥 预约挂号", use_container_width=True):
        now_loc = st.session_state.location
        if "朝阳区" in now_loc:
            hospital = "北京市朝阳区第一医院"
            app_name = "朝阳医院挂号小程序"
        elif "海淀区" in now_loc:
            hospital = "北京市海淀区人民医院"
            app_name = "海淀健康挂号平台"
        elif "浦东新区" in now_loc:
            hospital = "上海市浦东中心医院"
            app_name = "浦东就医服务"
        elif "天河区" in now_loc:
            hospital = "广州市天河区人民医院"
            app_name = "广州健康通"
        elif "南山区" in now_loc:
            hospital = "深圳市南山人民医院"
            app_name = "深圳健康服务"
        else:
            hospital = "就近综合医院"
            app_name = "全民健康挂号"

        st.markdown(f"""
        <div class="guide-box big-font">
        📍 当前位置：{now_loc}<br>
        🏥 推荐就近医院：{hospital}<br>
        💡 请打开微信，搜索小程序：<b>{app_name}</b> 完成线上预约
        </div>
        """, unsafe_allow_html=True)

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

# 健康监测
st.subheader("❤️ 健康监测（手环同步）")
health_data = {
    "心率": "72 次/分",
    "收缩压": "135 mmHg",
    "舒张压": "88 mmHg",
    "血糖": "5.6 mmol/L",
    "血氧": "97%",
    "压力指数": "正常",
    "睡眠时长": "7小时20分"
}
df_health = pd.DataFrame(list(health_data.items()), columns=["项目", "当前数值"])
st.dataframe(df_health, use_container_width=True)

# 病史档案
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
