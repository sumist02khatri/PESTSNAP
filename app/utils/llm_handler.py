from textwrap import dedent

import requests
from groq import Groq

from config.settings import GROQ_API_KEY, GROQ_MODEL, OLLAMA_BASE_URL, OLLAMA_MODEL
from utils.pest_info import build_rule_based_response


def build_chat_prompt(question, pest_name, confidence, pest_details):
    return dedent(
        f"""
        You are an agricultural assistant for rice pest management.
        Keep the answer practical, concise, and farmer-friendly.
        Focus only on the detected pest and its management.

        Detected pest: {pest_name}
        Confidence: {confidence:.2%}
        Problem description: {pest_details["problem"]}
        Suggested cure: {pest_details["cure"]}
        Prevention methods: {pest_details["prevention"]}

        User question: {question}
        """
    ).strip()


def ask_fast_mode(question, pest_name, confidence, pest_details):
    return build_rule_based_response(question, pest_name, confidence, pest_details)


def ask_ollama(question, pest_name, confidence, pest_details):
    prompt = build_chat_prompt(question, pest_name, confidence, pest_details)

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL.rstrip('/')}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=45,
        )
        response.raise_for_status()
        payload = response.json()
        answer = payload.get("response", "").strip()
        if answer:
            return answer, "Local Ollama response"
    except Exception:
        pass

    return (
        build_rule_based_response(question, pest_name, confidence, pest_details),
        "Ollama unavailable, showing curated pest guidance",
    )


def ask_groq(question, pest_name, confidence, pest_details):
    if not GROQ_API_KEY:
        return (
            build_rule_based_response(question, pest_name, confidence, pest_details),
            "Groq API key missing, showing curated pest guidance",
        )

    prompt = build_chat_prompt(question, pest_name, confidence, pest_details)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You answer only about rice pest identification, treatment, and prevention.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_completion_tokens=400,
        )
        answer = completion.choices[0].message.content.strip()
        if answer:
            return answer, "Free Cloud response via Groq"
    except Exception:
        pass

    return (
        build_rule_based_response(question, pest_name, confidence, pest_details),
        "Groq unavailable, showing curated pest guidance",
    )


def get_chat_response(mode, question, pest_name, confidence, pest_details):
    if mode == "Local Ollama mode":
        return ask_ollama(question, pest_name, confidence, pest_details)
    if mode == "Free Cloud mode":
        return ask_groq(question, pest_name, confidence, pest_details)
    return ask_fast_mode(question, pest_name, confidence, pest_details), "Fast rule-based response"
