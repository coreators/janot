import subprocess

import gradio as gr
from llama_cpp import Llama

llama = Llama(model_path='./models/TheBloke_WizardLM-7B-uncensored-GGML/WizardLM-7B-uncensored.ggmlv3.q4_0.bin', verbose=False)


def say(text: str):
    subprocess.call(['say', text])


def gen_instruction(instruction: str, input: str = None) -> str:
    input_section = f'### Input: \n{input}\n' if input else ""
    # return f"Q: {instruction}, A: "
    return f"""Here is an instruction that describes a task. Write a response that adequately completes the request.

    ### Instruction:
    {instruction}

    {input_section}### Response:"""


def get_completion(instruction: str, input: str = None, temperature: float = 0.1) -> str:
    prompt = gen_instruction(instruction, input)
    generation_output = llama.create_completion(
        prompt,
        temperature=temperature,
        top_p=0.75,
        max_tokens=32,
        stop=["###", "User:"]
    )
    response_text = generation_output['choices'][0]['text']
    return response_text


def stt(text_input: str, reset_conversation: bool, temperature: float):
    if reset_conversation:
        gr.State.conversation_history = []
        return ""

    if not hasattr(gr.State, 'conversation_history'):
        gr.State.conversation_history = []

    conversation_history = gr.State.conversation_history

    try:
        print(text_input)
        print('#-------------------------')
        conversation_history.append('User: ' + text_input)
        conversation_input = '\n'.join(conversation_history)

        response_text = get_completion(conversation_input, temperature=temperature)
        print(response_text)
        print('---------------------------#')
        conversation_history.append("JANOT: " + response_text)

        formatted_conversation_history = '\n'.join(conversation_history)
        say(response_text)

        return formatted_conversation_history

    except (ValueError, Exception) as e:
        error_message = str(e)
        return f'Error: {error_message}'


inputs = [
    gr.Textbox(
        label='Text 1',
        info="Initial text",
        lines=3,
        value="Name the planets in the solar system?"
    ),
    gr.Checkbox(label="Restart conversation", value=False),
    gr.Slider(0.0, 1.0, step=0.1, value=0.8, label="Generation temperature 🌡️")
]

outputs = [
    gr.Textbox(label="Conversation history")
]

gr.Interface(
    fn=stt,
    inputs=inputs,
    outputs=outputs,
    allow_flagging='never',
    title='Llama talk',
    description='This demo use Llama.cpp, use mac to Text-to-Speach',
    css='footer {visibility: hidden}'
).launch()
