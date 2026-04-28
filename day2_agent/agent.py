"""
Task 9 - Day 2 Agent (Groq)
ReAct loop:
Thought -> Action -> Action Input -> Observation

Uses TOOL_REGISTRY for every tool call.
"""

import os
import sys
import json
import time
import re

from dotenv import load_dotenv
from groq import Groq


# -------------------------------------------------
# Paths
# -------------------------------------------------

HERE = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(0, HERE)

from tools.registry import TOOL_REGISTRY

load_dotenv(
    os.path.join(HERE, ".env")
)


# -------------------------------------------------
# Groq Setup
# -------------------------------------------------

try:
    GROQ_API_KEY = os.getenv(
        "GROQ_API_KEY"
    )

    if not GROQ_API_KEY:
        raise ValueError(
          "GROQ_API_KEY missing"
        )

    client = Groq(
        api_key=GROQ_API_KEY
    )

except Exception as e:
    print(
      f"[ERROR] {e}"
    )
    sys.exit(1)


# Recommended models:
# llama-3.3-70b-versatile
# deepseek-r1-distill-llama-70b
# mixtral-8x7b-32768

MODEL = "llama-3.3-70b-versatile"


# -------------------------------------------------
# Prompt
# -------------------------------------------------

SYSTEM_PROMPT = """
You are a smart customer-support agent.

Available tools:

search_products(query: str, limit: int=10)

get_order_details(order_id: str)

check_inventory(sku: str)

create_support_ticket(
 customer_id: str,
 issue: str,
 priority: str
)

STRICT FORMAT ONLY:

Thought: reasoning

Action: tool_name

Action Input: {"param":"value"}

One tool per turn.

No markdown.

When finished output ONLY:

Final Answer: summary
"""


TASK = """
Search for products containing Magento.
Check inventory status of each result.
For every product with low or out stock,
create support ticket with priority high
for customer CUST-SYS-01.
Summarize what happened.
"""


MAX_ITERATIONS = 12
SLEEP_BETWEEN = 2


# -------------------------------------------------
# Helpers
# -------------------------------------------------

def extract_field(
    text,
    field
):
    for line in text.splitlines():

        if line.startswith(
            f"{field}:"
        ):
            return line[
              len(field)+1:
            ].strip()

    return ""


def clean_json(raw):

    raw=raw.strip()

    raw = re.sub(
      r"^```[a-z]*\n?",
      "",
      raw
    )

    raw = re.sub(
      r"\n?```$",
      "",
      raw
    )

    return raw.strip()


def separator(label=""):

    if label:
        return (
          f"\n[{label}]\n"
          + "-"*50
        )

    return "-"*60


# -------------------------------------------------
# Agent Loop
# -------------------------------------------------

def run_agent():

    print("="*60)
    print(
      "DAY 2 AGENT - Groq Demo"
    )
    print(
      f"Model: {MODEL}"
    )
    print("="*60)

    print(TASK)

    messages=[]

    stop_reason="max_iterations"

    messages.append(
        {
          "role":"system",
          "content":SYSTEM_PROMPT
        }
    )

    messages.append(
        {
          "role":"user",
          "content":TASK
        }
    )


    for iteration in range(
       1,
       MAX_ITERATIONS+1
    ):

        print(
          separator(
           f"Iteration {iteration}"
          )
        )

        # ----------------------------------
        # LLM Call
        # ----------------------------------

        try:

            response = (
              client.chat.completions.create(
                 model=MODEL,
                 messages=messages,
                 temperature=0,
                 max_tokens=1024
              )
            )

            text = (
              response.choices[0]
              .message.content
              .strip()
            )

        except Exception as e:

            print(
             f"[LLM ERROR] {e}"
            )
            break


        print(text)

        messages.append(
           {
             "role":"assistant",
             "content":text
           }
        )


        # ----------------------------------
        # Done?
        # ----------------------------------

        if "Final Answer:" in text:

            stop_reason="end_turn"

            print(separator())

            print(
             f"Agent finished:"
             f" {stop_reason}"
            )

            print("="*60)

            break


        # ----------------------------------
        # Parse action
        # ----------------------------------

        action = extract_field(
            text,
            "Action"
        )

        action_input = extract_field(
            text,
            "Action Input"
        )


        if not action:

            obs=(
             "Error no Action line."
            )

        elif action not in TOOL_REGISTRY:

            obs=(
             f"Error tool {action} "
             "not found"
            )

        elif not action_input:

            obs=(
             "Error missing "
             "Action Input."
            )

        else:

            try:

                params=json.loads(
                    clean_json(
                      action_input
                    )
                )

                result=TOOL_REGISTRY[
                    action
                ](
                    **params
                )

                obs=(
                  result.model_dump_json(
                     indent=2
                  )
                )

            except json.JSONDecodeError as e:

                obs=(
                  f"JSON error: {e}"
                )

            except TypeError as e:

                obs=(
                  f"Parameter error: {e}"
                )

            except Exception as e:

                obs=f"Error: {e}"


        # ----------------------------------
        # Observation
        # ----------------------------------

        print(
         f"\nObservation:\n{obs}"
        )


        messages.append(
            {
             "role":"user",
             "content":
              f"Observation:\n{obs}"
            }
        )


        time.sleep(
          SLEEP_BETWEEN
        )


    else:

        print(separator())

        print(
         f"Agent stopped:"
         f" {stop_reason}"
        )


    print("\nDone.")


# -------------------------------------------------

if __name__=="__main__":
    run_agent()