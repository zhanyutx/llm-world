import os
import json
import sys
from openai import OpenAI

# def get_openai_response(prompt: str, api_key: str):
#     """
#     Interacts with the OpenAI API to get a response for the given prompt.
#     """
#     try:
#         client = OpenAI(api_key=api_key)
#         completion = client.chat.completions.create(
#             model="gpt-3.5-turbo",  # Or another suitable model
#             messages=[
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         if completion.choices and len(completion.choices) > 0:
#             return completion.choices[0].message.content
#         else:
#             return "Error: No response from OpenAI."
#     except Exception as e:
#         return f"Error interacting with OpenAI: {str(e)}"

# Placeholder for XAI or other providers in the future
def get_openai_response(prompt: str, api_key: str, base_url: str = "https://api.x.ai/v1"):
    """
    Interacts with the XAI API to get a response. (Placeholder)
    """
    try:
        client = OpenAI(api_key=api_key, base_url=base_url) # Note: OpenAI SDK used for XAI as per user feedback
        completion = client.chat.completions.create(
            model="grok-3", # Replace with actual XAI model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        if completion.choices and len(completion.choices) > 0:
            return completion.choices[0].message.content
        else:
            return "Error: No response from XAI."
    except Exception as e:
        return f"Error interacting with XAI: {str(e)}"

if __name__ == "__main__":
    response_data = {}
    if len(sys.argv) > 1:
        try:
            input_data = json.loads(sys.argv[1])
            provider = input_data.get("provider", "openai")
            prompt_text = input_data.get("prompt")

            if not prompt_text:
                response_data = {"error": "Prompt text is missing."}
            else:
                api_key = ""
                llm_response = ""

                if provider == "openai":
                    api_key = os.environ.get("OPENAI_API_KEY")
                    if not api_key:
                        llm_response = "Error: OPENAI_API_KEY environment variable not set."
                    else:
                        llm_response = get_openai_response(prompt_text, api_key)
                # elif provider == "xai":
                #     api_key = os.environ.get("XAI_API_KEY")
                #     base_url = os.environ.get("XAI_BASE_URL", "https://api.x.ai/v1")
                #     if not api_key:
                #         llm_response = "Error: XAI_API_KEY environment variable not set."
                #     else:
                #         llm_response = get_xai_response(prompt_text, api_key, base_url)
                else:
                    llm_response = f"Error: Provider '{provider}' not supported yet."
                
                response_data = {"response": llm_response}
        except json.JSONDecodeError:
            response_data = {"error": "Invalid JSON input."}
        except Exception as e:
            response_data = {"error": f"An unexpected error occurred: {str(e)}"}
    else:
        response_data = {"error": "No input data provided. Usage: python llm_handler.py '{\"prompt\": \"your prompt\", \"provider\": \"openai\"}'"}

    print(json.dumps(response_data))
