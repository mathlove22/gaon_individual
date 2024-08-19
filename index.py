import streamlit as st
import pandas as pd

# 데이터 로드
data = pd.read_csv('data.csv', encoding='euc-KR')

# student_id를 문자열로 변환
data['student_id'] = data['student_id'].astype(str)

# 사용자 입력
st.title("학생 평가 조회 시스템")
student_id = st.text_input("학생 ID를 입력하세요:")
password = st.text_input("비밀번호를 입력하세요:", type="password")

# 로그인 및 결과 조회
if st.button("로그인"):
    # 입력한 ID와 비밀번호에 해당하는 학생 검색
    student = data[(data['student_id'] == student_id) & (data['password'] == password)]

    if not student.empty:
        # 학생의 평가 결과 출력
        st.write(f"학생 이름 : {student['name'].values[0]}")
        st.write(f"{student['evaluation_1'].values[0]} - 점수: {student['evaluation_1_score'].values[0]}")
        st.write(f"{student['evaluation_2'].values[0]} - 점수: {student['evaluation_2_score'].values[0]}")
        st.write(f"{student['evaluation_3'].values[0]} - 점수: {student['evaluation_3_score'].values[0]}")
        st.write(f"{student['evaluation_4'].values[0]} - 점수: {student['evaluation_4_score'].values[0]}")
        st.write(f"참고사항 : {student['description'].values[0]}")
    else:
        st.error("ID 또는 비밀번호가 잘못되었습니다.")

        # 비밀번호 변경 버튼 추가
        new_password = st.text_input("새로운 비밀번호를 입력하세요:", type="password")
        if st.button("비밀번호 변경"):
            # 데이터프레임에서 해당 행의 비밀번호 업데이트
            data.loc[data['student_id'] == student_id, 'password'] = new_password

            # 변경된 데이터를 다시 CSV 파일로 저장
            data.to_csv('data.csv', index=False, encoding='euc-KR')
            st.success("비밀번호가 변경되었습니다.")
    else:
        st.error("ID 또는 비밀번호가 잘못되었습니다.")
