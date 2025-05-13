from groq import Groq, APIError


def verify_groq_api_key(api_key):
    """Verify if the Groq API key is valid by making a test request."""
    try:
        client = Groq(api_key=api_key)
        # Make a simple test request
        client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        return True
    except APIError:
        return False