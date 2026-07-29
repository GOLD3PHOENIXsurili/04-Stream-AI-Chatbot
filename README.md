What students will learn

This project introduces one major concept:

What is streaming?
Why do ChatGPT and Claude stream responses?
stream=True
Response chunks
Processing tokens as they arrive
Real-time terminal output
Why streaming improves user experience

Notice that we're not introducing memory or tools here. Project 4 focuses on exactly one new capability.

Concepts introduced

By the end of Project 4, students will understand:

Why APIs stream
What a token stream is
Iterator basics (for chunk in response)
Delta messages
Flushing terminal output
Difference between normal completion and streaming completion

We'll explain these after the code:

What is Streaming?
What is a Token?
What is a Chunk?
Why stream=True changes the response type
Why we use for chunk in response
What is delta?
Why some chunks are None
Why assistant_reply += token is necessary
Why flush=True makes the typing effect smooth
Difference between normal completion and streaming completion

