import streamlit as st
from openai import OpenAI
import os

openai_models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"]
deepseek_models = ["deepseek-chat", "deepseek-reasoner"]

def get_client(model):
    if model in openai_models:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))
    elif model in deepseek_models:
        client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY", "<your DeepSeek API key if not set as env var>"), base_url="https://api.deepseek.com")
    else:
        raise ValueError("Unrecognized model")
    return client


def get_response(model, system_prompt, user_input):
    client = get_client(model)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        temperature=1.3,
        stream=True
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content


st.title('Replying to customers')

with st.expander("Customize the prompt"):
    st.subheader("Preset prompt")
    prompt = st.text_area(
        "Prompt",
        "You are the manager of a corporate or school cafeterias, you receive customer comments feedbacks frequently. Please use humane, friendly, polite, inclusive and formal writing to reply to your customers.",
        key="prompt",
    )
    st.write(f"{len(prompt)} characters.")


st.subheader(":thought_balloon: Voice from your customer")
comment = st.text_area(
    "Feedback",
    "The food served in the cafeteria is consistently cold and tasteless. The ingredients don’t seem fresh, and the meals lack variety. I often find myself bringing food from home instead.",
    key="comment"
)

with st.expander("Advanced"):
    model = st.selectbox(
            label="Select model",
            options=openai_models + deepseek_models,
            index=0,
            # placeholder="gpt-4o-mini",
            )
    n_examples = st.number_input(
            label="Number of examples",
            min_value=1,
            max_value=10,
            step=1,
            )
if comment and st.button("Generate Response"):
    st.subheader(":robot_face: :green[AI Assisted Reply]")
    for i in range(n_examples):
        st.divider()
        st.write_stream(get_response(model, prompt, comment))


# generated_reply = comment[::-1]

# if generated_reply:
#     st.subheader("AI Assisted Reply")
#     st.write(generated_reply)


