# STEP 1 - Import Required Modules

# Used to access environment variables
import os

# Used to print streamed text on the same line
# We'll use it later to immediately display each token without waiting for Python's output buffer.
# We'll explain flush=True later.
# import sys

# Loads variables from the .env file
from dotenv import load_dotenv

# OpenAI SDK (works with Groq because Groq follows the OpenAI API standard)
from openai import OpenAI

# STEP 2 - Load Environment Variables

# Load all variables from the .env file
load_dotenv()

# STEP 3 - Create the Client
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# STEP 4 - Conversation Memory
# Store the entire conversation history.
messages = []


# Words that end the conversation
EXIT_COMMANDS = ["exit", "quit", "bye"]

# STEP 5 - Start Chat Loop
while True:

    user_input = input("\nYou: ")
    # Ignore empty messages

    #This prevent you from sending empty message to LLM
    if not user_input.strip():
        continue

    if user_input.lower() in EXIT_COMMANDS:
        print("\nAssistant: Goodbye! 👋")
        break

    # Save the user's message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # ⭐ STEP 6 - Enable Streaming (NEW)

    # Replace the old API call with this:

    # Ask the LLM to stream the response instead of
    # waiting for the complete answer.
    # Enable streaming mode.
    #
    # Instead of waiting for the complete response,
    # the API sends small pieces (chunks)
    # as soon as they are generated.
    #
    # This creates the typing effect
    # seen in ChatGPT and Claude.

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )

    """
    ==============================
    What is Streaming?
    ==============================

    Project 3:

    User
    │
    ▼
    LLM thinks...
    (wait)

    (wait)

    (wait)

    Assistant:
    Hello! How are you?

    The user waits until the ENTIRE response is generated.


    Project 4:

    User
    │
    ▼
    LLM generates a few tokens
    │
    ▼
    Show them immediately

    LLM generates more tokens
    │
    ▼
    Show them immediately

    LLM generates more tokens
    │
    ▼
    Show them immediately


    The user starts reading while the model is still generating.

    This is exactly how ChatGPT, Claude and Gemini feel so responsive.

    ------------------------------------------------

    Normal API

    Request
    │
    ▼
    Generate Entire Answer
    │
    ▼
    Return Complete Response


    Streaming API

    Request
    │
    ▼
    Generate Token
    │
    ▼
    Send Token

    Generate Token
    │
    ▼
    Send Token

    Generate Token
    │
    ▼
    Send Token

    ...

    Instead of one big response,
    we receive many small pieces called "chunks".
    """

    # ⭐ STEP 7 - Read Every Chunk
    # Store the complete assistant response.
    assistant_reply = ""

    print("\nAssistant: ", end="", flush=True)

    """
    Why delta instead of message?

    Project 3

    response
        │
        ▼
    message
        │
        ▼
    content


    Project 4

    chunk
        │
        ▼
    delta
        │
        ▼
    content


    A delta means "the new change."

    Instead of sending the complete answer every time,

    the API only sends the newly generated text.

    Example

    Chunk 1

    Hello

    Chunk 2

    ,

    Chunk 3

    how

    Chunk 4

    are

    Chunk 5

    you?

    Each chunk only contains
    the NEW text.
    """

    # Read every chunk as soon as it arrives.
    for chunk in response:

        # Extract the newly generated text.
        token = chunk.choices[0].delta.content

        # Some chunks don't contain text.
        if token:

            # Print immediately without moving
            # to a new line.
            print(token, end="", flush=True)

            # Save the token so we can build
            # the complete response.
            assistant_reply += token

        # Keep building the complete response.
        #
        # Although we're already printing each token,
        # we also need to store it.
        #
        # Later we'll save the assistant's full reply
        # into the conversation history.

    """
    ==============================
    Understanding Streaming Chunks
    ==============================

    The response is no longer ONE object.

    Instead, it becomes an iterator.

    Think of it like this.


    Project 3

    response

    ↓

    Entire Answer


    Project 4

    response

    ↓

    Chunk 1

    ↓

    Chunk 2

    ↓

    Chunk 3

    ↓

    Chunk 4

    ↓

    ...


    Each chunk usually contains only a few characters.

    Example:

    Chunk 1

    {
        "delta": {
            "content": "Hello"
        }
    }

    Chunk 2

    {
        "delta": {
            "content": ", "
        }
    }

    Chunk 3

    {
        "delta": {
            "content": "how"
        }
    }

    Chunk 4

    {
        "delta": {
            "content": " are"
        }
    }

    Chunk 5

    {
        "delta": {
            "content": " you?"
        }
    }


    Instead of waiting for all chunks,
    we immediately display every chunk.

    The final output becomes

    Hello, how are you?


    This creates the typing effect.

    """
    """
    =========================================
    Why do we use

    for chunk in response

    instead of

    response.choices[0] ?
    =========================================

    Project 3

    Response

    ↓

    Entire Answer


    Project 4

    Response

    ↓

    Chunk

    ↓

    Chunk

    ↓

    Chunk

    ↓

    Chunk


    Streaming no longer returns
    one complete response.

    Instead,

    it returns an iterator.

    An iterator gives us one chunk
    at a time.

    That's why we write

    for chunk in response

    instead of

    response.choices[0].
    """

    # STEP 8 - Save Assistant Memory
    # Move the cursor to the next line
    # after streaming is complete.
    print()

    # Save the assistant's complete response.
    # This allows the model to remember
    # its own previous replies in the next conversation.

    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    """
    =====================================
    Project 3 vs Project 4
    =====================================

    Project 3

    User
    │
    ▼
    Wait...
    │
    ▼
    Entire Response
    │
    ▼
    Print


    Project 4

    User
    │
    ▼
    Generate Token
    │
    ▼
    Print Token
    │
    ▼
    Generate Next Token
    │
    ▼
    Print Token


    Result

    Project 3
    ---------
    Feels like waiting.

    Project 4
    ---------
    Feels like ChatGPT typing.
    """