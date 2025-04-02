import os
from openai import OpenAI

# Use your OpenAI API key from environment variable or fallback (for testing only)
api_key = os.getenv("OPENAI_API_KEY") or "your-openai-api-key-here"
client = OpenAI(api_key=api_key)

# GPT-4o Mini pricing (April 2024)
INPUT_COST_PER_1K = 0.00015   # $0.15 per million tokens
OUTPUT_COST_PER_1K = 0.0006   # $0.60 per million tokens

# Track token usage and cost
total_input_tokens = 0
total_output_tokens = 0

def chat_with_chatgpt(prompt, conversation_history=None):
    global total_input_tokens, total_output_tokens
    try:
        messages = conversation_history if conversation_history else []
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4o Mini (cheapest option)
            messages=messages,
            temperature=0.2,
            max_tokens=200,
        )

        bot_response = response.choices[0].message.content

        # Track tokens and cost
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        total_input_tokens += input_tokens
        total_output_tokens += output_tokens

        input_cost = (input_tokens / 1000) * INPUT_COST_PER_1K
        output_cost = (output_tokens / 1000) * OUTPUT_COST_PER_1K
        total_cost = input_cost + output_cost
        running_total = ((total_input_tokens / 1000) * INPUT_COST_PER_1K) + ((total_output_tokens / 1000) * OUTPUT_COST_PER_1K)

        print(f"\n[Usage] Input: {input_tokens} tokens, Output: {output_tokens} tokens")
        print(f"[Cost] This message: ${total_cost:.6f} | Total so far: ${running_total:.6f}\n")

        return bot_response

    except Exception as e:
        return f"Error: {e}"

def main():
    print("Welcome to the GPT-4o Mini-powered English practice chatbot!")
    conversation_history = []
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        bot_response = chat_with_chatgpt(user_input, conversation_history)
        print("Bot:", bot_response)

        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": bot_response})
        conversation_history = conversation_history[-10:]

if __name__ == "__main__":
    main()
