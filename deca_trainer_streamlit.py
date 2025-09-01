import streamlit as st
import random

roleplay_questions = [
    {"question": "How would you increase sales for a small retail store?", "keywords": ["social media", "promotion", "ads", "marketing"]},
    {"question": "A customer complains about a product. How would you handle it?", "keywords": ["listen", "empathy", "solution", "customer service"]},
    {"question": "How would you launch a new product in a competitive market?", "keywords": ["research", "advertising", "target audience", "pricing"]},
    {"question": "Your team has a limited budget for marketing. What strategy would you choose?", "keywords": ["budget", "ROI", "prioritize", "effective"]},
]

def score_response(user_response, keywords):
    user_response = user_response.lower()
    score = sum(1 for word in keywords if word in user_response)
    return score, len(keywords)

if 'messages' not in st.session_state: st.session_state.messages = []
if 'question' not in st.session_state: st.session_state.question = random.choice(roleplay_questions)
if 'submitted' not in st.session_state: st.session_state.submitted = False
if 'user_input' not in st.session_state: st.session_state.user_input = ""
if 'total_score' not in st.session_state: st.session_state.total_score = 0
if 'total_possible' not in st.session_state: st.session_state.total_possible = 0

st.title("DECA Roleplay Trainer")
st.subheader("Question:")
st.write(st.session_state.question["question"])

st.session_state.user_input = st.text_input("Type your answer here:", value=st.session_state.user_input)

if st.button("Submit Answer"):
    if st.session_state.user_input.strip() != "":
        score, max_score = score_response(st.session_state.user_input, st.session_state.question["keywords"])
        st.session_state.total_score += score
        st.session_state.total_possible += max_score

        if score == max_score:
            feedback = "Excellent! You included all key points."
            color = "green"
        elif score >= max_score / 2:
            feedback = "Good job! Try to include more key points next time."
            color = "orange"
        else:
            feedback = "Keep practicing! Focus on incorporating the key ideas."
            color = "red"

        st.session_state.messages.append({"role": "user", "content": st.session_state.user_input})
        st.session_state.messages.append({"role": "bot", "content": f"Score: {score}/{max_score} - {feedback}", "color": color})
        st.session_state.submitted = True
    else:
        st.error("Please type your answer before submitting.")

if st.button("Next Question") and st.session_state.submitted:
    st.session_state.question = random.choice(roleplay_questions)
    st.session_state.user_input = ""
    st.session_state.submitted = False

for msg in st.session_state.messages:
    if msg['role'] == 'user':
        st.markdown(f"**You:** {msg['content']}")
    else:
        color = msg.get("color", "black")
        st.markdown(f"**Trainer:** <span style='color:{color}'>{msg['content']}</span>", unsafe_allow_html=True)

st.markdown("---")
st.subheader("📊 Session Progress")
st.write(f"**Total Score:** {st.session_state.total_score}/{st.session_state.total_possible}")
if st.session_state.total_possible > 0:
    percentage = st.session_state.total_score / st.session_state.total_possible
    st.write(f"**Percentage:** {percentage*100:.1f}%")
    st.progress(percentage)
