from model_interface.prompts import Prompt

test_prompt: Prompt = Prompt()

def test_entity_recog():
    prompt = test_prompt.get_entity_recog_conv_prompt("Will my house flood?")
    assert type(prompt), str

    print(prompt)

def test_step_gen():
    prompt = test_prompt.get_step_gen_conv_prompt("Will my house flood?")
    assert type(prompt), str

    print(prompt)

def main():
    test_entity_recog()
    print("----------------------------------")
    test_step_gen()

if __name__ == "__main__":
    main()
