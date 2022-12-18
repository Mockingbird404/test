
import openai

openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman:"


while True:
	
	restart_sequence = input("\nHuman: ")
	response = openai.Completion.create(
		  model="text-davinci-003",
		  prompt= restart_sequence,
		  temperature=0.9,
		  max_tokens=150,
		  top_p=1,
		  frequency_penalty=0,
		  presence_penalty=0.6,
		  stop=[" Human:", " AI:"]
		)
	print("AI: " + response["choices"][0]["text"])
	
	