# main.py

from prompt_logic import extract_conditions, generate_prompt

def main():
    intent = input("💡 What do you want to do? (summary/self_intro/customer_reply/code_run): ").strip()
    conditions = extract_conditions()

    if intent == "code_run":
        command = input("💻 Enter the Python command: ").strip()
        conditions["command"] = command

    prompt = generate_prompt(intent, conditions)

    print("\n🧠 [Generated Prompt]")
    print(prompt)

if __name__ == "__main__":
    main()
