import streamlit as st
import pandas as pd

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('data.csv', encoding='euc-KR')

# 초기 세션 상태 설정
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student_id = None

# 데이터 로드
data = load_data()
data['student_id'] = data['student_id'].astype(str)

# 로그인 함수
def login(student_id, password):
    student = data[(data['student_id'] == student_id) & (data['password'] == password)]
    if not student.empty:
        st.session_state.logged_in = True
        st.session_state.student_id = student_id
        return student
    return None

# 비밀번호 변경 함수
def change_password(student_id, new_password):
    global data
    data.loc[data['student_id'] == student_id, 'password'] = new_password
    data.to_csv('data.csv', index=False, encoding='euc-KR')
    st.cache_data.clear()
    st.success("비밀번호가 성공적으로 변경되었습니다!")

# 메인 앱 레이아웃
st.title("학생 평가 조회 시스템")

if not st.session_state.logged_in:
    # 로그인 폼
    with st.form("login_form"):
        student_id = st.text_input("학생 ID를 입력하세요:")
        password = st.text_input("비밀번호를 입력하세요:", type="password")
        submit_button = st.form_submit_button("로그인")
        
        if submit_button:
            student = login(student_id, password)
            if student is not None:
                st.success("로그인 성공!")
            else:
                st.error("ID 또는 비밀번호가 잘못되었습니다.")
else:
    # 학생 정보 및 비밀번호 변경 섹션
    student = data[data['student_id'] == st.session_state.student_id].iloc[0]
    st.write(f"학생 이름 : {student['name']}")
    st.write(f"{student['evaluation_1']} - 점수: {student['evaluation_1_score']}")
    st.write(f"{student['evaluation_2']} - 점수: {student['evaluation_2_score']}")
    st.write(f"{student['evaluation_3']} - 점수: {student['evaluation_3_score']}")
    st.write(f"{student['evaluation_4']} - 점수: {student['evaluation_4_score']}")
    st.write(f"참고사항 : {student['description']}")
    
    st.subheader("비밀번호 변경")
    with st.form("password_change_form"):
        new_password = st.text_input("새 비밀번호를 입력하세요:", type="password")
        confirm_password = st.text_input("새 비밀번호를 다시 입력하세요:", type="password")
        change_button = st.form_submit_button("비밀번호 변경")
        
        if change_button:
            if new_password == confirm_password:
                change_password(st.session_state.student_id, new_password)
            else:
                st.error("새 비밀번호가 일치하지 않습니다. 다시 확인해주세요.")
    
    if st.button("로그아웃"):
        st.session_state.logged_in = False
        st.session_state.student_id = None
        st.experimental_rerun()
