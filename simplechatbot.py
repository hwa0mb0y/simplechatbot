import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

# Streamlit 페이지 설정
st.set_page_config(page_title="여행 가이드 챗봇", page_icon="✈️")

# 제목
st.title("여행 가이드 챗봇 🌍")

# OpenAI API 키 입력
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 입력 필드를 리셋하기 위한 키 생성
if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# 프롬프트 템플릿 생성
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "안녕하세요! 저는 여행 가이드 챗봇이에요. 여행에 대한 정보나 추천지를 알려드릴게요 ✈️🌍 궁금한 점이 있으면 언제든지 물어보세요!"),
    ("human", "{input_text}")
])

# 사용자 입력 (key를 동적으로 변경)
user_input = st.text_input("질문을 입력하세요:", key=f"user_input_{st.session_state.input_key}")

# API 키가 입력되었을 때만 실행
if api_key:
    # LangChain 체인 생성
    chain = {"input_text": RunnablePassthrough()} | prompt_template | ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key) | StrOutputParser()
    
    if user_input:
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # AI 응답 생성
        with st.spinner("AI가 답변을 생성 중입니다..."):
            ai_response = chain.invoke(user_input)
        
        # AI 메시지 추가
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # 입력 필드 리셋을 위해 키 변경
        st.session_state.input_key += 1
        st.experimental_rerun()

    # 대화 내용 표시
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.text_area("You:", value=message["content"], height=100, disabled=True)
        else:
            st.text_area("AI:", value=message["content"], height=200, disabled=True)
else:
    st.warning("OpenAI API 키를 입력해주세요.")