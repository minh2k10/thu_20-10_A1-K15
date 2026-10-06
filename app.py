import re
import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ==========================================
# CẤU HÌNH ĐƯỜNG DẪN ẢNH CỐ ĐỊNH
# ==========================================
CLASS_BG_URL = "/static/backgrounds/tap_the_lop.jpg"
BOYS_AVATAR_URL = "/static/avatars/cac_ban_nam.jpg"


def format_display_name(text):
    """Chuẩn hóa định dạng tên hiển thị (Viết hoa chữ cái đầu)"""
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text.title()


# ==========================================
# DANH SÁCH 30 LỜI CHÚC & CẢM ƠN DÀI
# ==========================================
WISH_TEMPLATES = [
    # 1
    "Gửi tới {name} những lời chúc ấm áp và tuyệt vời nhất nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Chúc bạn luôn rạng rỡ, xinh đẹp, giữ trọn nụ cười tươi tắn trên môi và tràn đầy năng lượng tích cực. "
    "Mong rằng chặng đường phía trước của bạn sẽ luôn ngập tràn niềm vui, thành công trong học tập và gặp thật nhiều may mắn, yêu thương trong cuộc sống! ✨💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 2
    "Gửi tới {name} - một mảnh ghép vô cùng đáng yêu của tập thể A1K15!\n\n"
    "Nhân ngày 20/10, chúc bạn luôn giữ vững phong độ xinh đẹp, tự tin và tỏa sáng theo cách của riêng mình. "
    "Cảm ơn bạn vì đã luôn đồng hành, sẻ chia và mang đến nhiều kỉ niệm đẹp cho lớp. Chúc bạn một ngày tràn ngập hoa, quà và những niềm vui trọn vẹn nhất! 🌸✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 3
    "Chúc mừng ngày Phụ nữ Việt Nam 20/10 gửi tới {name}!\n\n"
    "Cảm ơn sự xuất hiện của bạn đã giúp bầu không khí A1K15 luôn ấm áp và ngập tràn niềm vui. "
    "Chúc bạn ngày hôm nay nhận được thật nhiều tình yêu thương, ngọt ngào và quà cáp. Hãy luôn giữ vững nụ cười rạng rỡ, học giỏi và gặp thật nhiều may mắn nhé! 💕🌷\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 4
    "Gửi người bạn xinh xắn {name} nhân ngày 20/10!\n\n"
    "Chúc bạn ngày càng rạng rỡ, học tập đạt thật nhiều điểm số cao và luôn đạt được những mục tiêu mình mơ ước. "
    "Cảm ơn bạn đã luôn nhiệt tình, dễ thương và đồng hành cùng tập thể lớp. Mong mọi điều bình an và hạnh phúc nhất sẽ luôn mỉm cười với bạn! ✨💝\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 5
    "Chúc mừng {name} nhân ngày 20/10 thật nhiều niềm vui và ý nghĩa!\n\n"
    "Cảm ơn bạn vì đã luôn mang tới năng lượng tích cực và sự ấm áp cho mọi người xung quanh. "
    "Chúc bạn luôn xinh tươi như những bông hoa mùa xuân, luôn kiên cường, tự tin bước đi trên con đường tương lai và luôn là cô gái hạnh phúc nhất! 🌹💫\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 6
    "Thân gửi {name} nhân ngày phụ nữ Việt Nam 20/10!\n\n"
    "Chúc bạn có một ngày kỉ niệm thật ngọt ngào bên gia đình, bạn bè và những người thân yêu. "
    "Mong rằng hành trình sắp tới của bạn sẽ toàn là cơ hội tốt, đi đến đâu tỏa sáng đến đó và luôn nhận được sự trân trọng, yêu mến từ mọi người! ✨💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 7
    "Gửi tới {name} xinh đẹp và tràn đầy nhiệt huyết!\n\n"
    "Cảm ơn vì sự đồng hành tuyệt vời của bạn cùng A1K15 trong suốt thời gian qua. "
    "Nhân ngày 20/10, chúc bạn luôn giữ được tâm hồn trẻ trung, nụ cười rạng rỡ, vượt qua mọi kỳ thi thật dễ dàng và luôn thành công trên mọi chặng đường! 🎀🌺\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 8
    "Gửi {name} - cô gái vô cùng đặc biệt của lớp chúng mình!\n\n"
    "Chúc bạn ngày 20/10 ngập tràn trong sự cưng chiều, nhận được vô số món quà đáng yêu và luôn ngập tràn tiếng cười. "
    "Cảm ơn bạn đã luôn là một phần không thể thiếu của A1K15, chúc bạn luôn xinh xắn, may mắn và gặt hái nhiều kết quả cao! 💖🌟\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 9
    "Chúc mừng ngày 20/10 gửi tới {name}!\n\n"
    "Cảm ơn bạn vì những khoảnh khắc đáng nhớ và sự dễ thương bạn mang lại cho lớp. "
    "Mong rằng bạn luôn tự tin vào bản thân, theo đuổi đam mê một cách trọn vẹn và luôn gặp được những người yêu thương bạn thật lòng. Chúc bạn ngày hôm nay thật ngọt ngào! 🌷✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 10
    "Thân gửi {name} nhân ngày Phụ nữ Việt Nam 20/10!\n\n"
    "Chúc bạn có một ngày ngọt ngào, tràn đầy niềm vui và sự bất ngờ. "
    "Hãy luôn là một cô gái xinh đẹp, mạnh mẽ, tự tin và vững vàng bước qua mọi thử thách nhé. Cảm ơn bạn vì đã luôn hòa đồng và đáng yêu với tập thể A1K15! ✨💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 11
    "Gửi đến {name} những lời chúc chân thành nhất ngày 20/10!\n\n"
    "Cảm ơn bạn vì đã luôn làm cho tập thể A1K15 trở nên tuyệt vời hơn. "
    "Chúc bạn tuổi mới ngày càng xinh đẹp, sắc sảo, học tập thăng tiến và mỗi ngày trôi qua đều là một ngày ngập tràn niềm vui cùng những điều tuyệt vời nhất! 🌸⭐\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 12
    "Gửi {name} thân mến!\n\n"
    "Nhân ngày 20/10, chúc bạn luôn tràn ngập sức sống, xinh đẹp rạng ngời và luôn giữ được sự vui vẻ hồn nhiên. "
    "Cảm ơn những cống hiến và sự hiện diện đáng quý của bạn trong tập thể lớp. Mong bạn luôn bình an, may mắn và vạn sự như ý! 💫💕\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 13
    "Chúc mừng ngày 20/10 thật nhiều niềm vui gửi tới {name}!\n\n"
    "Chúc bạn hôm nay sẽ nhận được thật nhiều hoa, quà và vô vàn lời chúc ý nghĩa. "
    "Cảm ơn bạn vì đã luôn dịu dàng, nhiệt tình hỗ trợ mọi người. Chúc chặng đường tương lai của bạn sẽ luôn rải đầy hoa hồng và may mắn! 🌹✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 14
    "Gửi {name} - cô bạn vô cùng cá tính và đáng yêu!\n\n"
    "Nhân ngày Phụ nữ Việt Nam, chúc bạn lúc nào cũng rạng rỡ, tràn đầy năng lượng tích cực và luôn tỏa sáng rực rỡ. "
    "Cảm ơn bạn đã mang lại nhiều tiếng cười cho lớp. Chúc bạn đạt được mọi ước mơ và gặt hái thật nhiều thành công nhé! 💖✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 15
    "Chúc mừng 20/10 ngọt ngào gửi tới {name}!\n\n"
    "Cảm ơn vì bạn đã luôn là một mảnh ghép dịu dàng, đáng mến của A1K15. "
    "Chúc bạn ngày hôm nay và cả 364 ngày còn lại trong năm luôn xinh đẹp, an yên, không có lo âu vướng bận và luôn thi cử đạt thành tích xuất sắc! 🌷💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 16
    "Thân gửi {name} nhân ngày Phụ nữ Việt Nam!\n\n"
    "Chúc bạn luôn vững tin vào bản thân, xinh đẹp mỗi ngày và luôn gặp những cơ hội rộng mở trên đường đời. "
    "Cảm ơn bạn đã gắn bó và đóng góp nhiều kỷ niệm đẹp cho thanh xuân A1K15. Chúc bạn có một ngày 20/10 thật trọn vẹn! 🌟✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 17
    "Gửi {name} xinh đẹp!\n\n"
    "Chúc bạn ngày 20/10 thật nhiều hoa thơm, quà đẹp và những lời chúc yêu thương nhất. "
    "Cảm ơn bạn vì đã luôn hoà đồng, tinh tế và mang lại không khí ấm áp cho lớp. Mong rằng chặng đường học tập của bạn luôn đạt điểm tuyệt đối! 🌸💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 18
    "Chúc mừng {name} nhân ngày 20/10!\n\n"
    "Cảm ơn sự nhiệt tình và tâm huyết của bạn trong mọi hoạt động của lớp. "
    "Chúc bạn luôn giữ được sự vui tươi, thông minh, ngày càng xinh đẹp và chinh phục được mọi đỉnh cao học tập mà mình mong muốn! ✨💥\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 19
    "Gửi tới {name} - bông hoa tươi thắm của A1K15!\n\n"
    "Nhân ngày Phụ nữ Việt Nam 20/10, chúc bạn luôn rực rỡ, may mắn và hạnh phúc. "
    "Cảm ơn vì bạn đã luôn mang sự tích cực đến với tập thể. Mong rằng mọi dự định sắp tới của bạn đều diễn ra thuận lợi và thành công rực rỡ! 🌷💫\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 20
    "Chúc mừng {name} nhân ngày kỉ niệm 20/10!\n\n"
    "Mong bạn luôn tràn đầy sức sống, nụ cười luôn thường trực trên môi và luôn cảm nhận được tình yêu thương xung quanh. "
    "Cảm ơn bạn đã luôn đồng hành cùng A1K15, chúc bạn luôn gặt hái được những điều tuyệt vời nhất! 💕✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 21
    "Thân gửi {name} xinh xắn!\n\n"
    "Nhân ngày 20/10, chúc bạn không chỉ hôm nay mà ngày nào cũng là một ngày ngập tràn niềm vui và bình an. "
    "Cảm ơn sự hiền lành, dễ thương của bạn dành cho mọi người. Chúc bạn thi cử luôn suôn sẻ và gặt hái thật nhiều hoa điểm 10! 🌸🌟\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 22
    "Gửi tới {name} - cô gái thông minh và đáng yêu!\n\n"
    "Nhân ngày 20/10, chúc bạn lúc nào cũng trẻ trung, tự tin và vững bước với ước mơ của mình. "
    "Cảm ơn bạn vì đã cùng tạo nên một thời thanh xuân A1K15 thật đẹp. Chúc bạn có một ngày ngọt ngào tràn đầy bất ngờ! 💖✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 23
    "Chúc mừng {name} nhân ngày Phụ nữ Việt Nam!\n\n"
    "Cảm ơn nụ cười và năng lượng đáng yêu của bạn mỗi ngày đến lớp. "
    "Chúc bạn 20/10 nhận thật nhiều quà, luôn xinh đẹp như công chúa và gặt hái thành công rực rỡ trong chặng đường sắp tới! 🌹💫\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 24
    "Gửi {name} thân thương!\n\n"
    "Chúc bạn ngày 20/10 thật nhiều niềm vui, luôn tự tin tỏa sáng và đạt được mọi mong ước. "
    "Cảm ơn bạn đã cùng đồng hành, vun đắp cho A1K15 thêm phần gắn kết. Mong bạn luôn bình an và luôn nở nụ cười rạng rỡ! 🌷✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 25
    "Chúc mừng {name} nhân dịp đặc biệt 20/10!\n\n"
    "Cảm ơn bạn vì đã luôn lắng nghe, chia sẻ và tô điểm cho lớp học thêm sắc màu. "
    "Chúc bạn luôn xinh đẹp, duyên dáng, giữ trọn ngọn lửa đam mê và vượt qua mọi kì thi một cách xuất sắc nhất! 💕💫\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 26
    "Gửi người bạn {name} vô cùng dễ mến!\n\n"
    "Chúc bạn ngày Phụ nữ Việt Nam tràn ngập tiếng cười, nhận được những bất ngờ ngọt ngào nhất. "
    "Cảm ơn bạn vì đã là một thành viên tuyệt vời của A1K15. Mong tương lai sẽ mang đến cho bạn vô vàn may mắn và cơ hội tốt! ✨🌸\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 27
    "Thân gửi {name} nhân ngày 20/10!\n\n"
    "Chúc bạn luôn giữ được sự lạc quan, rạng rỡ và nét cuốn hút rất riêng của mình. "
    "Cảm ơn những đóng góp thầm lặng nhưng tuyệt vời của bạn cho lớp. Chúc bạn luôn vui vẻ, học giỏi và gặp toàn điều tốt lành! 💖🌟\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 28
    "Gửi tới {name} lời chúc 20/10 ngọt ngào nhất!\n\n"
    "Chúc bạn xinh đẹp rạng ngời, lúc nào cũng tràn đầy niềm tin và động lực phấn đấu. "
    "Cảm ơn bạn đã cùng A1K15 đi qua những tháng ngày học sinh đẹp đẽ. Chúc bạn luôn là cô gái hạnh phúc và thành công! 🌺✨\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 29
    "Chúc mừng ngày Phụ nữ Việt Nam gửi tới {name}!\n\n"
    "Mong rằng ngày hôm nay của bạn sẽ ngập tràn quà tặng, sự quan tâm và tình yêu thương từ mọi người. "
    "Cảm ơn bạn vì sự dễ thương và ấm áp. Chúc bạn luôn may mắn, học tập xuất sắc và luôn tỏa sáng! 🌸💖\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫",

    # 30
    "Gửi {name} - mảnh ghép rực rỡ của A1K15!\n\n"
    "Nhân ngày 20/10, chúc bạn có một ngày ngập tràn nụ cười, luôn xinh đẹp, thông minh và tràn đầy kiêu hãnh. "
    "Cảm ơn vì đã cùng tạo nên vô vàn kỉ niệm thanh xuân tuyệt đẹp cùng lớp. Chúc mọi ước mơ của bạn đều trở thành hiện thực! ✨💫\n\n"
    "From:22 anh tài A1-K15 THPT Lê Hoàn 💫"
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get-card', methods=['POST'])
def get_card():
    data = request.get_json()
    input_name = data.get('name', '')
    
    if not input_name or not input_name.strip():
        return jsonify({'success': False, 'message': 'Vui lòng nhập tên!'}), 400

    display_name = format_display_name(input_name)

    # Chọn ngẫu nhiên 1 mẫu trong 30 câu chúc và điền tên người nhận vào
    random_template = random.choice(WISH_TEMPLATES)
    wishes = random_template.format(name=display_name)

    return jsonify({
        'success': True,
        'name': display_name,
        'image_url': BOYS_AVATAR_URL,
        'bg_url': CLASS_BG_URL,
        'wishes': wishes
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)