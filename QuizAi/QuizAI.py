from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

print("=== QUIZ AI ===\nAby wyjść wpisz 'q' lub 'quit'")

while True:
    category = input("Podaj kategorię: ").strip()
    if category.lower() in ["q", "quit", "exit"]:
        print("Koniec quizu")
        raise SystemExit
    if category:
        break

num_questions = 10
score = 0

messages = [
    {
        "role": "system",
        "content": (
            f"Jesteś quizbotem AI. Zadajesz pytania z kategorii {category}. "
            "Każde pytanie ma 4 warianty (A-D) i tylko jedną poprawną odpowiedź. "
            "Po otrzymaniu odpowiedzi oceń ją: 'Dobrze!' lub 'Źle.' "
            "Na końcu dodaj ukryty znacznik techniczny: "
            "'ANSWER: OK' jeśli odpowiedź była poprawna lub 'ANSWER: WRONG' jeśli błędna. "
            "Nie zadawaj kolejnego pytania, dopóki użytkownik o to nie poprosi."
        )
    }
]

messages.append({"role": "user", "content": "Podaj pierwsze pytanie."})
question = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages
).choices[0].message.content

for i in range(num_questions):
    print(f"\n{question}")
    messages.append({"role": "assistant", "content": question})

    while True:
        answer = input("Twoja odpowiedź: ").strip().upper()
        if answer in ["Q", "QUIT", "EXIT"]:
            print("Przerwano quiz.")
            num_questions = i
            break
        if answer in ["A", "B", "C", "D"]:
            break

    messages.append({"role": "user", "content": f"Moja odpowiedź: {answer}"})
    feedback = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages
    ).choices[0].message.content

    lines = feedback.strip().splitlines()
    visible = "\n".join(line for line in lines if not line.startswith("ANSWER:"))
    hidden_tag = next((line for line in lines if line.startswith("ANSWER:")), "")

    print(visible)
    messages.append({"role": "assistant", "content": feedback})

    if "ANSWER: OK" in hidden_tag:
        score += 1

    if i < num_questions - 1:
        messages.append({"role": "user", "content": f"Podaj kolejne pytanie (nr {i+2})."})
        question = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages
        ).choices[0].message.content

print(f"\n=== KONIEC QUIZU ===")
print(f"Wynik: {score}/{num_questions} ({round(score/num_questions*100)}%)")

messages.append({
    "role": "user",
    "content": (
        f"Zdobyłem {score} punktów na {num_questions}. "
        "Oceń ten wynik krótko i rzeczowo (bez gratulacji, bez słodzenia, maks 1-2 zdania). "
        "Jeśli wynik jest słaby – powiedz to wprost."
    )
})

ai_evaluate = client.chat.completions.create(
    model="gpt-5-mini",
    messages=messages
).choices[0].message.content

print("\nOcena wyniku:")
print(ai_evaluate)