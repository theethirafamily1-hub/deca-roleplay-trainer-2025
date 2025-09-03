import streamlit as st
import random

roleplay_questions = [
    # ----------------------
    # Marketing
    # ----------------------
    {"question": "How would you promote a new energy drink to teenagers?", 
     "keywords": ["social media", "promotion", "influencers", "ads"]},
    
    {"question": "Sales at your clothing store are down. What marketing strategy would you use to increase traffic?", 
     "keywords": ["discount", "advertising", "promotion", "social media"]},

    {"question": "Your company is launching a new app. How would you generate excitement before launch?", 
     "keywords": ["buzz", "advertising", "pre-launch", "campaign"]},

    {"question": "You are asked to design a loyalty program for a coffee shop. What features would you include?", 
     "keywords": ["points", "rewards", "discount", "customer loyalty"]},

    {"question": "Your competitor is running a successful ad campaign. How would you respond?", 
     "keywords": ["competitive", "advertising", "unique", "differentiate"]},

    # ----------------------
    # Customer Service
    # ----------------------
    {"question": "A customer is upset about a late delivery. How would you resolve the issue?", 
     "keywords": ["apology", "solution", "customer service", "empathy"]},

    {"question": "You are a store manager and a customer demands a refund against store policy. How do you handle it?", 
     "keywords": ["policy", "solution", "empathy", "alternative"]},

    {"question": "Your hotel received several negative online reviews. What steps would you take to address them?", 
     "keywords": ["reviews", "response", "improvement", "service"]},

    {"question": "A customer is waiting in line for a long time and becomes frustrated. How do you calm the situation?", 
     "keywords": ["apology", "patience", "solution", "service"]},

    {"question": "You are working at a restaurant and a customer claims their food is undercooked. What do you do?", 
     "keywords": ["apology", "replace", "customer", "service"]},

    # ----------------------
    # Finance / Business
    # ----------------------
    {"question": "Your company has a limited budget. How would you decide what to spend on marketing?", 
     "keywords": ["budget", "ROI", "prioritize", "effective"]},

    {"question": "You are asked to prepare a budget for a small business. What categories should you include?", 
     "keywords": ["expenses", "revenue", "marketing", "operations"]},

    {"question": "Sales are dropping but expenses are rising. What financial strategy would you suggest?", 
     "keywords": ["cut costs", "increase revenue", "budget", "efficiency"]},

    {"question": "A business wants to expand into a new market. What financial factors should they consider?", 
     "keywords": ["costs", "revenue", "profit", "investment"]},

    {"question": "How would you help a company increase profit margins?", 
     "keywords": ["reduce costs", "increase sales", "efficiency", "pricing"]},

    # ----------------------
    # Teamwork / Leadership
    # ----------------------
    {"question": "You are leading a group project and two members are arguing. How do you handle it?", 
     "keywords": ["conflict", "mediate", "teamwork", "solution"]},

    {"question": "Your team has a tight deadline and people are falling behind. What do you do?", 
     "keywords": ["delegate", "prioritize", "support", "time management"]},

    {"question": "A team member isn’t contributing. How would you motivate them?", 
     "keywords": ["encourage", "communicate", "motivate", "support"]},

    {"question": "You are a new manager. How would you build trust with your team?", 
     "keywords": ["respect", "communication", "listening", "trust"]},

    {"question": "Your team just finished a project successfully. How would you celebrate their achievement?", 
     "keywords": ["recognition", "reward", "celebrate", "motivate"]},
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
