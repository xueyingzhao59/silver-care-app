import streamlit as st
import datetime
import random
import pandas as pd

# 页面配置
st.set_page_config(page_title="颐年乐生活·智慧助老", layout="wide")

# ============ 全局状态初始化 ============
if "font_size" not in st.session_state:
    st.session_state.font_size = "标准"
# 老年食堂状态
if "dinner_mode" not in st.session_state:
    st.session_state.dinner_mode = ""
if "show_food_panel" not in st.session_state:
    st.session_state.show_food_panel = False
if "show_delivery_tip" not in st.session_state:
    st.session_state.show_delivery_tip = False
if "delivery_addr" not in st.session_state:
    st.session_state.delivery_addr = ""
if "select_foods" not in st.session_state:
    st.session_state.select_foods = []
# 定位位置
if "location" not in st.session_state:
    st.session_state.location = "北京市·朝阳区"
# 健康监测数据
if "health_vals" not in st.session_state:
    st.session_state.health_vals = {
        "心率": 72,
        "收缩压": 135,
        "舒张压": 88,
        "血糖": 5.6,
        "血氧": 97,
        "睡眠": "7小时20分"
    }
# 漂浮指引助手状态（核心）
if "guide_step" not in st.session_state:
    st.session_state.guide_step = 0
if "guide_open" not in st.session_state:
    st.session_state.guide_open = True

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
/* 健康卡片样式 */
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
.warning {{color: #ff4d4f; font-weight: bold;}}
.normal {{color: #52c41a;}}
/* 跳转按钮样式 */
.link-btn {{
    display: block;
    text-align: center;
    background: #2E86AB;
    color: white !important;
    padding: 10px;
    border-radius: 8px;
    text-decoration: none;
    font-size: {current_font};
    font-weight: bold;
}}
.link-btn:hover {{background: #236b8a;}}
/* 通话弹窗样式 */
.call-alert {{
    background: #ff3b30;
    color: white;
    padding: 25px;
    border-radius: 16px;
    text-align: center;
    font-size: calc({current_font} + 4px);
    font-weight: bold;
    margin: 15px 0;
}}
/* 外卖下单弹窗样式 */
.order-box {{
    background: #fff;
    border:2px solid #ff9800;
    border-radius:16px;
    padding:25px;
    margin:15px 0;
}}
.delivery-success {{
    background:#00c853;
    color:white;
    border-radius:16px;
    padding:20px;
    text-align:center;
    font-weight:bold;
    font-size: calc({current_font}+4px);
}}
/* 漂浮指引外层容器 */
.float-guide-wrap {{
    position: fixed;
    right: 20px;
    bottom: 30px;
    width: 320px;
    z-index: 99999;
}}
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

# ========== 漂浮豆包指引分步文案 ==========
guide_content = [
    "大家好！我是本页面专属指引助手豆包😊，我会一步一步带领您学会这个老年智慧平台全部功能，点击【下一步】开始教学！",
    "第一步：页面左上角侧边栏设置。您可以切换标准/大号/超大字体方便阅读；还能手动选择您的居住地区，或者点击上方【获取当前真实位置】自动定位您的家！",
    "第二步：页面顶部卡片会显示您的姓名、当前定位地址和今日气温，定位成功后会自动更新为您的真实住址，方便匹配附近社区医院与食堂。",
    "第三步：常用服务第一个蓝色按钮【预约挂号】，点击会自动新开页面跳转医院官网，可在线看病挂号；系统会根据您的地址推荐就近医院。",
    "第四步：点击【老年食堂】按钮，可选择堂食到店吃饭，或外卖配送到家；选外卖可以勾选多款适合老人的清淡菜品，填写家庭地址下单，下单后提示正在配送。",
    "第五步：健康监测区域，模拟智能手环实时同步心率、血压、血糖、血氧、睡眠数据；数值异常会弹出黄色提醒，严重超标系统自动模拟拨打120急救。",
    "第六步：页面下方有一键紧急求助，触发后同时拨打120和家人；下方快速联系可直接呼叫儿子、女儿、社区工作人员，点击即弹出通话提示窗口。",
    "全部功能教学完成！您可以自由使用页面所有功能，忘记操作随时点【重置引导】重新看教程，有不懂的随时查看我的指引~"
]

# ========== 漂浮指引（纯Streamlit原生按钮，点击立刻生效） ==========
if st.session_state.guide_open:
    with st.container():
        st.markdown('<div class="float-guide-wrap">', unsafe_allow_html=True)
        guide_card = st.expander("🤖 豆包智能指引人", expanded=True)
        with guide_card:
            step = st.session_state.guide_step
            st.write(guide_content[step])
            b1, b2, b3 = st.columns(3)
            with b1:
                if st.button("下一步") and step < len(guide_content)-1:
                    st.session_state.guide_step += 1
            with b2:
                if st.button("重置引导"):
                    st.session_state.guide_step = 0
            with b3:
                if st.button("关闭助手"):
                    st.session_state.guide_open = False
        st.markdown('</div>', unsafe_allow_html=True)

# ========== 真实定位JS模块 ==========
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
            const input = window.parent.document.querySelector('input[key="real_loc"]');
            if(input){
                input.value = lat+","+lon;
                input.dispatchEvent(new Event('input'));
            }
        },
        function(err){
            textDom.innerText = "❌ 定位失败，请检查权限";
        }
    );
}
</script>
"""
st.components.v1.html(loc_html, height=150)

# 接收定位经纬度
loc_result = st.text_input("", key="real_loc", label_visibility="hidden")
if loc_result:
    try:
        lat, lon = map(float, loc_result.split(","))
        if 32.10 <= lat <= 32.30 and 119.40 <= lon <= 119.60:
            st.session_state.location = "镇江市-京口区"
        else:
            st.session_state.location = "已获取真实GPS位置"
    except:
        st.session_state.location = "已获取真实GPS位置"

# ========== 侧边栏设置 ==========
st.sidebar.title("⚙️ 功能设置")
st.sidebar.radio("字体大小", ["标准", "大号", "超大号"], key="font_size")
st.sidebar.markdown("---")
st.sidebar.subheader("📍 备用模拟定位")
area_list = ["北京市·朝阳区", "北京市·海淀区", "上海市·浦东新区", "广州市·天河区", "深圳市·南山区","镇江市-京口区"]
selected_area = st.sidebar.selectbox("选择地区", area_list, index=area_list.index(st.session_state.location) if st.session_state.location in area_list else 0)
if st.sidebar.button("一键模拟定位", use_container_width=True):
    st.session_state.location = selected_area
    st.sidebar.success(f"模拟定位：{st.session_state.location}")

# 头部信息卡片
st.markdown(f"""
<div class="card big-font">
👴 王爷爷，{get_greet()}<br>
📍 {st.session_state.location} &nbsp; 🌡️ 24°C 晴
</div>
""", unsafe_allow_html=True)

# ========== 常用服务区域 ==========
st.subheader("常用服务")
col1, col2, col3 = st.columns(3)
with col1:
    # 预约挂号跳转链接
    st.markdown(f'<a href="http://www.jdfy.cn" target="_blank" class="link-btn">🏥 预约挂号</a>', unsafe_allow_html=True)
    # 老年食堂按钮
    if st.button("🍚 老年食堂", use_container_width=True):
        st.session_state.show_food_panel = True
    # 堂食/外卖面板常驻渲染
    if st.session_state.show_food_panel:
        st.session_state.dinner_mode = st.radio("选择用餐方式", ["堂食", "外卖"])
        if st.session_state.dinner_mode == "堂食":
            st.success("🥢 明日菜单：西红柿炒蛋、清蒸鲈鱼、杂粮饭，可直接到店用餐。")
            st.session_state.show_delivery_tip = False
        if st.session_state.dinner_mode == "外卖":
            st.markdown('<div class="order-box big-font">', unsafe_allow_html=True)
            st.subheader("🍱 社区老年食堂外卖点餐")
            food_list = ["清蒸鲈鱼","西红柿炒鸡蛋","清炒西兰花","冬瓜排骨汤","杂粮米饭","小米粥","蒸南瓜","豆腐炖白菜"]
            st.session_state.select_foods = st.multiselect("请勾选需要配送的菜式", food_list, default=st.session_state.select_foods)
            st.session_state.delivery_addr = st.text_input("填写您的家庭配送地址", value=st.session_state.delivery_addr)
            if st.button("✅ 确认下单配送"):
                if len(st.session_state.select_foods) == 0:
                    st.warning("请至少选择一道菜品！")
                elif len(st.session_state.delivery_addr.strip()) < 3:
                    st.warning("请填写完整家庭地址！")
                else:
                    st.session_state.show_delivery_tip = True
            st.markdown('</div>', unsafe_allow_html=True)
    # 下单成功配送提示
    if st.session_state.show_delivery_tip:
        st.markdown("""
        <div class="delivery-success">
        🚚 下单成功！<br>
        菜品：{select}<br>
        配送地址：{addr}<br>
        正在配送中，请留意送餐人员电话！
        </div>
        """.format(select="、".join(st.session_state.select_foods), addr=st.session_state.delivery_addr), unsafe_allow_html=True)
with col2:
    if st.button("💊 用药提醒", use_container_width=True):
        st.info("用药提醒：每日早7:30、晚19:00，药师专线：400-882-1234。")
    if st.button("👨‍⚕️ 上门护理", use_container_width=True):
        st.info("已预约下周一体温测量/康复护理，工作人员将提前致电联系。")
with col3:
    if st.button("🎭 社区活动", use_container_width=True):
        st.info("下周活动：书法班、八段锦、手机课堂，报名热线：010-87654321。")
    if st.button("💳 生活缴费", use_container_width=True):
        st.info("水电燃气线上缴费即将上线，可前往社区服务点线下办理。")

# 健康每日小贴士
tips = ["🌿 夏季午休30分钟，多喝温水，高血压人群按时服药。","🍎 每日吃果蔬，少吃高盐腌制菜。","🚶 饭后散步15分钟平稳血压。","😴 23点前睡觉保护心脑血管。","👂 雨天出门小心滑倒。"]
if "cur_tip" not in st.session_state:
    st.session_state.cur_tip = random.choice(tips)
if st.button("🔄 换一条提醒"):
    st.session_state.cur_tip = random.choice(tips)
st.markdown(f'<div class="tip-box">{st.session_state.cur_tip}</div>', unsafe_allow_html=True)

# ========== 健康监测六宫格卡片 ==========
st.subheader("❤️ 健康监测（手环同步）")
st.write("当前手环实时数据：")
hr = st.number_input("心率（次/分）", min_value=40, max_value=200, value=st.session_state.health_vals["心率"])
sbp = st.number_input("收缩压（mmHg）", min_value=70, max_value=220, value=st.session_state.health_vals["收缩压"])
dbp = st.number_input("舒张压（mmHg）", min_value=40, max_value=120, value=st.session_state.health_vals["舒张压"])
bg = st.number_input("血糖（mmol/L）", min_value=2.0, max_value=20.0, value=st.session_state.health_vals["血糖"], step=0.1)
spo2 = st.number_input("血氧饱和度（%）", min_value=70, max_value=100, value=st.session_state.health_vals["血氧"])
# 同步数据
st.session_state.health_vals["心率"] = hr
st.session_state.health_vals["收缩压"] = sbp
st.session_state.health_vals["舒张压"] = dbp
st.session_state.health_vals["血糖"] = bg
st.session_state.health_vals["血氧"] = spo2

# 健康异常判断
warnings = []
call_120 = False
if hr < 60 or hr > 100:
    warnings.append("⚠️ 心率异常（60-100次/分）")
    if hr < 40 or hr > 150: call_120 = True
if sbp < 90 or sbp > 140 or dbp < 60 or dbp > 90:
    warnings.append("⚠️ 血压异常（90-140/60-90mmHg）")
    if sbp > 180 or dbp > 120 or sbp < 70: call_120 = True
if bg < 3.9 or bg > 6.1:
    warnings.append("⚠️ 血糖异常（3.9-6.1mmol/L）")
    if bg > 13.9 or bg < 2.8: call_120 = True
if spo2 < 95:
    warnings.append("⚠️ 血氧偏低（≥95%正常）")
    if spo2 < 90: call_120 = True

# 两行两列卡片
hc1, hc2 = st.columns(2)
with hc1:
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

# 健康异常提醒
if warnings:
    st.error("⚠️ 健康数据异常提醒：")
    for msg in warnings:
        st.warning(msg)
# 严重异常自动呼叫120弹窗
if call_120:
    st.markdown("""
    <div class="call-alert">
        🚨 身体指标严重异常<br>
        系统正在自动拨打：120 急救中心<br>
        请保持手机畅通，等待医护人员来电！
    </div>
    """, unsafe_allow_html=True)

# 个人病史档案
st.subheader("📋 个人病史档案")
medical_history = [
    {"疾病名称": "高血压", "确诊年份": "2020", "现状": "规律服药，控制良好"},
    {"疾病名称": "轻度关节炎", "确诊年份": "2021", "现状": "注意保暖，偶尔不适"}
]
df_medical = pd.DataFrame(medical_history)
st.dataframe(df_medical, use_container_width=True)

# 一键紧急求助
st.markdown('<div class="emergency">🚨 一键紧急求助 🚨</div>', unsafe_allow_html=True)
if st.button("立即求助", type="primary", use_container_width=True):
    st.markdown("""
    <div class="call-alert">
        🚨 紧急求助已触发<br>
        正在同步拨打：120急救中心 + 紧急联系人（儿子 张三）<br>
        请耐心等待来电！
    </div>
    """, unsafe_allow_html=True)

# 快速联系家人社区
st.subheader("📞 快速联系家人/社区")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("👨 儿子 张三", use_container_width=True):
        st.markdown("""
        <div class="call-alert">
            📞 正在拨打紧急联系人：儿子 张三
        </div>
        """, unsafe_allow_html=True)
with c2:
    if st.button("👩 女儿 李芳", use_container_width=True):
        st.markdown("""
        <div class="call-alert">
            📞 正在拨打紧急联系人：女儿 李芳
        </div>
        """, unsafe_allow_html=True)
with c3:
    if st.button("🏘️ 社区小王", use_container_width=True):
        st.markdown("""
        <div class="call-alert">
            📞 正在拨打社区工作人员：小王
        </div>
        """, unsafe_allow_html=True)

# 底部页脚
st.markdown(f"""
<div style="text-align:center; background:#f0f4f9; padding:12px; border-radius:40px; font-size: {current_font};">
📞 社区热线：010-12345678 &nbsp; | &nbsp; 急救：120
</div>
""", unsafe_allow_html=True)
st.markdown("<hr><p style='text-align:center; color:#888; text-align:center;'>🏡 颐年乐生活 · 用心陪伴</p>", unsafe_allow_html=True)
