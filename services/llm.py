from openai import AsyncOpenAI
from settings import AppSettings
from models import Conversation
from repositories.conversations import ConversationRepository
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

settings = AppSettings()

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def generate_conversation_title(self, initial_prompt: str) -> str:
        """Generate a title for the conversation based on the initial prompt"""
        try:
            completion = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Suggest a short, descriptive title (max 50 characters) for the conversation based on the user prompt. Return only the title, nothing else.",
                    },
                    {
                        "role": "user",
                        "content": initial_prompt,
                    },
                ],
                model="gpt-3.5-turbo",
                max_tokens=50,
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating title: {e}")
            return "New Conversation"
    
    async def create_conversation_with_title(
        self, initial_prompt: str, session: AsyncSession
    ) -> Conversation:
        """Create a new conversation with an AI-generated title"""
        title = await self.generate_conversation_title(initial_prompt)
        
        conversation = Conversation(
            title=title,
            model_type="gpt-3.5-turbo"
        )
        
        return await ConversationRepository(session).create(conversation)
    
    async def stream_response(self, prompt: str, conversation_id: int = None):
        """Stream response from OpenAI"""
        try:
            stream = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, concise, and accurate responses.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                model="gpt-3.5-turbo",
                stream=True,
            )
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            print(f"Error streaming response: {e}")
            yield f"Error: {str(e)}" 