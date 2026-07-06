from config import groq_client


def get_ai_response(messages, stream=False):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=stream
    )

    if stream:
        return response

    return response.choices[0].message.content