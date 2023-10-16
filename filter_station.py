import pandas as pd
import weather

if __name__ == "__main__":
    weather_station = pd.read_csv("data\\weather_station.csv")
    no_shineshine = ['五分山雷達站', '墾丁雷達站', '山佳', '坪林', '四堵', '泰平', '福山', '桶後', '石碇', '火燒寮', '瑞芳', '科教館', 
                     '大坪', '五指山', '福隆', '雙溪', '富貴角', '三和', '金山', '鼻頭角', '三貂角', '社子', '天母', '內湖', '大屯山', 
                     '三峽', '信義', '文山', '新莊', '三芝', '八里', '蘆洲', '土城', '鶯歌', '中和', '汐止', '永和', '五分山', '平等', 
                     '林口', '松山', '深坑', '福山植物園', '五股', '屈尺', '白沙灣', '三重', '石牌', '野柳', '淡水觀海', '石門', '水湳洞', 
                     '六塊厝', '田寮', '板橋', '澳底', '七堵', '基隆嶼', '大武崙', '八斗子', '暖暖', '復興', '桃園', '八德', '觀音', 
                     '蘆竹', '大溪', '平鎮', '楊梅', '龍潭', '龜山', '中壢', '大溪永福', '竹圍', '中大臨海站', '觀音工業區', '新興坑尾', 
                     '梅花', '峨眉', '打鐵坑', '橫山', '雪霸', '竹東', '寶山', '新豐', '湖口', '新竹市東區', '海天一線', '香山濕地', '外湖', 
                     '關西', '竹南', '南庄', '大湖', '後龍', '明德', '通霄', '馬都安', '頭份', '造橋', '苗栗', '銅鑼', '卓蘭', '西湖', '獅潭', 
                     '苑裡', '大河', '高鐵苗栗', '三義', '海埔', '通霄漁港', '龍鳳', '雪山圈谷', '石岡', '中坑', '審馬陣', '南湖圈谷', '東勢', '梨山', '大甲', 
                     '大坑', '中竹林', '神岡', '大安', '后里', '豐原', '大里', '潭子', '清水', '外埔', '龍井', '烏日', '西屯', '南屯', '新社', '大雅(中科園區)', 
                     '桃山', '雪山東峰', '烏石坑', '松柏', '溫寮', '臺中電廠', '霧峰', '芬園', '鹿港', '員林', '溪湖', '溪州', '二林', '大城', '福興', '秀水', 
                     '埔鹽', '埔心', '田尾', '埤頭', '北斗', '社頭', '芳苑', '二水', '伸港', '線西', '花壇', '永靖', '竹塘', '防潮門', '福寶', '三豐', '埔里', 
                     '中寮', '草屯', '昆陽', '神木村', '合歡山', '廬山', '信義', '鳳凰', '竹山', '水里', '魚池', '集集', '仁愛', '名間', '國姓', '南投', '梅峰',
                    '萬大林道', '玉山風口', '小奇萊', '奇萊稜線', '草嶺', '崙背', '四湖', '宜梧', '虎尾', '土庫', '斗六', '北港', '西螺', '褒忠', '二崙', '大埤', 
                    '斗南', '林內', '莿桐', '元長', '水林', '臺西', '蔦松', '棋山', '高鐵雲林', '雲林東勢', '箔子寮', '馬頭山', '東後寮', '奮起湖', '中埔', '朴子', 
                    '溪口', '大林', '太保', '水上', '竹崎', '東石', '番路', '嘉義市東區', '六腳', '布袋', '民雄', '嘉義梅山', '鹿草', '新港', '茶山', '里佳', '達邦', 
                    '表湖', '新美', '好美里', '鯤鯓國小', '城西', '四草', '蘆竹溝', '蚵寮', '曾文', '北寮', '王爺宮', '大內', '善化', '玉井', '安南', '崎頂', '虎頭埤', 
                    '新市', '媽廟', '尾寮山', '阿禮', '瑪家', '三地門', '鹽埔', '屏東', '赤山', '潮州', '來義', '春日', '琉球嶼', '檳榔', '車城', '牡丹', '貓鼻頭', '大漢山',
                    '高樹', '長治', '九如', '崁頂', '佳冬', '新埤', '新園', '麟洛', '南州', '里港', '舊泰武', '墾雷', '東港', '竹田', '枋寮', '楓港', '佳樂水', '墾丁', '枋山',
                    '龍磐', '旭海', '大坪頂', '獅子', '四林格山', '南仁湖', '保力', '滿州', '九棚', '丹路', '內獅', '白鷺', '高士', '牡丹池山', '林邊', '鼻頭', '興海', '後壁湖', 
                    '山海', '竹坑', '下寮', '塭仔', '萬丹', '加祿堂', '下馬', '太麻里', '知本', '鹿野', '綠島', '池上', '向陽', '紅石', '大溪山', '金崙', '東河', '長濱', '南田', 
                    '關山', '蘭嶼高中', '蘭嶼燈塔', '金峰嘉蘭', '延平', '石寧山', '七塊厝', '香蘭', '加津林', '勝林山', '山豬窟', '歷坵', '檳榔四格山', '金崙山', '都歷', '瑞和', 
                    '知本（水試所）', '土?', '達仁林場', '大禹嶺', '天祥', '鯉魚潭', '西林', '光復', '月眉山', '水源', '和中', '大坑', '水璉', '鳳林山', '加路蘭山', ' 豐濱', '靜浦', 
                    '富里', '雙連埤', '礁溪', '玉蘭', '太平山', '南山', '龜山島', '東澳', '南澳', '五結', '頭城', '大礁溪', '北關', '三星', '內城', '冬山', '羅東', '鶯子嶺', '翠峰湖', 
                    '大福', '坪林石牌', '員山', '土場', '鴛鴦湖', '多加屯', '白嶺', '西德山', '西帽山', '樟樹山', '桃源谷', '大溪漁港', '石城', '淡江大學蘭陽校園', '蘇澳', '壯圍', '復興', 
                    '甲仙', '月眉', '美濃', '溪埔', '內門', '古亭坑', '阿公店', '鳳山', '鳳森', '新興', '阿蓮', '梓官', '', '花嶼', '金沙', '金寧', '烏坵', '東河', '下營', '佳里', '臺南市北區', 
                    '臺南市南區', '麻豆', '官田', '西港', '安定', '仁德', '關廟', '山上', '安平', '左鎮', '白河', '學甲', '鹽水', '關子嶺', '新營', '後壁', '將軍', '北門', '鹿寮', '七股', '柳營', 
                    '明里', '佳心', '玉里', '舞鶴', '富源', '東華', '吉安光華', '鳳林', '卓溪', '新城', '富世', '萬榮', '瑞穗', '和平林道', '和平', '瑞穗林道', '蕃薯寮', '德武', '赤柯山', '東里', '清水斷崖', 
                    '清水林道', '安通山', '下盆', '石碇服務區', '坪林交控', '四十份', '關渡', '國三N016K', '國一N039K', '水尾', '新埔', '鳥嘴山', '白蘭', '太閣南', '飛鳳山', '外坪(五指山)', '象鼻', '松安', 
                    '鳳美', '新開', '南勢', '南礦', '南勢山', '南湖', '八卦', '馬拉邦山', '泰安', '公館', '國三N149K', '國一N128K', '上谷關', '稍來', '新伯公', '雪嶺', '桐林', '白冷', '白毛台', '龍安', 
                    '伯公龍', '慶福山', '清水林', '德基', '下水埔', '國一S218K', '翠峰', '國三N238K', '瑞岩', '清流', '長豐', '雙冬', '六分寮', '阿眉', '萬大', '武界', '丹大', '和社', '溪頭', 
                    '大鞍', '桶頭', '卡奈托灣', '青雲', '中心崙', '蘆竹湳', '樟湖', '九份二山', '外大坪', '鯉潭', '北坑', '埔中', '豐丘', '西巒', '奧萬大', '楓樹林', '新興橋', '凌霄', 
                    '翠華', '新高口', '望鄉山', '杉林溪', '大尖山', '線浸林道', '國六W023K', '口湖', '龍美', '菜瓜坪', '獨立山', '頭凍', '石磐龍', '瑞里', '十字', '國三N285K', '沙崙',
                    '環湖', '大棟山', '關山', '楠西', '東山服務區', '口社', '上德文', '力里', '石門山', '西大武山', '龍泉', '摩天', '華源', '金峰', '豐南', '利嘉', '南美山', '壽卡', '利嘉林道', '都蘭',
                    '洛韶', '慈恩', '布洛灣', '中興', '大觀', '太安', '大農', '龍澗', '高寮', '太魯閣', '牛鬥', '寒溪', '東澳嶺', '觀音海岸', 
                    '思源', '粉鳥林', '達卡努瓦', '排雲', '南天池', '梅山', '小關山', '高中', '御油山', '大津', '尖山', '吉東', '溪南(特生中心)', 
                    '新發', '藤枝', '多納林道', '國三S383K', '東原', '紅葉', 
'立山', '三棧', '壽豐', '銅門', '荖溪', '中平林道']
    
    # for ws in weather_station:
    #     df = weather.get_month_data(ws, 2023,9)['SunShine']
    #     print(ws)
    #     if df.isna().all():
    #         no_shineshine.append(ws)


    weather_station = weather_station[~weather_station['站名'].isin(no_shineshine)]
    weather_station.to_csv("./data/weather_srarion_with_sunshine.csv")