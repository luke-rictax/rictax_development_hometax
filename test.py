# 주어진 데이터 문자열
data_str = """
{
    "과세연월": "",
    "신고서종류": "",
    "신고유형": "",
    "상호(성명)": "",
    "사업자(주민)등록번호": "",
    "접수방법": "",
    "접수번호(신고서보기)": "",
    "접수서류": "",
    "접수증": "",
    "납부서": "",
    "제출자ID": "",
    "부속서류제출여부": "",
    "지방소득세": "",
    "납부여부": ""
}
"""

# 문자열을 바이트로 인코딩
data_bytes = data_str.encode('utf-8')

# 바이트 길이를 계산하여 킬로바이트로 변환
data_size_kb = len(data_bytes) / 1024

print(f"데이터 크기: {data_size_kb} KB")