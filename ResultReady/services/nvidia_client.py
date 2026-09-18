import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class NvidiaClient:
    def __init__(self) -> None:
        api_key = os.getenv("NVIDIA_API_KEY")
        base_url = os.getenv(
            "NVIDIA_BASE_URL",
            "https://integrate.api.nvidia.com/v1",
        )
        model = os.getenv(
            "NVIDIA_MODEL",
            "nvidia/nemotron-3.5-lightning-30b-a3b",
        )

        if not api_key:
            raise ValueError(
                "NVIDIA_API_KEY was not found. "
                "Add it to the .env file."
            )

        self.model = model
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.0,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False
                }
            },
        )

        message = response.choices[0].message
        content = message.content

        if not content:
            raise RuntimeError(
                "The NVIDIA model returned an empty response."
            )

        return content.strip()