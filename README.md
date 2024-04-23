# Echo
An approach towards second brain


# Second Brain 

This project implements a "second brain" chatbot that can summarize conversations, store summaries and embeddings in a database, and then take queries to return relevant summaries from past conversations.

## Overview

The main components are:

- Speech recognition to transcribe a conversation
- Language model to summarize the conversation
- Database to store summaries and sentence embeddings  
- Sentence embedding API to encode summaries
- User query interface
- Search database to find relevant past summaries
- Language model to generate a response based on retrieved summaries

## Speech Transcription

Uses SpeechRecognition library to record from microphone and transcribe audio to text.

## Conversation Summarization 

Google's Palm language model is used to generate a concise summary while retaining key information.

## Database Storage

MongoDB database stores the summary and its vector embedding for each conversation.

## Sentence Embeddings

The summary text is encoded into a dense vector representation using SentenceTransformers semantic search framework.

## User Query

User can enter a text query and relevant past summaries are retrieved.

## Summary Retrieval

MongoDB's vector similarity search is used to match user query embedding against stored summary embeddings.

## Response Generation

Palm language model generates a response by conditioning on the most relevant retrieved summary.

So in summary, it allows conversational history to be stored in a searchable way, implementing the "second brain" concept where past knowledge is available to inform future responses. The project shows an end-to-end pipeline for this.
