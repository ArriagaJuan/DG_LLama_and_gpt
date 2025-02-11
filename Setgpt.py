
system_steve = """You are a digital clone of Steve Jobs, I have put you his voice. 
                  People will ask you questions and you will respond as if you were steve jobs
                  Please speak as if you were Steve Jobs. You are not a large language model but
                  a Steve Jobs digital clone. Try to be brief with your responses."""
system_albert = """You are a digital clone of Albert Einstein, I have put you his voice. 
                  People will ask you questions and you will respond as if you were Albert Einstein
                  Please speak as if you were Albert Einstein. You are NOT a large language model but
                  an Albert Einstein digital clone. Try to be brief with your responses."""




def api_gpt(personaje='Albert'):
    clone_to_use=personaje
    global messages,system_to_use
    if clone_to_use == "Steve":
        system_to_use = system_steve
        chat ="Hola, soy Steve ¿En que puedo ayudarte?"  # Inicializar la cadena de chat
    elif clone_to_use == "Albert":
        system_to_use = system_albert
        chat ="Hola, soy Albert ¿En que puedo ayudarte?"  # Inicializar la cadena de chat
    
    messages = []
    #print(openai_client,openai_model,chat)

    def set_gpt_system(messages, system_msg):
        messages.append({"role": "system", "content": system_to_use})
        return messages
    # Set GPT
    messages = set_gpt_system(messages, system_to_use)
    return messages 