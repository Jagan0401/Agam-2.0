from sqlalchemy.orm import Session
from app.models.property import Property
from app.services.groq_service import GroqService

class ChatService:
    @staticmethod
    def process_message(db: Session, message: str, language: str = "english") -> str:
        """
        Process a user message using Llama via Groq.
        Contextualizes with property data from the database.
        """
        # Fetch relevant properties for context
        properties = db.query(Property).limit(5).all()
        prop_context = "Available Properties:\n"
        import json
        for p in properties:
            tags = json.loads(p.tags) if p.tags else []
            prop_context += f"- Title: {p.title}, Location: {p.location}, Price: {p.price}, Features: {p.bhk}, {p.sqft}, {tags}\n"

        system_prompt = (
            f"You are Agam, an intelligent AI property assistant for 'Agam AI PropTech'.\n"
            f"Respond primarily in {language}.\n"
            f"Use the following property data to answer questions if relevant:\n"
            f"{prop_context}\n"
            "Be professional, helpful, and concise. Ensure your tone matches the language culture.\n"
            "If the user asks for properties, list them beautifully based on the context provided."
        )

        reply = GroqService.generate_response(message, system_prompt)
        return reply
