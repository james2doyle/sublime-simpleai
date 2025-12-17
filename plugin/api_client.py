import http.client
import json
import logging
import threading
from typing import Any, Dict, List, Union

import sublime

# Import get_setting from the new settings module
from .settings import get_setting

logger = logging.getLogger("SimpleAIPlugin")


class AsyncSimpleAI(threading.Thread):
    """
    A simple async thread class for accessing the Simple AI API and waiting for a response.
    """

    def __init__(self, view: sublime.View, region: sublime.Region, data: Dict[str, Any], instruction: str):
        """
        Initializes the AsyncSimpleAI thread.

        Args:
            view: The Sublime Text view associated with the command.
            region: The sublime.Region object representing the highlighted text.
            data: The payload data for the API request.
            instruction: Original prompt text
        """
        super().__init__()
        self.view: sublime.View = view
        self.region: sublime.Region = region
        self.data: Dict[str, Any] = data
        self.instruction: str = instruction
        self.running: bool = False
        self.result: Union[str, None] = None
        self.error: Union[str, None] = None

    def run(self) -> None:
        """
        Overrides the threading.Thread run method.
        Performs the API call and handles potential errors.
        """
        self.running = True
        self.result = None
        self.error = None
        try:
            self.result = self.get_ai_response()
        except Exception as e:
            self.error = str(e)
            logger.error("Error in AsyncSimpleAI thread: {}".format(self.error))
        finally:
            self.running = False

    def get_ai_response(self) -> str:
        """
        Passes the given data to the API, returning the response.
        Raises ValueError if API token is missing or if the API returns an error.
        """
        token: Union[str, None] = get_setting(self.view, "api_token", None)
        hostname: str = get_setting(self.view, "hostname", "openrouter.ai")
        model_name: str = self.data.get("model", "openrouter/auto")
        api_path: str = "/api/v1/chat/completions"

        if token is None:
            raise ValueError("API token is missing.")

        conn: http.client.HTTPSConnection = http.client.HTTPSConnection(hostname)
        headers: Dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(token)
        }

        # Use the payload directly (already in OpenAI format)
        data_payload: str = json.dumps(self.data)
        logger.debug("API request data: {}".format(data_payload))

        logger.debug("API request path: {}".format(api_path))

        conn.request("POST", api_path, data_payload, headers)
        response: http.client.HTTPResponse = conn.getresponse()
        response_body: str = response.read().decode("utf-8")
        response_dict: Dict[str, Any] = json.loads(response_body)
        logger.debug("API response data: {}".format(response_dict))

        # Handle OpenAI API errors
        if response_dict.get("error", None):
            error_details = response_dict["error"].get("message", "Unknown API error")
            raise ValueError("API Error: {}".format(error_details))

        # Check for OpenAI-specific error structure
        if "choices" not in response_dict:
            raise ValueError("Invalid API response: missing 'choices' field")

        choices: List[Dict[str, Any]] = response_dict.get("choices", [])
        if not choices:
            raise ValueError(
                "AI did not return any choices. The model might have generated no response or encountered an internal issue."
            )

        first_choice: Dict[str, Any] = choices[0]
        finish_reason = first_choice.get("finish_reason", None)

        if finish_reason:
            if finish_reason == "stop":
                pass
            elif finish_reason == "length":
                usage_metadata = response_dict.get("usage", {})
                total_token_count = usage_metadata.get("total_tokens", 0)
                raise ValueError(
                    "AI finished early due to max tokens limit. Used {} tokens. Try increasing 'max_tokens' in settings.".format(
                        total_token_count
                    )
                )
            elif finish_reason == "content_filter":
                raise ValueError("AI response blocked by content filters.")
            else:
                raise ValueError("AI finished early with reason: {}".format(finish_reason))

        message: Dict[str, Any] = first_choice.get("message", {})
        if not message:
            raise ValueError("No message found in AI response choice.")

        content: str = message.get("content", "")
        if not content:
            raise ValueError("No text content found in AI response message.")

        return content


