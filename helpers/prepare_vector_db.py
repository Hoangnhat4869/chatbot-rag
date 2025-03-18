import pdfplumber

from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from constants import OPENAI_API_KEY


def create_vector_store_from_text():
    raw_text = """
  Gặp gỡ nam sinh thủ khoa khối A tỉnh Quảng Ngãi kỳ thi tốt nghiệp THPT đợt 2 với điểm 10 môn Hóa
  Thứ ba, 17/08/2021 20:41 (GMT+7)

  Với tổng điểm 28,55 (trong đó có một điểm 10 môn Hóa học), bạn Trương Hoàng Nhật, học sinh trường THPT số 1 Đức Phổ đã xuất sắc trở thành thủ khoa khối A của tỉnh Quảng Ngãi và nằm trong Top 5 thí sinh đạt điểm có điểm khối A cao nhất cả nước đợt 2.
  Ngay sau khi Bộ GD-ĐT công bố điểm thi tốt nghiệp THPT đợt 2, nhiều gương mặt vàng xứng danh "Con nhà người ta" tiếp tục xuất hiện. Trong số đó có nam sinh Trương Hoàng Nhật với điểm 10 môn Hóa; 9,8 môn Toán và 8,75 môn Vật lý đã trở thành thủ khoa khối A đợt 2 của tỉnh Quảng Ngãi và nằm trong Top 5 thí sinh đạt điểm có điểm khối A cao nhất cả nước.
  Ngoài ra, cậu bạn còn đạt 9 điểm môn tiếng Anh và cũng trở thành thủ khoa khối D07 của tỉnh nhà. Dù phải dự thi tốt nghiệp THPT đợt 2 do ảnh hưởng của dịch Covid-19, song thành tích “khủng” này của Nhật khiến nhiều người ngưỡng mộ.
  Bí quyết học tập của Nhật là học theo chương trình mà thầy cô đã biên soạn, sau đó tự phát triển cách làm theo tư duy của mình sao cho tối ưu và đạt kết quả tốt nhất.
  Chia sẻ về cảm xúc trong ngày nhận điểm thi, Hoàng Nhật cho biết cậu bạn vừa rất vui vì đạt điểm tuyệt đối môn Hóa nhưng cũng có phần hụt hẫng khi môn Lý làm bài không được như ý muốn: “Mình khá hài lòng về số điểm của mình. Khi biết điểm thì mình chỉ bất ngờ ở môn Văn vì các môn còn lại đều đúng số điểm mà mình đã ước tính trước đó. Nhận được kết quả, mình báo ngay cho ba mẹ của mình, gia đình mình rất hạnh phúc và tự hào với số điểm mình đạt được”. Nhật nói.
  Được biết trước ngày thi tốt nghiệp THPT đợt 1 vài ngày, Hoàng Nhật nhận được thông báo sẽ phải chuyển qua thi vào đợt 2 bởi tình hình dịch Covid 19 đang diễn biến phức tạp tại địa phương mình sinh sống. Vì đã chuẩn bị sẵn sàng tất cả mọi thứ để đi thi nên nghe tin như vậy, cậu bạn khá hoang mang và lo lắng. “Việc phải kéo dài thời gian ôn tập khiến mình cảm thấy áp lực và mệt mỏ. Hơn nữa, mình cũng lo sợ không biết đề thi đợt 2 có khó hơn đợt 1 may không. Tuy nhiên sau đó suy nghĩ kỹ lại thì mình cảm thấy khá may mắn vì hôm các bạn thi đợt 1 thì mình bị cảm. Nên nếu mình thi đợt 1 thì có lẽ điểm số sẽ không được như bây giờ.” Nhật bộc bạch.

  Ngoài thành tích học tập tốt, Nhật còn tham gia rất nhiều hoạt động ngoại khóa mà trường và địa phương tổ chức như các chương trình tham quan, tìm hiểu lịch sử, các cuộc thi về an toàn giao thông, rung chuông vàng...Những hoạt động này đã giúp Nhật rèn luyện khả năng ghi nhớ, học hỏi và tiếp thu thêm nhiều kiến thức để làm nền tảng cho vốn hiểu biết của bản thân.
  Từ nhỏ, cậu bạn đã đam mê rất lớn với công nghệ.
  Thời gian tới, Hoàng Nhật dự đinh sẽ lựa chọn và theo học chuyên ngành Trí tuệ nhân tạo (ngành Khoa học máy tính) của trường đại học Bách Khoa TPHCM. Cậu bạn chia sẻ ý do thú vị nhất khiến bản thân quyết định theo đuổi ngành này là bởi từ nhỏ Nhật đã có một niềm đam mê rất lớn với công nghệ và “ấp ủ” mong muốn bản thân sẽ có thể làm gì đó giúp cho nước nhà càng phát triển hơn trong tương lai.
  Trước đó, cậu bạn cũng đã xuất sắc đạt được 981 điểm thi ĐGNL và đậu vào ngành Khoa học máy tính mà bản thân mong muốn. Ngoài ra trong năm học lớp 12, Nhật cũng là thành viên của đội tuyển HSG quốc gia môn Toán của tỉnh nhà.
  """

    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=800, chunk_overlap=150, length_function=len
    )

    chunks = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY, model="text-embedding-ada-002"
    )

    vector_store = FAISS.from_texts(texts=chunks, embedding=embeddings)
    return vector_store


def get_text_from_file(documents):
    """
    Extract text from PDF files.
    Variables:
      * documents: list of file paths
    """
    raw_text = ""
    for document in documents:
        if document.name.endswith(".pdf"):
            with pdfplumber.open(document) as pdf:
                for page in pdf.pages:
                    raw_text += page.extract_text() or ""
    return raw_text


def create_vector_store_from_files(documents: list):
    """
    Create a vector store from a list of PDF files.
    Variables:
      * documents: list of file paths
    """
    raw_text = get_text_from_file(documents)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_text(raw_text)

    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY, model="text-embedding-ada-002"
    )

    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store
