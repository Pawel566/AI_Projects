from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI()
chat_history = ""

print("Cześć! O co chcesz zapytać? Wyjście z rozmowy q/exit")

while True:
    question = input(f"Ja: ")
    if question.lower() in ["q", "exit"]:
        print("Koniec rozmowy. Cześć")
        break

    chat_history += f"Ja: {question}\n"

    response = client.responses.create(
    model="gpt-5-mini",
    input=chat_history
    )

    answer = response.output_text
    print(f"Bot:{answer}")
    chat_history += f"Bot: {answer}\n"
